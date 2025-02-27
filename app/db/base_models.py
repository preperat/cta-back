# Import base
# Remove unused import: Base

# Import all models for Alembic
# These imports are needed for Alembic to detect models
# even if they appear unused in this file
# pylint: disable=unused-import
from app.models.conversation import Conversation  # noqa: F401
from app.models.message import Message  # noqa: F401

# Add other models as they're created
