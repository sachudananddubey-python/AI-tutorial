from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini_service import generate_ai_response

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    prompt: str


@router.post("/")
def chat(request: ChatRequest):
    if not request.prompt.strip():
        return {
            "status": False,
            "message": "Prompt cannot be empty"
        }

    answer = generate_ai_response(request.prompt)

    return {
        "status": True,
        "answer": answer
    }