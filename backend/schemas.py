import datetime
from pydantic import BaseModel
from typing import Optional, List

# --- Pydantic Schemas ---

class MessageCreate(BaseModel):
    content: str
    msg_type: str

class MessageResponse(BaseModel):
    id: int
    content: str
    msg_type: str
    prediction: str
    confidence: float
    timestamp: datetime.datetime
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    name: str
    password: Optional[str] = None # Or oauth token

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    is_active: int

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_analyzed: int
    total_sms: int
    total_emails: int
    spam_detected: int
    safe_messages: int
    accuracy_rate: float
    recent_messages: List[MessageResponse]

class UserActivityResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: int
    total_sms: int
    total_emails: int

class AdminDashboardStats(BaseModel):
    total_users: int
    user_activities: List[UserActivityResponse]

class GoogleAuthToken(BaseModel):
    email: str
    name: str
