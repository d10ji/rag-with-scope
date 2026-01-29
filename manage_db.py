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
    
    try:
        # Use the built-in reset functionality
        vector_db = VectorDatabase()
        vector_db.reset_database()
        print("✅ Database reset using built-in functionality")
    except Exception as e:
        print(f"⚠️  Built-in reset failed: {e}")
        
        # Fallback: try to remove the database file
        milvus_path = Path(Config.MILVUS_DB_PATH)
        if milvus_path.exists():
            try:
                if milvus_path.is_file():
                    milvus_path.unlink()
                    print(f"✅ Removed Milvus database file: {milvus_path}")
                elif milvus_path.is_dir():
                    shutil.rmtree(milvus_path)
                    print(f"✅ Removed Milvus database directory: {milvus_path}")
            except Exception as cleanup_error:
                print(f"⚠️  Could not remove database file: {cleanup_error}")
    
    # Add a small delay to ensure proper cleanup
    import time
    time.sleep(1)
    
    # Reinitialize the database
    print("🔄 Reinitializing vector database...")
    try:
        vector_db = VectorDatabase()
        info = vector_db.get_collection_info()
        
        print(f"✅ Vector database rebuilt successfully!")
        print(f"📊 Collection: {info['name']}")
        print(f"📄 Document count: {info['document_count']}")
    except Exception as e:
        print(f"❌ Failed to reinitialize database: {e}")
        raise


def ingest_sample_data():
    """Ingest some sample documents for testing"""
    print("📝 Ingesting sample data...")
    
    pipeline = RAGPipeline()
    
    # Sample documents
    sample_texts = [ ]
    
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