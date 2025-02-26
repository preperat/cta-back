from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationCreate, ConversationUpdate
from app.schemas.message import MessageCreate

class ConversationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation."""
        from datetime import datetime
        now = datetime.utcnow()
        
        conversation = Conversation(
            title=conversation_data.title,
            created_at=now,
            updated_at=now
        )
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def get_conversations(self, skip: int = 0, limit: int = 100) -> List[Conversation]:
        """Get all conversations."""
        result = await self.db.execute(
            select(Conversation)
            .offset(skip)
            .limit(limit)
            .order_by(Conversation.created_at.desc())
        )
        return result.scalars().all()

    async def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """Get a specific conversation by ID with its messages."""
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .options(selectinload(Conversation.messages))
        )
        conversation = result.scalars().first()
        
        # If conversation exists, ensure messages are loaded
        if conversation:
            # Force loading of messages to avoid lazy loading issues
            _ = conversation.messages
        
        return conversation

    async def update_conversation(
        self, conversation_id: int, conversation_data: ConversationUpdate
    ) -> Optional[Conversation]:
        """Update a conversation."""
        result = await self.db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalars().first()
        
        if not conversation:
            return None
            
        # Update fields if provided
        if conversation_data.title is not None:
            conversation.title = conversation_data.title
            
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def delete_conversation(self, conversation_id: int) -> bool:
        """Delete a conversation."""
        result = await self.db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalars().first()
        
        if not conversation:
            return False
            
        await self.db.delete(conversation)
        await self.db.commit()
        return True

    async def add_message(self, data: MessageCreate) -> Message:
        """Add a message to a conversation"""
        message = Message(**data.model_dump())
        self.db.add(message)
        await self.db.commit()
        return message 