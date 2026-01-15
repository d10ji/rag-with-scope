import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Vector Database
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma")
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