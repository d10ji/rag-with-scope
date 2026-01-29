import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Environment Detection
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
    IS_PRODUCTION = ENVIRONMENT in ["production", "prod"]
    IS_DEVELOPMENT = ENVIRONMENT in ["development", "dev", "local"]
    
    # Vector Database - Dynamic Configuration
    if IS_DEVELOPMENT:
        # Local Milvus configuration
        MILVUS_URI = os.getenv("MILVUS_DB_PATH", "./data/milvus.db")
        MILVUS_TOKEN = None
        MILVUS_TYPE = "local"
    else:
        # Cloud Milvus configuration
        MILVUS_URI = os.getenv("MILVUS_URI")
        MILVUS_TOKEN = os.getenv("MILVUS_TOKEN")
        MILVUS_TYPE = "cloud"
        
        # Required for production
        if not MILVUS_URI:
            raise ValueError("MILVUS_URI must be set in production environment")
    
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_documents")
    
    # Embedding Model
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama2-70b-4096")
    
    # Document Processing
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Search Configuration
    MAX_RETRIEVED_DOCS = int(os.getenv("MAX_RETRIEVED_DOCS", "5"))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))