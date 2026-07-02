from fastapi import FastAPI
from app.routers import auth, projects, task, attachments
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://capstone-task-frontend.azurewebsites.net",
]

# Allow overriding/adding origins through Azure App Settings
env_origins = os.getenv("ALLOWED_ORIGINS")

if env_origins:
    allowed_origins = [
        origin.strip()
        for origin in env_origins.split(",")
        if origin.strip()
    ]
else:
    allowed_origins = default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message" : "API is working !"}

@app.get("/health", tags=["Health"])
def check_health():
    return {
        "status": "ok",
        "service": "Task Management API - Working",
        "version": "2.0.0"
    }

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

app.include_router(projects.router, tags=["Projects"])

app.include_router(task.router, tags=["Tasks"])

app.include_router(attachments.router, tags=["Attachments"])