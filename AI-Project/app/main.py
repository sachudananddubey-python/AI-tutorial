from fastapi import FastAPI
from app.routers import chat
from app.database.database import engine,Base
from app.models import Chat,User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Chat API")

app.include_router(chat.router)


@app.get("/")
def home():
    return {
        "message": dir(chat.router)
    }