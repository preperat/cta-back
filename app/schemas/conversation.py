from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.message import MessageResponse


class ConversationBase(BaseModel):
    """Base schema for conversation data."""
    title: str = Field(..., description="The title of the conversation")


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    pass


class ConversationUpdate(BaseModel):
    """Schema for updating an existing conversation."""
    title: Optional[str] = Field(None, description="The title of the conversation")


class ConversationResponse(ConversationBase):
    """Schema for conversation response data."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[MessageResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
        populate_by_name = True


class ConversationListResponse(ConversationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True 