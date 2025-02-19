from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from app.core.security import SecurityManager
from app.models.user import User

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    username: str,
    email: str,
    password: str,
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new user"""
    user = User.create(
        username=username,
        email=email,
        password=password
    )
    session.add(user)
    await session.commit()
    return {"username": user.username, "email": user.email}

@router.get("/me")
async def get_current_user():
    """Get current user details"""
    # TODO: Implement JWT authentication
    pass 