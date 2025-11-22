from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import User, UserRegister, UserLogin
from auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register")
def register(user_data: UserRegister, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Set admin flag based on email
    is_admin = user_data.email == "admin@example.com"
    user = User(email=user_data.email, hashed_password=hash_password(user_data.password), is_admin=is_admin)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User registered"}

@router.post("/login")
def login(user_data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_data.email)).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"accessToken": token}