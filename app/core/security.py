# /Users/tef/Projects/cta/back/app/core/security.py
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from .config import settings


class SecurityManager:
    """
    Centralized security utilities for authentication and token management.

    Key Responsibilities:
    - Password hashing
    - JWT token generation and validation
    - Secure token management
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Hash a password using bcrypt for secure storage.

        Args:
            password (str): Plain text password

        Returns:
            str: Hashed password
        """
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its stored hash.

        Args:
            plain_password (str): Password to verify
            hashed_password (str): Stored password hash

        Returns:
            bool: True if password matches, False otherwise
        """
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def create_access_token(
        cls, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Generate a JWT access token.

        Args:
            data (dict): Payload data to encode
            expires_delta (Optional[timedelta]): Token expiration time

        Returns:
            str: Encoded JWT token
        """
        to_encode = data.copy()

        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

        return encoded_jwt
