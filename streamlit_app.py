#!/usr/bin/env python3
"""
Streamlit Web Interface for Simple RAG System - Clean & Simple with Logging
"""

import streamlit as st
import sys
import os
import logging
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.rag_pipeline import RAGPipeline
from config import Config

# Simple console logging
import logging

# Configure simple logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="RAG System",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean and compact
st.markdown("""
<style>
    /* General styling */
    .stApp {
        font-size: 12px !important;
    }
    
    /* Headers */
    h1 {
        font-size: 1.5rem !important;
        color: #1f77b4 !important;
    }
    
    h2 {
        font-size: 1.0rem !important;
    }
    
    h3 {
        font-size: 0.9rem !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        padding: 1rem !important;
    }
    
    /* Buttons */
    .stButton button {
        font-size: 11px !important;
        padding: 0.3rem 0.6rem !important;
    }
    
    /* File uploader */
    .stFileUploader {
        font-size: 11px !important;
    }
    
    /* Text area */
    .stTextArea textarea {
        font-size: 12px !important;
    }
    
    /* Success/error messages */
    .stAlert {
        font-size: 11px !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        font-size: 12px !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-size: 11px !important;
    }
    
    /* Fix metric container sizes - VERY SMALL */
    .metric-container {
        font-size: 9px !important;
        padding: 0.3rem !important;
        min-height: 50px !important;
    }
    
    .metric-container div[data-testid="metric-container"] > div > div > div {
        font-size: 14px !important;
        line-height: 1.0 !important;
        margin-bottom: 0px !important;
    }
    
    .metric-container div[data-testid="metric-container"] > div > div > div > div {
        font-size: 8px !important;
        margin-top: 0px !important;
    }
    
    /* Target all metric text specifically */
    .css-1e5zngp, .css-1tj3f16 {
        font-size: 8px !important;
    }
    
    /* Even smaller for collection name */
    .css-1w6e33s {
        font-size: 7px !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-size: 13px !important;
    }
    
    /* Success/error messages */
    .stAlert {
        font-size: 13px !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        font-size: 14px !important;
    }
    
    /* Clean box styling */
    .info-box {
        background-color: #f8f9fa;
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 0.3rem 0;
        font-size: 13px;
    }
    
    /* Sidebar content */
    .sidebar-content {
        font-size: 12px !important;
    }
    
    /* Upload tracking section */
    .upload-tracking {
        background-color: #e8f4fd;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .instruction-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "rag_initialized" not in st.session_state:
    st.session_state.rag_initialized = False
    logger.info("RAG System session started - Not initialized")

if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "added_texts" not in st.session_state:
    st.session_state.added_texts = []

# Function to initialize RAG system
def initialize_rag_system():
    try:
        with st.spinner("Initializing..."):
            logger.info("Starting RAG System initialization...")
            st.session_state.rag_pipeline = RAGPipeline()
            st.session_state.rag_initialized = True
            logger.info("RAG System initialized successfully!")
            st.success("✅ System ready!")
            st.rerun()
    except Exception as e:
        error_msg = f"Failed to initialize RAG System: {e}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        st.session_state.rag_initialized = False

# Function to rebuild database
def rebuild_database():
    try:
        with st.spinner("Rebuilding database..."):
            logger.info("Starting database rebuild...")
            import subprocess
            result = subprocess.run(
                ['python', 'manage_db.py', 'rebuild'],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            if result.returncode == 0:
                logger.info("Database rebuilt successfully!")
                st.success("✅ Database rebuilt!")
                # Clear upload tracking after rebuild
                st.session_state.uploaded_files = []
                st.session_state.added_texts = []
                st.rerun()
            else:
                error_msg = f"Database rebuild error: {result.stderr}"
                logger.error(error_msg)
                st.error(f"❌ {error_msg}")
    except Exception as e:
        error_msg = f"Error rebuilding database: {e}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")

# Function to log document upload
def log_document_upload(filename, chunk_count, file_type="file"):
    log_msg = f"Document {file_type} uploaded: {filename} ({chunk_count} chunks)"
    logger.info(log_msg)
    
    if file_type == "file":
        st.session_state.uploaded_files.append({
            "name": filename,
            "chunks": chunk_count,
            "time": datetime.now().strftime("%H:%M:%S")
        })
    else:
        st.session_state.added_texts.append({
            "name": filename if filename else f"Custom Text {len(st.session_state.added_texts)+1}",
            "chunks": chunk_count,
            "time": datetime.now().strftime("%H:%M:%S")
        })

# Simple header
st.markdown("# 🤖 RAG System")
st.markdown("Chat with your documents using AI")

# Sidebar with minimal info and controls
with st.sidebar:
    st.markdown("## ⚙️ System")
    
    # Initialize button (always visible)
    if not st.session_state.rag_initialized:
        st.markdown("### System Status")
        st.markdown('<div class="info-box">🔴 Not initialized</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Initialize System", use_container_width=True, type="primary"):
            initialize_rag_system()
    
    else:
        # System is initialized - show minimal info
        st.markdown('<div class="info-box">🟢 System Ready</div>', unsafe_allow_html=True)
        
        try:
            info = st.session_state.rag_pipeline.get_system_info()
            doc_count = info['vector_db']['document_count']
            logger.info(f"System status checked - {doc_count} documents in database")
            
            # Small metrics with much smaller font sizes
            st.markdown("### 📊 Status")
            
            # Document count with very small display
            st.metric(
                "Docs", 
                str(doc_count),
                delta=None,
                help="Total document chunks in system"
            )
            
            # Model info (compact)
            model_name = info['embedding_model']['model_name'].split('/')[-1]
            st.markdown(f"**Model:** `{model_name}`")
            st.markdown(f"**LLM:** `{info['llm']['model']}`")
            
        except Exception as e:
            error_msg = f"Status check error: {e}"
            logger.error(error_msg)
            st.error(error_msg)
        
        st.markdown("---")
        
        # Action buttons
        st.markdown("### 🔧 Actions")
        if st.button("🗄️ Rebuild Database", use_container_width=True):
            rebuild_database()
        
        if st.button("🔄 Reinitialize", use_container_width=True):
            logger.info("System reinitialization requested")
            st.session_state.rag_initialized = False
            st.session_state.rag_pipeline = None
            st.session_state.uploaded_files = []
            st.session_state.added_texts = []
            st.rerun()

# Main content area
if st.session_state.rag_initialized:
    # Main tabs
    tab1, tab2 = st.tabs(["💬 Chat", "📚 Documents"])

    with tab1:
        st.markdown("### Ask questions about your documents")
        
        # Chat history (compact)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        user_query = st.chat_input("Type your question here...")
        
        if user_query:
            logger.info(f"User query: {user_query[:100]}...")
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)
            
            with st.chat_message("assistant"):
                with st.spinner("Searching..."):
                    try:
                        result = st.session_state.rag_pipeline.query(user_query, max_results=5)
                        response_text = result.get("answer", "No response found")
                        logger.info(f"Generated response: {len(response_text)} chars")
                        st.markdown(response_text)
                        
                        # Show sources (compact)
                        if result.get("sources"):
                            with st.expander("📖 Sources"):
                                for i, source in enumerate(result["sources"], 1):
                                    st.markdown(f"**Source {i}:**")
                                    st.markdown(f"{source.get('content', '')[:200]}...")
                                    st.divider()
                        
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                        
                    except Exception as e:
                        error_msg = f"Query error: {e}"
                        logger.error(error_msg)
                        st.error(f"Error: {e}")

    with tab2:
        # Main content and sidebar layout
        main_col, sidebar_col = st.columns([3, 1])
        
        with main_col:
            st.markdown("### 📄 Document Upload")
            
            uploaded_file = st.file_uploader(
                "Choose a file (PDF, TXT, MD)",
                type=["pdf", "txt", "md"],
                help="Upload documents to add to the RAG system"
            )
            
            if uploaded_file is not None:
                if st.button("📤 Upload Document", use_container_width=True):
                    try:
                        with st.spinner(f"Processing {uploaded_file.name}..."):
                            temp_path = f"/tmp/{uploaded_file.name}"
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            chunk_count = st.session_state.rag_pipeline.ingest_document(temp_path)
                            log_document_upload(uploaded_file.name, chunk_count, "file")
                            
                            st.success(f"✅ {uploaded_file.name} uploaded ({chunk_count} chunks)")
                            st.rerun()
                    except Exception as e:
                        error_msg = f"Upload error: {e}"
                        logger.error(error_msg)
                        st.error(f"❌ {error_msg}")
            
            st.markdown("---")
            st.markdown("### 📝 Add Custom Text")
            
            custom_text = st.text_area("Enter text to add:", height=120)
            
            if st.button("📝 Add Text", use_container_width=True):
                if custom_text.strip():
                    try:
                        with st.spinner("Adding text..."):
                            chunk_count = st.session_state.rag_pipeline.ingest_text(custom_text)
                            log_document_upload("Custom Text", chunk_count, "text")
                            
                            st.success(f"✅ Text added ({chunk_count} chunks)")
                            st.rerun()
                    except Exception as e:
                        error_msg = f"Text addition error: {e}"
                        logger.error(error_msg)
                        st.error(f"❌ {error_msg}")
                else:
                    st.warning("Please enter some text")
        
        with sidebar_col:
            st.markdown("## 📋 Information")
            
            # Upload tracking
            st.markdown("### Recent Uploads")
            
            if st.session_state.uploaded_files:
                for i, file_info in enumerate(st.session_state.uploaded_files[-5:], 1):  # Show last 5
                    st.markdown(f"**{file_info['name']}**")
                    st.markdown(f"*{file_info['chunks']} chunks*")
                    st.markdown(f"*{file_info['time']}*")
                    st.divider()
            else:
                st.markdown("*No files uploaded yet*")
            
            if st.session_state.added_texts:
                st.markdown("### Text Added")
                for i, text_info in enumerate(st.session_state.added_texts[-3:], 1):  # Show last 3
                    st.markdown(f"**{text_info['name']}**")
                    st.markdown(f"*{text_info['chunks']} chunks*")
                    st.markdown(f"*{text_info['time']}*")
                    st.divider()
            
            # Database Statistics
            st.markdown("### 📊 Statistics")
            try:
                info = st.session_state.rag_pipeline.get_system_info()
                doc_count = info['vector_db']['document_count']
                
                st.metric("Total Docs", str(doc_count))
                
                st.markdown("### System Info")
                st.markdown(f"**Collection:** {info['vector_db']['name']}")
                model_name = info['embedding_model']['model_name'].split('/')[-1]
                st.markdown(f"**Model:** {model_name}")
                
                if doc_count == 0:
                    st.info("📄 No documents yet")
                    
            except Exception as e:
                st.error(f"Error: {e}")

else:
    # Show welcome message when not initialized
    st.markdown("### 🚀 Welcome to RAG System")
    
    st.markdown('<div class="info-box">Please initialize the system from the sidebar to begin using the RAG System.</div>', unsafe_allow_html=True)
    
    st.markdown("### After initialization, you can:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- 📄 Upload documents")
        st.markdown("- 💬 Chat with documents")
    with col2:
        st.markdown("- 📝 Add custom text")
        st.markdown("- 🗄️ Rebuild database")

# Simple footer
st.markdown("---")
st.markdown("<center><small>🤖 RAG System | Simple Document Chat</small></center>", unsafe_allow_html=True)