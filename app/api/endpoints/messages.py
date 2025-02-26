from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.message import MessageCreate, MessageResponse, MessageUpdate
from app.services.message_service import MessageService
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def create_message(
    conversation_id: int = Path(..., description="The ID of the conversation"),
    message: MessageCreate = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a new message in a conversation and get AI response."""
    message_service = MessageService(db)
    ai_service = AIService()
    
    # Ensure the message is associated with the correct conversation
    if message.conversation_id != conversation_id:
        raise HTTPException(
            status_code=400, 
            detail="Message conversation_id does not match URL conversation_id"
        )
    
    # Create the user message
    user_message = await message_service.create_message(message)
    
    # Get conversation history for context
    messages = await message_service.get_conversation_messages(conversation_id)
    
    # Format messages for AI service
    message_history = [
        {
            "message_type": msg.message_type.value,
            "content": msg.content
        }
        for msg in messages
    ]
    
    # Generate AI response
    ai_response_text = await ai_service.generate_response(message_history)
    
    # Create AI message in database
    ai_message_data = MessageCreate(
        content=ai_response_text,
        message_type="AI",
        conversation_id=conversation_id
    )
    ai_message = await message_service.create_message(ai_message_data)
    
    # Generate embedding for the message (async background task)
    # This could be moved to a background task with FastAPI
    embedding = await ai_service.generate_embedding(user_message.content)
    if embedding:
        await message_service.update_message_embedding(user_message.id, embedding)
    
    return ai_message

@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all messages for a conversation."""
    message_service = MessageService(db)
    messages = await message_service.get_conversation_messages(
        conversation_id, skip, limit
    )
    return messages

@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific message by ID."""
    message_service = MessageService(db)
    message = await message_service.get_message(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.put("/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: int,
    message_update: MessageUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a message."""
    message_service = MessageService(db)
    updated_message = await message_service.update_message(message_id, message_update)
    if not updated_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated_message

@router.delete("/messages/{message_id}", response_model=dict)
async def delete_message(
    message_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a message."""
    message_service = MessageService(db)
    success = await message_service.delete_message(message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"success": True, "message": "Message deleted"} 