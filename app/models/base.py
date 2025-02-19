from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase, AsyncAttrs):
    """
    Async-compatible SQLAlchemy base model
    Supports both sync and async database operations
    """
    pass 