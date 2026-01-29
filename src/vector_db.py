from pymilvus import MilvusClient, CollectionSchema, FieldSchema, DataType
from typing import List, Dict, Any
import os
import numpy as np
from config import Config


class VectorDatabase:
    def __init__(self):
        # Dynamic Milvus connection based on environment
        if Config.IS_DEVELOPMENT:
            # Local Milvus using milvus-lite
            self.client = MilvusClient(uri=Config.MILVUS_URI or "./data/milvus.db")
            self.connection_type = "local"
            print(f"🔧 Connecting to local Milvus: {Config.MILVUS_URI or './data/milvus.db'}")
        else:
            # Cloud Milvus - ensure required values are present
            if not Config.MILVUS_URI:
                raise ValueError("MILVUS_URI is required for production environment")
            if not Config.MILVUS_TOKEN:
                raise ValueError("MILVUS_TOKEN is required for production environment")
            
            self.client = MilvusClient(
                uri=Config.MILVUS_URI,
                token=Config.MILVUS_TOKEN
            )
            self.connection_type = "cloud"
            print(f"☁️ Connecting to cloud Milvus: {Config.MILVUS_URI}")
        
        self.collection_name = Config.COLLECTION_NAME
        
        # Get embedding dimension from the embedding model
        from src.embeddings import EmbeddingModel
        embedding_model = EmbeddingModel()
        self.embedding_dim = embedding_model.get_embedding_dimension()
        
        # Create collection if it doesn't exist
        if not self.client.has_collection(self.collection_name):
            self._create_collection()
    
    def _create_collection(self):
        """Create a Milvus collection with appropriate schema"""
        # Define the schema with proper field types
        schema = self.client.create_schema(
            auto_id=False,
            enable_dynamic_field=True
        )
        
        schema.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=100, is_primary=True)
        schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)
        schema.add_field(field_name="metadata", datatype=DataType.JSON)
        schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=self.embedding_dim)
        
        # Create the collection with schema
        self.client.create_collection(
            collection_name=self.collection_name,
            schema=schema,
            consistency_level="Strong"
        )
        
        # Create index for vector field using AUTOINDEX (supported in Milvus lite)
        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name="vector",
            metric_type="COSINE",
            index_type="AUTOINDEX"
        )
        
        self.client.create_index(
            collection_name=self.collection_name,
            index_params=index_params
        )
        
        print(f"✅ Created Milvus collection '{self.collection_name}' with index")
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]] | None = None, ids: List[str] | None = None):
        """Add documents to the vector database"""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        if metadatas is None:
            metadatas = [{"source": f"document_{i}"} for i in range(len(documents))]
        
        # Generate embeddings
        from src.embeddings import EmbeddingModel
        embedding_model = EmbeddingModel()
        embeddings = embedding_model.encode(documents)
        
        # Prepare data for insertion
        data = []
        for i, (doc, meta, emb) in enumerate(zip(documents, metadatas, embeddings)):
            data.append({
                "id": ids[i],
                "text": doc,
                "metadata": meta,
                "vector": emb.tolist()
            })
        
        # Insert data
        self.client.insert(collection_name=self.collection_name, data=data)
        print(f"✅ Inserted {len(data)} chunks")
    
    def query(self, query_text: str, n_results: int | None = None) -> Dict[str, Any]:
        """Query the vector database"""
        if n_results is None:
            n_results = Config.MAX_RETRIEVED_DOCS
        
        # Generate embedding for query
        from src.embeddings import EmbeddingModel
        embedding_model = EmbeddingModel()
        query_embedding = embedding_model.encode_single(query_text)
        
        # Perform search - let Milvus handle search params
        search_results = self.client.search(
            collection_name=self.collection_name,
            data=[query_embedding.tolist()],
            limit=n_results,
            output_fields=["text", "metadata"]
        )[0]
        
        # Format results to match ChromaDB format
        formatted_results = {
            "ids": [[result["id"] for result in search_results]],
            "documents": [[result["entity"]["text"] for result in search_results]],
            "metadatas": [[result["entity"]["metadata"] for result in search_results]],
            "distances": [[result["distance"] for result in search_results]]
        }
        
        return formatted_results
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        stats = self.client.get_collection_stats(collection_name=self.collection_name)
        return {
            "name": Config.COLLECTION_NAME,
            "document_count": stats.get("row_count", 0),
            "connection_type": self.connection_type,
            "uri": Config.MILVUS_URI,
            "environment": Config.ENVIRONMENT
        }
    
    def delete_collection(self):
        """Delete the entire collection"""
        if self.client.has_collection(self.collection_name):
            self.client.drop_collection(collection_name=self.collection_name)
    
    def get_all_documents(self) -> Dict[str, Any]:
        """Get all documents from the collection"""
        # Query all documents
        results = self.client.query(
            collection_name=self.collection_name,
            filter="id != ''",
            output_fields=["id", "text", "metadata"],
            limit=16384  # Large number to get all documents
        )
        
        # Format results to match ChromaDB format
        formatted_results = {
            "ids": [doc["id"] for doc in results],
            "documents": [doc["text"] for doc in results],
            "metadatas": [doc["metadata"] for doc in results]
        }
        
        return formatted_results
    
    def reset_database(self):
        """Reset the entire database"""
        try:
            # Delete the collection if it exists
            if self.client.has_collection(self.collection_name):
                self.client.drop_collection(collection_name=self.collection_name)
                print(f"✅ Dropped collection '{self.collection_name}'")
        except Exception as e:
            print(f"⚠️  Error dropping collection: {e}")
        
        # Recreate collection
        self._create_collection()