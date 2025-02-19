from sqlalchemy.ext.asyncio import AsyncSession
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationCreate
from app.schemas.message import MessageCreate

class ConversationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_conversation(self, data: ConversationCreate) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(**data.model_dump())
        self.session.add(conversation)
        await self.session.commit()
        return conversation

    async def add_message(self, data: MessageCreate) -> Message:
        """Add a message to a conversation"""
        message = Message(**data.model_dump())
        self.session.add(message)
        await self.session.commit()
        return message

    async def get_conversation(self, conversation_id: int) -> Conversation | None:
        """Get conversation by ID"""
        return await self.session.get(Conversation, conversation_id) 