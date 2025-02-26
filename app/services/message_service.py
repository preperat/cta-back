from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc

from app.models.message import Message, MessageType
from app.models.conversation import Conversation
from app.schemas.message import MessageCreate, MessageUpdate

class MessageService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, message_data: MessageCreate) -> Message:
        """Create a new message."""
        # Convert string message_type to enum if needed
        if isinstance(message_data.message_type, str):
            message_type = MessageType[message_data.message_type]
        else:
            message_type = message_data.message_type
            
        message = Message(
            content=message_data.content,
            message_type=message_type,
            conversation_id=message_data.conversation_id,
            message_metadata=message_data.message_metadata
        )
        
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_conversation_messages(
        self, conversation_id: int, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """Get all messages for a conversation."""
        # First check if conversation exists
        result = await self.db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalars().first()
        
        if not conversation:
            return []
            
        # Get messages
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .offset(skip)
            .limit(limit)
        )
        
        return result.scalars().all()

    async def get_message(self, message_id: int) -> Optional[Message]:
        """Get a specific message by ID."""
        result = await self.db.execute(
            select(Message).where(Message.id == message_id)
        )
        return result.scalars().first()

    async def update_message(
        self, message_id: int, message_data: MessageUpdate
    ) -> Optional[Message]:
        """Update a message."""
        result = await self.db.execute(
            select(Message).where(Message.id == message_id)
        )
        message = result.scalars().first()
        
        if not message:
            return None
            
        # Update fields if provided
        if message_data.content is not None:
            message.content = message_data.content
            
        if message_data.message_metadata is not None:
            message.message_metadata = message_data.message_metadata
            
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def update_message_embedding(self, message_id: int, embedding: List[float]) -> Optional[Message]:
        """Update a message's embedding."""
        result = await self.db.execute(
            select(Message).where(Message.id == message_id)
        )
        message = result.scalars().first()
        
        if not message:
            return None
            
        message.embedding = embedding
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def delete_message(self, message_id: int) -> bool:
        """Delete a message."""
        result = await self.db.execute(
            select(Message).where(Message.id == message_id)
        )
        message = result.scalars().first()
        
        if not message:
            return False
            
        await self.db.delete(message)
        await self.db.commit()
        return True 