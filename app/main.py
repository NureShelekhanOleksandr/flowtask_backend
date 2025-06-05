from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, tasks
from .database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="API for managing tasks and users",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Task Management API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }
