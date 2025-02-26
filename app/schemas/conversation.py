from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.message import MessageResponse


class ConversationBase(BaseModel):
    """Base schema for conversation data."""
    title: str = Field(..., description="Title of the conversation")


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    pass


class ConversationUpdate(BaseModel):
    """Schema for updating an existing conversation."""
    title: Optional[str] = Field(None, description="New title for the conversation")


class ConversationResponse(ConversationBase):
    """Schema for conversation response data."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: Optional[List[MessageResponse]] = []

    class Config:
        from_attributes = True 