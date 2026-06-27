from fastapi import FastAPI
from app.routers import auth, projects

app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "API is working !"}

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

app.include_router(projects.router, tags=["Projects"])