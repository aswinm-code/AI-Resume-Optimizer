# Start the FastAPI application.

from fastapi import FastAPI
from app.models import User, Resume
from app.core.database import Base, engine
# here this one no longer use as we r using alembic for migrations so we don't need to create tables manually
# Base.metadata.create_all(bind=engine)
from app.api.v1.auth import router as auth_router
from app.api.v1.resumes import router as resume_router
from app.api.v1.users import router as user_router
from app.api.v1 import job_descriptions
from app.api.v1 import analysis
from app.api.v1 import resume_versions
from app.api.v1 import resume_optimizer
from app.api.v1 import export
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Resume AI API",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite React
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registers the authentication routes with the FastAPI application.
app.include_router(auth_router)

app.include_router(resume_router)
app.include_router(user_router)
app.include_router(job_descriptions.router)
app.include_router(analysis.router)
app.include_router(  resume_versions.router)
app.include_router(
    resume_optimizer.router
)
app.include_router(export.router)

@app.get("/")
def root():
    return {
        "message": "Resume AI API is running"
    }