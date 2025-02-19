from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel
from app.models.message import MessageType

class MessageBase(BaseModel):
    content: str
    message_type: MessageType

class MessageCreate(MessageBase):
    conversation_id: int
    metadata: Optional[Dict] = None

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime
    metadata: Optional[Dict] = None

    class Config:
        from_attributes = True 