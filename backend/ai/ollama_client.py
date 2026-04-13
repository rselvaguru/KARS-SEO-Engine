"""
Ollama Client for local LLM interaction
Connects to local Ollama service running on PORT 11434
"""

import requests
import logging
from typing import Optional
import os

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = None, model: str = None):
        """
        Initialize Ollama client
        
        Args:
            base_url: Ollama API base URL (default: http://localhost:11434)
            model: Model name to use (default: phi)
        """
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "phi")
        self.endpoint = f"{self.base_url}/api/generate"
    
    def generate_text(self, prompt: str, system: str = None) -> Optional[str]:
        """
        Generate text using Ollama
        
        Args:
            prompt: The input prompt
            system: Optional system prompt
            
        Returns:
            Generated text response or None if error
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
            }
            
            if system:
                payload["system"] = system
            
            headers = {"Content-Type": "application/json"}
            
            logger.info(f"Calling Ollama API with model: {self.model}")
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=120  # 2 minute timeout for generation
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "").strip()
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Ollama. Ensure Ollama is running on localhost:11434")
            return None
        except Exception as e:
            logger.error(f"Error calling Ollama: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        """Check if Ollama service is available"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# Global client instance
ollama_client = OllamaClient()
