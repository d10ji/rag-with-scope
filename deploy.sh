#!/bin/bash

set -e

echo "🚀 RAG System Streamlit Deployment Script"
echo "=========================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it with your GROQ_API_KEY"
    exit 1
fi

echo "✅ Prerequisites checked"

# Deployment options
echo ""
echo "🎯 Choose deployment option:"
echo "1) Local Docker deployment"
echo "2) Production Docker deployment (with HTTPS)"
echo "3) Streamlit Community Cloud setup"
echo "4) Quick test deployment"

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🏠 Starting local Docker deployment..."
        docker-compose up --build -d
        echo "✅ App deployed locally at http://localhost:8501"
        ;;
    
    2)
        echo "🏭 Starting production Docker deployment..."
        
        # Create production docker-compose file
        cat > docker-compose.prod.yml << EOF
version: '3.8'

services:
  rag-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GROQ_API_KEY=\${GROQ_API_KEY}
      - CHROMA_DB_PATH=./data/chroma
      - COLLECTION_NAME=rag_documents
      - EMBEDDING_MODEL=all-MiniLM-L6-v2
      - GROQ_MODEL=llama-3.1-8b-instant
      - CHUNK_SIZE=1000
      - CHUNK_OVERLAP=200
      - MAX_RETRIEVED_DOCS=5
      - SIMILARITY_THRESHOLD=0.7
    volumes:
      - ./data:/app/data
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - rag-app
    restart: always
EOF
        
        echo "📝 Created production docker-compose file"
        echo "⚠️  Note: For HTTPS, you'll need to configure SSL certificates and nginx.conf"
        docker-compose -f docker-compose.prod.yml up --build -d
        echo "✅ Production deployment started"
        ;;
    
    3)
        echo "☁️  Setting up for Streamlit Community Cloud..."
        
        # Check if git repo
        if [ ! -d ".git" ]; then
            echo "❌ Not a git repository. Initialize git first:"
            echo "   git init"
            echo "   git add ."
            echo "   git commit -m 'Initial commit'"
            exit 1
        fi
        
        # Create deployment script
        python deploy_streamlit.py
        
        echo ""
        echo "📋 Streamlit Community Cloud Setup:"
        echo "1. Make sure your code is pushed to GitHub"
        echo "2. Go to https://share.streamlit.io"
        echo "3. Connect your GitHub repository"
        echo "4. In 'Secrets' section, add your GROQ_API_KEY"
        echo "5. Set main file path to 'streamlit_app.py'"
        echo "6. Click 'Deploy'"
        ;;
    
    4)
        echo "⚡ Quick test deployment..."
        docker run --rm -it \
            -p 8501:8501 \
            -v $(pwd):/app \
            -w /app \
            python:3.12-slim \
            bash -c "
                apt-get update && apt-get install -y curl && \
                pip install -r requirements.txt && \
                streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
            "
        ;;
    
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment process completed!"
echo ""
echo "📊 Monitoring commands:"
echo "- View logs: docker-compose logs -f"
echo "- Stop app: docker-compose down"
echo "- Restart app: docker-compose restart"