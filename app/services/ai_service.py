from typing import Dict, List
import anthropic
from app.core.config import settings
from app.models.message import MessageType

class AIService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.MODEL_NAME

    async def generate_response(
        self, 
        messages: List[Dict],
        system_prompt: str | None = None
    ) -> str:
        """
        Generate AI response using the conversation history
        """
        try:
            # Convert messages to Claude format
            message_history = []
            
            if system_prompt:
                message_history.append({
                    "role": "system",
                    "content": system_prompt
                })

            for msg in messages:
                role = "assistant" if msg["message_type"] == MessageType.AI else "user"
                message_history.append({
                    "role": role,
                    "content": msg["content"]
                })

            response = await self.client.messages.create(
                model=self.model,
                messages=message_history,
                max_tokens=1000
            )

            return response.content[0].text

        except Exception as e:
            # Log the error
            print(f"Error generating AI response: {str(e)}")
            raise 