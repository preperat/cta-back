from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .message import MessageResponse

class ConversationBase(BaseModel):
    title: Optional[str] = None

class ConversationCreate(ConversationBase):
    user_id: int

class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True 