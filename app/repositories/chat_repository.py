from sqlalchemy.orm import Session
from app.models.chat import Chat


class ChatRepository:

    def save_chat(self, db: Session, user_id: int, role: str, message: str):
        chat = Chat(
            user_id=user_id,
            role=role,
            message=message
        )

        db.add(chat)
        db.commit()
        db.refresh(chat)

        return chat

    def get_user_chats(self, db: Session, user_id: int):
        return (
            db.query(Chat)
            .filter(Chat.user_id == user_id)
            .order_by(Chat.created_at.asc())
            .all()
        )