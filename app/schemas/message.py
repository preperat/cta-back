from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.message import MessageType

class MessageBase(BaseModel):
    """Base schema for message data."""
    content: str = Field(..., description="Content of the message")
    message_type: MessageType = Field(..., description="Type of message (user/ai/system)")

class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    conversation_id: int = Field(..., description="ID of the conversation this message belongs to")
    message_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the message")

class MessageUpdate(BaseModel):
    """Schema for updating an existing message."""
    content: Optional[str] = Field(None, description="Updated content of the message")
    message_metadata: Optional[Dict[str, Any]] = Field(None, description="Updated metadata for the message")

class MessageResponse(MessageBase):
    """Schema for message response data."""
    id: int
    conversation_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    message_metadata: Optional[Dict[str, Any]] = None
    embedding: Optional[List[float]] = None

    class Config:
        from_attributes = True 