from typing import List, Dict, Any
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
    
    def ingest_text(self, text: str, metadata: Dict[str, Any] = None) -> int:
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
    
    def query(self, question: str, max_results: int = None) -> Dict[str, Any]:
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
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get information about the RAG system"""
        return {
            "vector_db": self.vector_db.get_collection_info(),
            "embedding_model": self.embedding_model.get_model_info(),
            "llm": self.llm.get_model_info()
        }