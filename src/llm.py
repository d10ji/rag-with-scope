from groq import Groq
from typing import List, Dict, Any
from config import Config


class LLMProvider:
    def __init__(self, provider: str = None):
        if provider is None:
            provider = Config.LLM_PROVIDER
        
        self.provider = provider
        
        if provider == "groq":
            self.model = Config.GROQ_MODEL
            self.client = Groq(api_key=Config.GROQ_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}. Only 'groq' is supported.")
    
    def generate_response(self, prompt: str, context: List[str] = None) -> str:
        """Generate a response from the LLM"""
        if context:
            context_str = "\n".join(context)
            full_prompt = f"""Context:
{context_str}

Question: {prompt}

Answer based on the context provided above. If the context doesn't contain enough information, say so."""
        else:
            full_prompt = prompt
        
        return self._generate_groq(full_prompt)
    
    def _generate_groq(self, prompt: str) -> str:
        """Generate response using Groq"""
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        return chat_completion.choices[0].message.content
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "provider": self.provider,
            "model": self.model,
            "type": "api"
        }