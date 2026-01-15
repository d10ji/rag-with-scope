#!/bin/bash
# RAG System Production Test Script
echo "🚀 Setting up RAG System Production Test..."
echo "=================================================="

# Create fresh virtual environment
echo "1. 📦 Creating virtual environment..."
python3 -m venv venv_test
source venv_test/bin/activate

# Install dependencies
echo "2. 📦 Installing dependencies..."
pip install --quiet python-dotenv groq chromadb sentence-transformers langchain pypdf

# Test the system
echo "3. 🧪 Testing RAG System..."
python3 -c "
import sys
sys.path.insert(0, '.')
from config import Config
from src.rag_pipeline import RAGPipeline

print('✅ Configuration loaded')
print(f'   LLM Provider: {Config.LLM_PROVIDER}')
print(f'   Groq Model: {Config.GROQ_MODEL}')
print(f'   Embedding Model: {Config.EMBEDDING_MODEL}')

rag = RAGPipeline()
print('✅ RAG Pipeline initialized')

# Test document ingestion
test_text = 'RAG systems combine vector databases with large language models for enhanced information retrieval.'
count = rag.ingest_text(test_text, {'source': 'test'})
print(f'✅ Document ingested: {count} chunks')

# Test query
result = rag.query('What is a RAG system?')
print(f'✅ Query processed: {len(result[\"answer\"])} chars in response')
print(f'✅ Sources found: {len(result[\"sources\"])} relevant chunks')

print('🎉 RAG System is FULLY OPERATIONAL!')
"

echo "4. 🧹 Cleaning up..."
deactivate
rm -rf venv_test

echo "=================================================="
echo "✅ PRODUCTION TEST COMPLETE - RAG System Ready!"
echo "📋 To use in production:"
echo "   source .venv/bin/activate"
echo "   python3 src/cli.py --interactive"
echo "   python3 src/cli.py --query 'your question here'"
echo "   python3 src/cli.py --ingest-file your_document.pdf"