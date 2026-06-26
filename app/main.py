from fastapi import FastAPI
from app.routers import auth

app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "API is working !"}

app.include_router(auth.router, prefix="/auth", tags=["Auth"])