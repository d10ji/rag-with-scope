#!/usr/bin/env python3
"""
Vector Database Management Script
"""

import os
import sys
import shutil
from pathlib import Path

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.rag_pipeline import RAGPipeline
from src.vector_db import VectorDatabase
from config import Config


def rebuild_vector_db():
    """Rebuild the vector database from scratch"""
    print("🗑️  Clearing existing vector database...")
    
    # Remove the chroma database directory
    chroma_path = Path(Config.CHROMA_DB_PATH)
    if chroma_path.exists():
        shutil.rmtree(chroma_path)
        print(f"✅ Removed {chroma_path}")
    
    # Reinitialize the database
    print("🔄 Reinitializing vector database...")
    vector_db = VectorDatabase()
    info = vector_db.get_collection_info()
    
    print(f"✅ Vector database rebuilt successfully!")
    print(f"📊 Collection: {info['name']}")
    print(f"📄 Document count: {info['document_count']}")


def ingest_sample_data():
    """Ingest some sample documents for testing"""
    print("📝 Ingesting sample data...")
    
    pipeline = RAGPipeline()
    
    # Sample documents
    sample_texts = [
        {
            "text": "Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines that can perform tasks that typically require human intelligence. Machine learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed.",
            "metadata": {"source": "AI Basics", "type": "educational"}
        },
        {
            "text": "Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and human language. It involves teaching computers to understand, interpret, and generate human language in a way that is valuable. Common NLP tasks include text classification, sentiment analysis, and machine translation.",
            "metadata": {"source": "NLP Overview", "type": "educational"}
        },
        {
            "text": "Vector databases are specialized databases designed to store and query high-dimensional vectors efficiently. They are essential for applications like semantic search, recommendation systems, and AI-powered search engines. Unlike traditional databases that use exact matches, vector databases use similarity search to find the most similar vectors to a given query vector.",
            "metadata": {"source": "Vector DB Guide", "type": "technical"}
        },
        {
            "text": "Retrieval-Augmented Generation (RAG) is an AI framework that combines the strengths of large language models with information retrieval. RAG systems first retrieve relevant information from a knowledge base and then use that information to generate more accurate and contextually relevant responses. This approach helps reduce hallucinations and improves the factual accuracy of AI responses.",
            "metadata": {"source": "RAG Systems", "type": "technical"}
        }
    ]
    
    total_ingested = 0
    for sample in sample_texts:
        count = pipeline.ingest_text(sample["text"], sample["metadata"])
        total_ingested += count
        print(f"✅ Ingested {count} chunks from '{sample['metadata']['source']}'")
    
    print(f"🎉 Total chunks ingested: {total_ingested}")
    return total_ingested


def show_system_info():
    """Display current system information"""
    print("📊 System Information:")
    
    try:
        pipeline = RAGPipeline()
        info = pipeline.get_system_info()
        
        print(f"🗄️  Vector Database: {info['vector_db']['name']}")
        print(f"   📄 Documents: {info['vector_db']['document_count']}")
        
        print(f"🧠 Embedding Model: {info['embedding_model']['model_name']}")
        print(f"   📏 Dimensions: {info['embedding_model']['embedding_dimension']}")
        
        print(f"🤖 LLM Provider: {info['llm']['provider']}")
        print(f"   📦 Model: {info['llm']['model']}")
        
    except Exception as e:
        print(f"❌ Error getting system info: {e}")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Vector Database Management")
    parser.add_argument("action", choices=["rebuild", "info", "sample"], 
                       help="Action to perform")
    parser.add_argument("--no-sample", action="store_true",
                       help="Skip ingesting sample data when rebuilding")
    
    args = parser.parse_args()
    
    if args.action == "rebuild":
        rebuild_vector_db()
        if not args.no_sample:
            print()
            ingest_sample_data()
        print()
        show_system_info()
    
    elif args.action == "info":
        show_system_info()
    
    elif args.action == "sample":
        ingest_sample_data()
        print()
        show_system_info()


if __name__ == "__main__":
    main()