from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime
from pydantic import BaseModel
from typing import Optional, List

# --- SQLAlchemy Models ---

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String, nullable=True) # Could be null if OAuth only
    role = Column(String, default="user") # 'user' or 'admin'
    is_active = Column(Integer, default=1) # 1 for active, 0 for deactivated
    messages = relationship("Message", back_populates="owner")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    msg_type = Column(String) # 'sms' or 'email'
    prediction = Column(String) # 'Spam' or 'Safe'
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="messages")

