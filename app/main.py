from fastapi import FastAPI
from app.routers import chat,auth
from app.database.database import engine,Base
from app.models import Chat,User
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Chat API")

app.include_router(chat.router)
app.include_router(auth.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": dir(chat.router)
    }