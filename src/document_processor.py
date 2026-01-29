from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from typing import List, Dict, Any, Optional
import os
from config import Config


class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
        )
    
    def load_document(self, file_path: str) -> List[Document]:
        """Load a document from file path"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_extension in ['.txt', '.md']:
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        return loader.load()
    
    def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        """Load and split a document into chunks"""
        documents = self.load_document(file_path)
        chunks = self.text_splitter.split_documents(documents)
        
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            processed_chunks.append({
                "content": chunk.page_content,
                "metadata": {
                    **chunk.metadata,
                    "source_file": file_path,
                    "source": os.path.basename(file_path),  # Add filename as source
                    "chunk_id": i,
                    "total_chunks": len(chunks)  # Add total chunk count
                }
            })
        
        return processed_chunks
    
    def process_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Process raw text into chunks"""
        if metadata is None:
            metadata = {}
        
        document = Document(page_content=text, metadata=metadata)
        chunks = self.text_splitter.split_documents([document])
        
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            processed_chunks.append({
                "content": chunk.page_content,
                "metadata": {
                    **chunk.metadata,
                    "chunk_id": i,
                    "total_chunks": len(chunks),  # Add total chunk count
                    "source": metadata.get('source', f"Custom Text {i+1}") if metadata else f"Custom Text {i+1}"
                }
            })
        
        return processed_chunks
    
    def process_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Process all supported documents in a directory"""
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        all_chunks = []
        supported_extensions = ['.pdf', '.txt', '.md']
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(filename)[1].lower()
                if file_extension in supported_extensions:
                    try:
                        chunks = self.process_document(file_path)
                        all_chunks.extend(chunks)
                        print(f"Processed {filename}: {len(chunks)} chunks")
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")
        
        return all_chunks