from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Message
from schemas import MessageCreate, MessageResponse, DashboardStats
from ml_model import spam_detector

router = APIRouter(prefix="/api", tags=["messages"])

@router.post("/messages/analyze", response_model=MessageResponse)
def analyze_message(message: MessageCreate, user_id: int = Query(..., description="User ID"), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    prediction, confidence = spam_detector.predict(message.content)

    new_msg = Message(
        content=message.content,
        msg_type=message.msg_type,
        prediction=prediction,
        confidence=confidence,
        user_id=user.id
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    
    return new_msg

@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(user_id: int = Query(..., description="User ID"), db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.user_id == user_id).order_by(Message.timestamp.desc()).all()
    
    total = len(messages)
    spam = sum(1 for m in messages if m.prediction == "Spam")
    safe = total - spam
    total_sms = sum(1 for m in messages if m.msg_type == "sms")
    total_emails = sum(1 for m in messages if m.msg_type == "email")
    
    accuracy_rate = 95.5
    recent_messages = messages[:5]

    return DashboardStats(
        total_analyzed=total,
        total_sms=total_sms,
        total_emails=total_emails,
        spam_detected=spam,
        safe_messages=safe,
        accuracy_rate=accuracy_rate,
        recent_messages=recent_messages
    )

@router.get("/messages/history", response_model=List[MessageResponse])
def get_message_history(user_id: int = Query(..., description="User ID"), db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.user_id == user_id).order_by(Message.timestamp.desc()).all()
    return messages

@router.delete("/messages/{message_id}")
def delete_message(message_id: int, user_id: int = Query(..., description="User ID"), db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id, Message.user_id == user_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    db.delete(message)
    db.commit()
    return {"status": "success", "message": "Message deleted"}
