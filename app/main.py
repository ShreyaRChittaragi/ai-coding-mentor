from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import memory

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered coding practice mentor with behavioral memory",
    version="0.1.0"
)

app.include_router(memory.router)

@app.get("/")
def root():
    return {"status": "ok", "app": settings.APP_NAME}

@app.get("/health")
def health():
    return {"status": "healthy"}