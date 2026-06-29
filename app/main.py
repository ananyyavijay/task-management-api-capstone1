from fastapi import FastAPI
from app.routers import auth, projects, task, attachments
import os

app = FastAPI()

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