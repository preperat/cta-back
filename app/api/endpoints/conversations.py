from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.core.database import get_async_session
from app.services.conversation_service import ConversationService
from app.services.ai_service import AIService
from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationUpdate, ConversationListResponse
from app.schemas.message import MessageCreate, MessageResponse
from app.models.message import MessageType
from app.db.base import get_db
from app.models.conversation import Conversation

router = APIRouter()

@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new conversation."""
    conversation_service = ConversationService(db)
    new_conversation = await conversation_service.create_conversation(conversation)
    
    # Create a response without messages to avoid lazy loading
    return {
        "id": new_conversation.id,
        "title": new_conversation.title,
        "created_at": new_conversation.created_at,
        "updated_at": new_conversation.updated_at or new_conversation.created_at,  # Fallback to created_at
        "messages": []
    }

@router.get("/", response_model=List[ConversationListResponse])
async def get_conversations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all conversations."""
    conversation_service = ConversationService(db)
    return await conversation_service.get_conversations(skip, limit)

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific conversation by ID."""
    conversation_service = ConversationService(db)
    conversation = await conversation_service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.put("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    conversation_update: ConversationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a conversation."""
    conversation_service = ConversationService(db)
    updated_conversation = await conversation_service.update_conversation(
        conversation_id, conversation_update
    )
    if not updated_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return updated_conversation

@router.delete("/{conversation_id}", response_model=dict)
async def delete_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a conversation."""
    conversation_service = ConversationService(db)
    success = await conversation_service.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"success": True, "message": "Conversation deleted"}

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

    # Convert messages to dictionaries for the AI service
    message_history = [
        {
            "message_type": msg.message_type.value,
            "content": msg.content
        }
        for msg in conversation.messages
    ]

    # Generate AI response in background
    background_tasks.add_task(
        generate_and_save_ai_response,
        conv_service,
        ai_service,
        conversation_id,
        message_history  # Use the converted message_history
    )

    return user_message

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
    """Generate AI response and save it to the database"""
    # Generate AI response
    ai_response = await ai_service.generate_response(message_history)
    
    # Create AI message
    ai_message = MessageCreate(
        content=ai_response,
        message_type="ai",
        conversation_id=conversation_id
    )
    
    # Save AI message
    await conv_service.add_message(ai_message) 