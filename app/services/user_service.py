from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        user = User.create(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
        )
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email"""
        result = await self.session.execute(
            User.__table__.select().where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """Get user by username"""
        result = await self.session.execute(
            User.__table__.select().where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def authenticate_user(self, email: str, password: str) -> User | None:
        """Authenticate user"""
        user = await self.get_user_by_email(email)
        if not user or not user.verify_password(password):
            return None
        return user
