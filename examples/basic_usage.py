#!/usr/bin/env python3
"""
Basic usage example for the Simple RAG System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.rag_pipeline import RAGPipeline
from config import Config


def main():
    print("=== Simple RAG System Example ===\n")
    
    # Initialize the RAG pipeline
    rag = RAGPipeline()
    
    # Show system information
    print("1. System Information:")
    info = rag.get_system_info()
    print(f"   - Vector DB: {info['vector_db']['name']} ({info['vector_db']['document_count']} documents)")
    print(f"   - Embedding Model: {info['embedding_model']['model_name']}")
    print(f"   - LLM Provider: {info['llm']['provider']} ({info['llm']['model']})")
    print()
    
    # Ingest some sample text
    print("2. Ingesting sample documents...")
    sample_texts = [
        ("Python is a high-level programming language known for its simplicity and readability. "
         "It was created by Guido van Rossum and first released in 1991. "
         "Python supports multiple programming paradigms including procedural, object-oriented, and functional programming."),
        
        ("Machine learning is a subset of artificial intelligence that focuses on the development of "
         "algorithms that can learn and make predictions from data. "
         "Common machine learning tasks include classification, regression, clustering, and dimensionality reduction."),
        
        ("ChromaDB is an open-source vector database designed for AI applications. "
         "It allows developers to store and query high-dimensional vectors efficiently, "
         "making it ideal for similarity search and retrieval-augmented generation systems.")
    ]
    
    total_chunks = 0
    for i, text in enumerate(sample_texts):
        metadata = {"source": f"sample_text_{i+1}", "type": "example"}
        count = rag.ingest_text(text, metadata)
        total_chunks += count
        print(f"   - Sample text {i+1}: {count} chunks")
    
    print(f"   Total chunks ingested: {total_chunks}\n")
    
    # Query the system
    print("3. Sample Queries:")
    
    queries = [
        "What is Python programming language?",
        "How does machine learning work?",
        "What is ChromaDB used for?",
        "Tell me about AI and vector databases"
    ]
    
    for query in queries:
        print(f"\n   Query: {query}")
        try:
            result = rag.query(query)
            print(f"   Answer: {result['answer']}")
            print(f"   Sources: {len(result['sources'])} relevant chunks")
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()