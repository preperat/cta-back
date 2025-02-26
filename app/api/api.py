from fastapi import APIRouter
from .endpoints import conversations, messages

api_router = APIRouter()

api_router.include_router(
    conversations.router, prefix="/conversations", tags=["conversations"]
)
api_router.include_router(
    messages.router, prefix="/conversations", tags=["messages"]
) 