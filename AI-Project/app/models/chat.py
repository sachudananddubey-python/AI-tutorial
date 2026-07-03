from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


from app.database.database import Base

class Chat(Base):
  __tablename__ = "chat"
  
  id = Column(Integer, primary_key=True , index=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("users.id"),nullable=True)
  
  role = Column(String(20), nullable=True)
  message = Column(Text, nullable=False)
  
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  
  user = relationship(
    "User",
    back_populates="chats"
  )