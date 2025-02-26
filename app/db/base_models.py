# Import base
from app.db.base import Base

# Import all models for Alembic
from app.models.conversation import Conversation
from app.models.message import Message
# Add other models as they're created 