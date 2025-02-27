from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class MessageType(PyEnum):
    USER = "user"
    AI = "ai"
    SYSTEM = "system"


class Message(Base):
    """
    Individual message within a conversation
    Tracks message type, content, and metadata
    """

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    content = Column(String, nullable=False)
    message_type = Column(Enum(MessageType), nullable=False)
    embedding = Column(ARRAY(FLOAT(precision=6)), nullable=True)  # Vector storage
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    message_metadata = Column(JSON, nullable=True)

    conversation = relationship("Conversation", back_populates="messages")
