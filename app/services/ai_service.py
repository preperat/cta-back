from typing import Dict, List, Any, Optional
import anthropic
import os
import numpy as np
from app.core.config import settings
from app.models.message import MessageType

class AIService:
    def __init__(self):
        self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-opus-20240229"  # Default model

    async def generate_response(self, message_history: List[Dict[str, Any]]) -> str:
        """Generate an AI response based on conversation history."""
        # Format messages for Claude
        messages = []
        
        for msg in message_history:
            role = "user" if msg["message_type"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
        
        # Ensure the last message is from the user
        if not messages or messages[-1]["role"] == "assistant":
            raise ValueError("Last message must be from the user")
        
        try:
            response = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error generating AI response: {str(e)}")
            return "I apologize, but I encountered an error processing your request."
    
    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate vector embedding for text using Claude."""
        try:
            # This is a placeholder - Claude doesn't have a dedicated embedding API yet
            # In a real implementation, you would use OpenAI or another embedding provider
            # For now, we'll return a random vector of the right dimensionality
            
            # Simulate a 1536-dimensional embedding vector (OpenAI's standard)
            random_embedding = np.random.normal(0, 1, 1536).tolist()
            return random_embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            return None 