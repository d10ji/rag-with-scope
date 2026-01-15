import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import os
from config import Config


class VectorDatabase:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_DB_PATH,
            settings=Settings(allow_reset=True)
        )
        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]] = None, ids: List[str] = None):
        """Add documents to the vector database"""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        if metadatas is None:
            metadatas = [{"source": f"document_{i}"} for i in range(len(documents))]
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, query_text: str, n_results: int = None) -> Dict[str, Any]:
        """Query the vector database"""
        if n_results is None:
            n_results = Config.MAX_RETRIEVED_DOCS
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        return results
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        count = self.collection.count()
        return {
            "name": Config.COLLECTION_NAME,
            "document_count": count,
            "path": Config.CHROMA_DB_PATH
        }
    
    def delete_collection(self):
        """Delete the entire collection"""
        self.client.delete_collection(name=Config.COLLECTION_NAME)
    
    def reset_database(self):
        """Reset the entire database"""
        self.client.reset()