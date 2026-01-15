#!/usr/bin/env python3
"""
Simple test for basic functionality without heavy dependencies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

def test_config():
    """Test configuration loading"""
    print("=== Configuration Test ===")
    print(f"LLM Provider: {Config.LLM_PROVIDER}")
    print(f"Groq Model: {Config.GROQ_MODEL}")
    print(f"Embedding Model: {Config.EMBEDDING_MODEL}")
    print(f"Chunk Size: {Config.CHUNK_SIZE}")
    print("✅ Configuration loaded successfully")

def test_basic_imports():
    """Test basic imports"""
    try:
        import groq
        print("✅ Groq imported successfully")
    except ImportError as e:
        print(f"❌ Groq import failed: {e}")
    
    try:
        import chromadb
        print("✅ ChromaDB imported successfully")
    except ImportError as e:
        print(f"❌ ChromaDB import failed: {e}")

def test_groq_api():
    """Test Groq API connection"""
    try:
        from groq import Groq
        
        if not Config.GROQ_API_KEY or Config.GROQ_API_KEY == "your_groq_api_key_here":
            print("⚠️  Groq API key not configured")
            return
        
        client = Groq(api_key=Config.GROQ_API_KEY)
        
        # Test simple completion
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Say 'Hello from Groq!'"}],
            model=Config.GROQ_MODEL,
            max_tokens=10
        )
        
        print(f"✅ Groq API test successful: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ Groq API test failed: {e}")

if __name__ == "__main__":
    print("=== Simple RAG System Test ===\n")
    
    test_config()
    print()
    
    test_basic_imports()
    print()
    
    test_groq_api()
    print("\n=== Test completed ===")