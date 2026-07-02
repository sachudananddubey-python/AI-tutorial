from fastapi import FastAPI
from app.routers import chat

app = FastAPI(title="AI Chat API")

app.include_router(chat.router)


@app.get("/")
def home():
    return {
        "message": dir(chat.router)
    }