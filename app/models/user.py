from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from .base import Base
from app.core.security import SecurityManager

class User(Base):
    """
    User model representing application users
    
    Includes authentication and profile management
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    @classmethod
    def create(cls, username: str, email: str, password: str):
        """
        Secure user creation method with password hashing
        
        Args:
            username (str): User's chosen username
            email (str): User's email address
            password (str): Plain text password
        
        Returns:
            User: Newly created user instance
        """
        return cls(
            username=username,
            email=email,
            hashed_password=SecurityManager.hash_password(password),
            is_active=True
        )

    def verify_password(self, plain_password: str) -> bool:
        """
        Verify user's password
        
        Args:
            plain_password (str): Password to verify
        
        Returns:
            bool: Password verification result
        """
        return SecurityManager.verify_password(plain_password, self.hashed_password) 