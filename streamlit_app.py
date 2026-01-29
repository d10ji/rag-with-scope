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
    
    /* Source card styling */
    .source-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 1px solid #dee2e6;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .source-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Match indicator styling */
    .match-high { color: #28a745; font-weight: bold; }
    .match-medium { color: #ffc107; font-weight: bold; }
    .match-low { color: #dc3545; font-weight: bold; }
    
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
        # Show warning and confirmation
        st.warning("⚠️ **WARNING**: This will permanently delete ALL documents from the database!")
        st.info("📋 What will happen:")
        st.markdown("- 🗑️ All uploaded documents will be deleted")
        st.markdown("- 📄 Document count will reset to 0") 
        st.markdown("- 🔄 Fresh empty database will be created")
        st.markdown("- 📝 Upload history will be cleared")
        
        # Add a small delay for user to see the warning
        import time
        time.sleep(2)
        
        with st.spinner("🗑️ Resetting database to fresh state..."):
            logger.info("Starting database reset...")
            import subprocess
            result = subprocess.run(
                ['python', 'manage_db.py', 'rebuild'],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            if result.returncode == 0:
                logger.info("Database reset successfully!")
                st.success("✅ Database has been reset to empty state!")
                st.info("📊 Database is now ready for fresh document uploads.")
                
                # Clear upload tracking after reset
                st.session_state.uploaded_files = []
                st.session_state.added_texts = []
                
                # Show success details
                if result.stdout:
                    st.markdown("**Reset Details:**")
                    st.code(result.stdout)
                
                time.sleep(2)  # Brief pause to show success
                st.rerun()
            else:
                error_msg = f"Database reset error: {result.stderr}"
                logger.error(error_msg)
                st.error(f"❌ {error_msg}")
    except Exception as e:
        error_msg = f"Error resetting database: {e}"
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

# Simple header with environment indicator
env_icon = "🔧" if Config.IS_DEVELOPMENT else "☁️"
env_text = "Local" if Config.IS_DEVELOPMENT else "Cloud"
st.markdown(f"# 🤖 RAG System {env_icon}")
st.markdown(f"Chat with your documents using AI ({env_text} Milvus)")

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
            chunk_count = info['vector_db']['document_count']
            unique_docs = st.session_state.rag_pipeline.get_unique_documents()
            unique_doc_count = len(unique_docs)
            logger.info(f"System status checked - {unique_doc_count} unique documents ({chunk_count} chunks) in database")
            
            # Environment indicator
            env_icon = "🔧" if Config.IS_DEVELOPMENT else "☁️"
            env_text = "Local" if Config.IS_DEVELOPMENT else "Cloud"
            db_connection = f"{env_icon} {env_text} Milvus"
            
            # Small metrics with much smaller font sizes
            st.markdown("### 📊 Status")
            
            # Document count with very small display
            st.metric(
                "Docs", 
                str(unique_doc_count),
                delta=None,
                help="Total unique documents in system"
            )
            
            # Environment indicator
            st.markdown(f"**Database:** {db_connection}")
            
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
        if st.button("🗑️ Reset Database", use_container_width=True, 
                    help="⚠️ This will delete ALL documents and create a fresh empty database"):
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
        col1, col2 = st.columns([4, 1])
        with col1:
            message_count = len(st.session_state.messages)
            st.markdown(f"### Ask questions about your documents ({message_count} messages)")
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        # Chat input at the top (fixed position)
        user_query = st.chat_input("Type your question here...")
        
        # Process new query immediately (if any)
        if user_query:
            logger.info(f"User query: {user_query[:100]}...")
            
            # Display user question
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)
            
            # Display assistant response below (ChatGPT style)
            with st.chat_message("assistant"):
                with st.spinner("Searching..."):
                    try:
                        result = st.session_state.rag_pipeline.query(user_query, max_results=5)
                        response_text = result.get("answer", "No response found")
                        logger.info(f"Generated response: {len(response_text)} chars")
                        st.markdown(response_text)
                        
                        # Show sources with single collapsible containing all sources
                        if result.get("sources"):
                            with st.expander(f"📚 Sources ({len(result['sources'])} chunks)", expanded=False):
                                for i, source in enumerate(result["sources"], 1):
                                    metadata = source.get('metadata', {})
                                    
                                    # Extract document name
                                    doc_name = metadata.get('source', 'Unknown Document')
                                    if '/' in doc_name:
                                        doc_name = doc_name.split('/')[-1]
                                    
                                    # Extract chunk info
                                    chunk_id = metadata.get('chunk_id', i-1)
                                    
                                    # Calculate match percentage
                                    distance = source.get('distance')
                                    if distance is not None:
                                        match_percent = f"{(1 - distance) * 100:.0f}%"
                                        match_color = "🟢" if (1 - distance) > 0.8 else "🟡" if (1 - distance) > 0.6 else "🔴"
                                    else:
                                        match_percent = "N/A"
                                        match_color = "⚪"
                                    
# Get preview with interactive design
                                    content = source.get('content', '')
                                    if content:
                                        words = content.split()[:30]
                                        preview = ' '.join(words)
                                        if len(content) > len(preview):
                                            preview += "..."
                                    else:
                                        preview = "No content available"
                                    
                                    # Modern card design with interactive elements
                                    match_value = (1 - distance) * 100 if distance is not None else 0
                                    
                                    # Color scheme based on match
                                    if match_value > 80:
                                        bg_color = "#d4edda"
                                        border_color = "#28a745"
                                        match_color = "#155724"
                                        match_bg = "#28a745"
                                    elif match_value > 60:
                                        bg_color = "#fff3cd"
                                        border_color = "#ffc107"
                                        match_color = "#856404"
                                        match_bg = "#ffc107"
                                    else:
                                        bg_color = "#f8d7da"
                                        border_color = "#dc3545"
                                        match_color = "#721c24"
                                        match_bg = "#dc3545"
                                    
                                    # Interactive card
                                    st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, {bg_color} 0%, rgba(255,255,255,0.95) 100%); 
                                               border-left: 4px solid {border_color}; 
                                               border-radius: 8px; 
                                               padding: 12px 16px; 
                                               margin: 8px 0; 
                                               box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                                               transition: all 0.3s ease;
                                               cursor: pointer;
                                               position: relative;
                                               overflow: hidden;'>
                                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                                            <div style='display: flex; align-items: center; gap: 8px;'>
                                                <div style='font-size: 16px;'>📄</div>
                                                <div>
                                                    <div style='font-weight: 600; font-size: 14px; color: #333; margin-bottom: 2px;'>{doc_name}</div>
                                                    <div style='font-size: 12px; color: #666;'>Chunk {chunk_id + 1}</div>
                                                </div>
                                            </div>
                                            <div style='text-align: right;'>
                                                <div style='background: {match_bg}; color: white; 
                                                           padding: 4px 8px; 
                                                           border-radius: 12px; 
                                                           font-size: 12px; 
                                                           font-weight: 600;
                                                           display: inline-block;'>
                                                    {match_percent} Match
                                                </div>
                                            </div>
                                        </div>
                                        <div style='font-size: 13px; color: #444; line-height: 1.5; 
                                                   border-top: 1px solid rgba(0,0,0,0.06); 
                                                   padding-top: 8px; 
                                                   margin-top: 8px;'>
                                            {preview}
                                        </div>
                                        <div style='position: absolute; top: 8px; right: 16px; 
                                                   font-size: 10px; color: {border_color}; 
                                                   font-weight: 600;'>#{i}</div>
                                    </div>
                                    <style>
                                        .source-card:hover {{
                                            transform: translateY(-2px);
                                            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
                                            border-left-width: 6px;
                                        }}
                                    </style>
                                    """, unsafe_allow_html=True)
                        
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                        
                    except Exception as e:
                        error_msg = f"Query error: {e}"
                        logger.error(error_msg)
                        st.error(f"Error: {e}")
        
        # Chat history below input (display in chronological order - newest Q&A pairs at bottom)
        if st.session_state.messages:
            st.markdown("---")
            st.markdown("### 💬 Chat History")
            
            # Group messages into Q&A pairs
            for i in range(0, len(st.session_state.messages), 2):
                # User question
                if i < len(st.session_state.messages):
                    user_msg = st.session_state.messages[i]
                    with st.chat_message("user"):
                        st.markdown(user_msg["content"])
                
                # Assistant answer
                if i + 1 < len(st.session_state.messages):
                    assistant_msg = st.session_state.messages[i + 1]
                    with st.chat_message("assistant"):
                        # Only show answer content, sources appear in real-time response
                        st.markdown(assistant_msg["content"])
                    
                    # Add separator between Q&A pairs (but not after last pair)
                    if i + 2 < len(st.session_state.messages):
                        st.markdown("<hr style='margin: 15px 0; border-top: 1px solid #e1e5e9;'>", unsafe_allow_html=True)
        
    with tab2:
        # Document List at the top
        st.markdown("## 📚 All Documents in System")
        try:
            unique_docs = st.session_state.rag_pipeline.get_unique_documents()
            if unique_docs:
                st.markdown(f"**Total Documents:** {len(unique_docs)}")
                
                # Show documents in expandable sections
                with st.expander("📄 View All Documents", expanded=False):
                    for i, doc in enumerate(unique_docs, 1):
                        st.markdown(f"### {i}. {doc['source']}")
                        
                        # Show metadata if available
                        if doc['metadata']:
                            metadata_str = ", ".join([f"{k}: {v}" for k, v in doc['metadata'].items()])
                            if metadata_str:
                                st.markdown(f"*Metadata: {metadata_str}*")
                        
                        # Show chunk count
                        st.markdown(f"**Chunks:** {doc['total_chunks']}")
                        
                        # Show preview of first chunk content
                        if doc['chunks']:
                            first_chunk = doc['chunks'][0]['content']
                            content_preview = first_chunk[:300].replace('\n', ' ')
                            if len(first_chunk) > 300:
                                content_preview += "..."
                            st.markdown(f"**Preview:** {content_preview}")
                        
                        if i < len(unique_docs):
                            st.divider()
            else:
                st.info("📄 **Database is empty** - No documents in the system yet.")
                st.markdown("### 🚀 Get Started:")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("📄 **Upload documents** using the form below")
                    st.markdown("📝 **Add custom text** to test the system")
                with col2:
                    st.markdown("💬 **Start chatting** once you have documents")
                    st.markdown("🔄 **Reset database** using the button in the sidebar")
        except Exception as e:
            logger.error(f"Error loading document list: {e}")
            st.error(f"Error loading documents: {e}")
        
        st.markdown("---")
        
        # Main content and sidebar layout
        main_col, sidebar_col = st.columns([3, 1])
        
        with main_col:
            st.markdown("### 📄 Document Upload")
            
            uploaded_files = st.file_uploader(
                "Choose files (PDF, TXT, MD)",
                type=["pdf", "txt", "md"],
                accept_multiple_files=True,
                help="Upload multiple documents to add to the RAG system"
            )
            
            if uploaded_files:
                st.markdown(f"**Selected {len(uploaded_files)} file(s):**")
                for uploaded_file in uploaded_files:
                    st.markdown(f"📄 {uploaded_file.name}")
                
                if st.button("📤 Upload Documents", use_container_width=True):
                    total_chunks = 0
                    successful_uploads = []
                    failed_uploads = []
                    
                    try:
                        progress_bar = st.progress(0, text=f"Processing {len(uploaded_files)} files...")
                        
                        for i, uploaded_file in enumerate(uploaded_files):
                            progress_bar.progress((i + 1) / len(uploaded_files), text=f"Processing {uploaded_file.name}...")
                            
                            try:
                                temp_path = f"/tmp/{uploaded_file.name}"
                                with open(temp_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                
                                chunk_count = st.session_state.rag_pipeline.ingest_document(temp_path)
                                log_document_upload(uploaded_file.name, chunk_count, "file")
                                
                                successful_uploads.append({
                                    "name": uploaded_file.name,
                                    "chunks": chunk_count
                                })
                                total_chunks += chunk_count
                                
                                # Clean up temp file
                                os.remove(temp_path)
                                
                            except Exception as file_error:
                                failed_uploads.append({
                                    "name": uploaded_file.name,
                                    "error": str(file_error)
                                })
                                logger.error(f"Failed to upload {uploaded_file.name}: {file_error}")
                        
                        progress_bar.empty()
                        
                        # Show results
                        if successful_uploads:
                            st.success(f"✅ Successfully uploaded {len(successful_uploads)} files ({total_chunks} total chunks)")
                            for upload in successful_uploads:
                                st.markdown(f"✅ {upload['name']} ({upload['chunks']} chunks)")
                        
                        if failed_uploads:
                            st.error(f"❌ Failed to upload {len(failed_uploads)} files:")
                            for upload in failed_uploads:
                                st.markdown(f"❌ {upload['name']}: {upload['error']}")
                        
                        if successful_uploads:
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
                unique_docs = st.session_state.rag_pipeline.get_unique_documents()
                unique_doc_count = len(unique_docs)
                chunk_count = info['vector_db']['document_count']
                
                st.metric("Total Docs", str(unique_doc_count))
                st.markdown(f"*{chunk_count} total chunks*")
                
                st.markdown("### System Info")
                st.markdown(f"**Collection:** {info['vector_db']['name']}")
                model_name = info['embedding_model']['model_name'].split('/')[-1]
                st.markdown(f"**Model:** {model_name}")
                
                if unique_doc_count == 0:
                    st.info("📄 No documents yet")
                    
            except Exception as e:
                st.error(f"Error: {e}")

# Simple footer
st.markdown("---")
st.markdown("<center><small>🤖 RAG System | Simple Document Chat</small></center>", unsafe_allow_html=True)