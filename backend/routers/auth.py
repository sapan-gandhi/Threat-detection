from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserLogin, UserCreate, UserResponse, GoogleAuthToken

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Account not found. Please register first.")
        
    if user.hashed_password is not None and user.hashed_password != user_data.password:
        raise HTTPException(status_code=401, detail="Invalid password.")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated")

    return user

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    new_user = User(
        email=user_data.email, 
        name=user_data.name,
        hashed_password=user_data.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/google")
def google_auth(token: GoogleAuthToken, db: Session = Depends(get_db)):
    email = token.email
    name = token.name
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Google account not linked to a registered user. Please register first.")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated")

    return {"user": {"id": user.id, "email": user.email, "name": user.name, "role": user.role, "is_active": user.is_active}, "token": "mock_jwt_token"}

@router.post("/admin/login")
def admin_login(user_data: UserLogin, db: Session = Depends(get_db)):
    if user_data.email == "admin@spamshield.com" and user_data.password == "admin123":
        user = db.query(User).filter(User.email == "admin@spamshield.com").first()
        if not user:
            user = User(email="admin@spamshield.com", name="Super Admin", role="admin")
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    raise HTTPException(status_code=401, detail="Invalid admin credentials")
