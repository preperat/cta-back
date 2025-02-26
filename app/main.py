from fastapi import FastAPI
from .config import settings
from .security import SecurityManager
from .api.endpoints import conversations

app = FastAPI(debug=settings.DEBUG)
security_manager = SecurityManager()

# Include routers
app.include_router(conversations.router, prefix="/conversations", tags=["conversations"])

@app.get("/")
async def root():
    return {"message": "Hello World"} 