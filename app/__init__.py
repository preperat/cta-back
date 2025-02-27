"""
CTA Backend Application Package.

This package contains the FastAPI application for the Claytons Travel Assistant backend.
"""
# /Users/tef/Projects/cta/back/app/core/__init__.py
# Import core components
# Import settings
from app.core.config import settings
from app.core.security import SecurityManager

# Define what's available when importing from app
__all__ = ["settings", "SecurityManager"]
