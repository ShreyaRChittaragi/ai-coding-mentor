from app.api.routes import visualizations  
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from app.core.config import settings
from app.api.routes import memory
from app.api.routes import submit_code, get_problem, get_feedback, user_profile

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered coding practice mentor with behavioral memory",
    version="0.1.0"
)

app.include_router(memory.router)
app.include_router(submit_code.router)
app.include_router(get_problem.router)
app.include_router(get_feedback.router)
app.include_router(user_profile.router)

@app.get("/")
def root():
    return {"status": "ok", "app": settings.APP_NAME}

@app.get("/health")
def health():
    return {"status": "healthy"}
       
app.include_router(visualizations.router)      