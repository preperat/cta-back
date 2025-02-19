from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here for Alembic to detect
from app.models.message import Message
from app.models.conversation import Conversation
# Add other models as they're created 