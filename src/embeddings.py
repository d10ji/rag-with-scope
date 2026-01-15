from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np
from config import Config


class EmbeddingModel:
    def __init__(self, model_name: Optional[str] = None):
        if model_name is None:
            model_name = Config.EMBEDDING_MODEL
        
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts into embeddings"""
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        return embeddings
    
    def encode_single(self, text: str) -> np.ndarray:
        """Encode a single text into embedding"""
        return self.model.encode(text, convert_to_numpy=True)
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        dim = self.model.get_sentence_embedding_dimension()
        return int(dim) if dim is not None else 0
    
    def get_model_info(self) -> dict:
        """Get information about the model"""
        return {
            "model_name": self.model_name,
            "embedding_dimension": self.get_embedding_dimension(),
            "max_sequence_length": self.model.max_seq_length
        }