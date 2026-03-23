from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from app.core.config import settings
from app.api.routes import memory
from app.api.routes import submit_code, get_problem, get_feedback, user_profile
from app.api.routes import next_problem
from app.api.routes import visualizations

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered coding practice mentor with behavioral memory",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(memory.router)
app.include_router(submit_code.router)
app.include_router(get_problem.router)
app.include_router(get_feedback.router)
app.include_router(user_profile.router)
app.include_router(next_problem.router)
app.include_router(visualizations.router)

@app.get("/")
def root():
    return {"status": "ok", "app": settings.APP_NAME}

@app.get("/health")
def health():
    return {"status": "healthy"}
