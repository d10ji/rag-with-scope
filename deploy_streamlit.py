#!/usr/bin/env python3
"""
Deployment script for Streamlit Community Cloud
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if all requirements are met for deployment"""
    print("🔍 Checking deployment requirements...")
    
    # Check if streamlit is in requirements
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
        if 'streamlit' not in requirements:
            print("❌ Streamlit not found in requirements.txt")
            return False
        else:
            print("✅ Streamlit found in requirements.txt")
    
    # Check if .env exists (but don't commit it)
    if os.path.exists('.env'):
        print("⚠️  .env file exists locally - ensure secrets are set in Streamlit Cloud")
    
    # Check main app file
    if os.path.exists('streamlit_app.py'):
        print("✅ Main app file exists")
    else:
        print("❌ Main app file not found")
        return False
    
    print("✅ All requirements checked")
    return True

def create_secrets_template():
    """Create a template for Streamlit Cloud secrets"""
    secrets_content = """
# Copy this to your Streamlit Cloud secrets configuration
[env]
GROQ_API_KEY = "your_groq_api_key_here"
CHROMA_DB_PATH = "./data/chroma"
COLLECTION_NAME = "rag_documents"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.1-8b-instant"
CHUNK_SIZE = "1000"
CHUNK_OVERLAP = "200"
MAX_RETRIEVED_DOCS = "5"
SIMILARITY_THRESHOLD = "0.7"
"""
    
    with open('streamlit_secrets.toml', 'w') as f:
        f.write(secrets_content)
    
    print("📝 Created streamlit_secrets.toml template")

if __name__ == "__main__":
    if check_requirements():
        create_secrets_template()
        print("\n🚀 Ready for Streamlit Community Cloud deployment!")
        print("\nNext steps:")
        print("1. Push your code to GitHub")
        print("2. Go to share.streamlit.io")
        print("3. Connect your GitHub repository")
        print("4. Configure secrets using streamlit_secrets.toml as reference")
        print("5. Deploy!")