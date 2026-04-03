from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Message
from schemas import AdminDashboardStats, UserActivityResponse, UserResponse

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    all_messages = db.query(Message).all()
    
    total = len(all_messages)
    spam = sum(1 for m in all_messages if m.prediction == "Spam")
    safe = total - spam
    
    return {
        "total_users": total_users,
        "total_messages": total,
        "spam_detected": spam,
        "safe_messages": safe,
        "system_accuracy": 96.2,
        "recent_logs": [
            {"id": m.id, "user_id": m.user_id, "prediction": m.prediction, "timestamp": m.timestamp, "msg_type": m.msg_type} 
            for m in all_messages[::-1][:15]
        ]
    }

@router.get("/dashboard-stats", response_model=AdminDashboardStats)
def get_admin_dashboard_stats(db: Session = Depends(get_db)):
    users = db.query(User).all()
    user_activities = []
    
    for user in users:
        sms_count = db.query(Message).filter(Message.user_id == user.id, Message.msg_type == 'sms').count()
        email_count = db.query(Message).filter(Message.user_id == user.id, Message.msg_type == 'email').count()
        
        user_activities.append(
            UserActivityResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                role=user.role,
                is_active=user.is_active,
                total_sms=sms_count,
                total_emails=email_count
            )
        )
        
    return AdminDashboardStats(
        total_users=len(users),
        user_activities=user_activities
    )

@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/users/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = 0
    db.commit()
    return {"status": "success", "message": f"User {user_id} deactivated"}

@router.post("/users/{user_id}/activate")
def activate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = 1
    db.commit()
    return {"status": "success", "message": f"User {user_id} activated"}

@router.delete("/users/{user_id}")
def delete_user_completely(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.query(Message).filter(Message.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"status": "success", "message": f"User {user_id} and all records deleted"}
