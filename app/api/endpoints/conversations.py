from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_async_session
from app.services.conversation_service import ConversationService
from app.services.ai_service import AIService
from app.schemas.conversation import ConversationCreate, ConversationResponse
from app.schemas.message import MessageCreate, MessageResponse
from app.models.message import MessageType
from app.db.base import get_db
from app.models.conversation import Conversation

router = APIRouter()

@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    data: ConversationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new conversation"""
    service = ConversationService(session)
    return await service.create_conversation(data)

@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def add_message(
    conversation_id: int,
    message: MessageCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session)
):
    """Add a message and generate AI response"""
    conv_service = ConversationService(session)
    ai_service = AIService()

    # Save user message
    user_message = await conv_service.add_message(message)

    # Get conversation history
    conversation = await conv_service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Generate AI response in background
    background_tasks.add_task(
        generate_and_save_ai_response,
        conv_service,
        ai_service,
        conversation_id,
        [msg.to_dict() for msg in conversation.messages]
    )

    return user_message

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Get a conversation and its messages"""
    service = ConversationService(session)
    conversation = await service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.get("/", response_model=List[dict])
async def get_conversations(db: AsyncSession = Depends(get_db)):
    """Get all conversations"""
    result = await db.execute(select(Conversation))
    conversations = result.scalars().all()
    return [{"id": c.id, "title": c.title, "created_at": c.created_at} for c in conversations]

@router.post("/", response_model=dict)
async def create_conversation(title: str, db: AsyncSession = Depends(get_db)):
    """Create a new conversation"""
    conversation = Conversation(title=title)
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return {"id": conversation.id, "title": conversation.title, "created_at": conversation.created_at}

async def generate_and_save_ai_response(
    conv_service: ConversationService,
    ai_service: AIService,
    conversation_id: int,
    message_history: List[dict]
):
    """Background task to generate and save AI response"""
    try:
        # Generate AI response
        ai_response = await ai_service.generate_response(message_history)

        # Save AI response
        await conv_service.add_message(MessageCreate(
            conversation_id=conversation_id,
            content=ai_response,
            message_type=MessageType.AI
        ))
    except Exception as e:
        # Log the error
        print(f"Error in background AI task: {str(e)}") 