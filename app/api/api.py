"""
API Router Configuration.

This module configures the main API router and includes all endpoint routers.
"""

from fastapi import APIRouter

from app.api.endpoints import conversations, messages

api_router = APIRouter()

# Include the conversations router
api_router.include_router(
    conversations.router, prefix="/conversations", tags=["conversations"]
)

# Include the messages router
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
