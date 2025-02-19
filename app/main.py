from fastapi import FastAPI
from .config import settings
from .security import SecurityManager

app = FastAPI(debug=settings.DEBUG)
security_manager = SecurityManager()

@app.get("/")
async def root():
    return {"message": "Hello World"} 