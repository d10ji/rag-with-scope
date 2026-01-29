from typing import List, Dict, Any, Optional
from src.vector_db import VectorDatabase
from src.embeddings import EmbeddingModel
from src.llm import LLMProvider
from src.document_processor import DocumentProcessor
from config import Config
import uuid


class RAGPipeline:
    def __init__(self):
        self.vector_db = VectorDatabase()
        self.embedding_model = EmbeddingModel()
        self.llm = LLMProvider()
        self.document_processor = DocumentProcessor()
    
    def ingest_document(self, file_path: str) -> int:
        """Ingest a document into the RAG system"""
        chunks = self.document_processor.process_document(file_path)
        return self._ingest_chunks(chunks)
    
    def ingest_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        """Ingest raw text into the RAG system"""
        chunks = self.document_processor.process_text(text, metadata)
        return self._ingest_chunks(chunks)
    
    def ingest_directory(self, directory_path: str) -> int:
        """Ingest all documents from a directory"""
        chunks = self.document_processor.process_directory(directory_path)
        return self._ingest_chunks(chunks)
    
    def _ingest_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """Helper method to ingest chunks into vector database"""
        if not chunks:
            return 0
        
        documents = [chunk["content"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        ids = [str(uuid.uuid4()) for _ in chunks]
        
        self.vector_db.add_documents(documents, metadatas, ids)
        return len(chunks)
    
    def query(self, question: str, max_results: Optional[int] = None) -> Dict[str, Any]:
        """Query the RAG system"""
        if max_results is None:
            max_results = Config.MAX_RETRIEVED_DOCS
        
        # Retrieve relevant documents
        search_results = self.vector_db.query(question, max_results)
        
        if not search_results["documents"] or not search_results["documents"][0]:
            return {
                "question": question,
                "answer": "I couldn't find any relevant information to answer your question.",
                "sources": []
            }
        
        # Extract context and sources
        context_docs = search_results["documents"][0]
        sources = []
        
        for i, doc in enumerate(context_docs):
            metadata = search_results["metadatas"][0][i] if search_results["metadatas"] else {}
            sources.append({
                "content": doc,
                "metadata": metadata,
                "distance": search_results["distances"][0][i] if search_results["distances"] else None
            })
        
        # Generate response
        answer = self.llm.generate_response(question, context_docs)
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents from the RAG system, grouped by original documents"""
        results = self.vector_db.get_all_documents()
        documents = []
        
        if results['documents']:
            for i, doc in enumerate(results['documents']):
                metadata = results['metadatas'][i] if results['metadatas'] else {}
                documents.append({
                    "content": doc,
                    "metadata": metadata,
                    "id": results['ids'][i] if results['ids'] else f"doc_{i}"
                })
        
        return documents
    
    def get_unique_documents(self) -> List[Dict[str, Any]]:
        """Get unique documents (grouped by source file) from the RAG system"""
        results = self.vector_db.get_all_documents()
        documents_by_source = {}
        
        if results['documents']:
            for i, doc in enumerate(results['documents']):
                metadata = results['metadatas'][i] if results['metadatas'] else {}
                
                # Determine the source key
                source_key = None
                if 'source_file' in metadata:
                    source_key = metadata['source_file']
                elif 'source' in metadata:
                    source_key = metadata['source']
                else:
                    source_key = f"Document {i}"
                
                # Extract filename from path if it's a path
                if '/' in source_key or '\\' in source_key:
                    source_key = source_key.split('/')[-1].split('\\')[-1]
                
                # Group by source
                if source_key not in documents_by_source:
                    documents_by_source[source_key] = {
                        "source": source_key,
                        "chunks": [],
                        "metadata": {},
                        "total_chunks": 0
                    }
                
                documents_by_source[source_key]["chunks"].append({
                    "content": doc,
                    "chunk_id": metadata.get('chunk_id', 0),
                    "id": results['ids'][i] if results['ids'] else f"doc_{i}"
                })
                
                # Merge metadata (excluding chunk-specific fields)
                for key, value in metadata.items():
                    if key not in ['chunk_id', 'source_file'] and value:
                        documents_by_source[source_key]["metadata"][key] = value
                
                documents_by_source[source_key]["total_chunks"] += 1
        
        # Convert to list
        return list(documents_by_source.values())
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get information about the RAG system"""
        return {
            "vector_db": self.vector_db.get_collection_info(),
            "embedding_model": self.embedding_model.get_model_info(),
            "llm": self.llm.get_model_info()
        }