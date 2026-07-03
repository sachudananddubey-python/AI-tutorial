from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer,primary_key=True,index=True,autoincrement=True)
  
  name = Column(String(20),nullable=False)
  email = Column(String(150),unique=True,nullable=False)
  
  password = Column(String(255),nullable=False)
  created_at = Column(DateTime(timezone=True),server_default=func.now())
  
  chats =relationship("Chat",back_populates="user",cascade="all,delete")
  
  
  