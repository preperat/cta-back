#!/usr/bin/env python
"""Script to test database operations with our models."""
import asyncio
import sys
from datetime import datetime

sys.path.append(".")  # Add current directory to path

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.base import AsyncSessionLocal
from app.models.conversation import Conversation
from app.models.message import Message, MessageType


async def test_create_conversation():
    """Test creating a conversation and messages."""
    async with AsyncSessionLocal() as session:
        # Create a new conversation
        conversation = Conversation(title="Test Conversation")
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        
        print(f"✅ Created conversation: id={conversation.id}, title={conversation.title}")
        
        # Add a user message
        user_message = Message(
            conversation_id=conversation.id,
            content="Hello, this is a test message",
            message_type=MessageType.USER
        )
        session.add(user_message)
        
        # Add an AI response
        ai_message = Message(
            conversation_id=conversation.id,
            content="Hello! I'm an AI assistant. How can I help you today?",
            message_type=MessageType.AI
        )
        session.add(ai_message)
        
        await session.commit()
        print(f"✅ Added messages to conversation {conversation.id}")
        
        return conversation.id


async def test_retrieve_conversation(conversation_id):
    """Test retrieving a conversation with its messages."""
    async with AsyncSessionLocal() as session:
        # Use selectinload to explicitly load the messages relationship
        stmt = select(Conversation).where(Conversation.id == conversation_id).options(selectinload(Conversation.messages))
        result = await session.execute(stmt)
        conversation = result.scalars().first()
        
        if not conversation:
            print(f"❌ Conversation {conversation_id} not found")
            return False
        
        print(f"✅ Retrieved conversation: id={conversation.id}, title={conversation.title}")
        
        # Now we can safely access the messages
        messages = conversation.messages
        print(f"✅ Found {len(messages)} messages:")
        
        for i, message in enumerate(messages):
            print(f"  {i+1}. [{message.message_type.value}]: {message.content[:50]}...")
        
        return True


async def run_tests():
    """Run all database tests."""
    try:
        # Test creating data
        conversation_id = await test_create_conversation()
        
        # Test retrieving data
        await test_retrieve_conversation(conversation_id)
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1) 