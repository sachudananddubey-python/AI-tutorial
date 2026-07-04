from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.gemini_service import generate_ai_response
from app.dependencies.auth_dependency import get_current_user
from app.models.user import User
from app.repositories.chat_repository import ChatRepository

router = APIRouter(prefix="/chat", tags=["Chat"])

chat_repo = ChatRepository()


class ChatRequest(BaseModel):
    prompt: str


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not request.prompt.strip():
        return {
            "status": False,
            "message": "Prompt cannot be empty"
        }

    chat_repo.save_chat(
        db=db,
        user_id=current_user.id,
        role="user",
        message=request.prompt
    )

    answer = generate_ai_response(request.prompt)

    chat_repo.save_chat(
        db=db,
        user_id=current_user.id,
        role="assistant",
        message=answer
    )

    return {
        "status": True,
        "answer": answer
    }

@router.get("/history")
def chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chats = chat_repo.get_user_chats(
        db=db,
        user_id=current_user.id
    )

    return {
        "status": True,
        "history": chats
    }