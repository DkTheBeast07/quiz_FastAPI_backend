from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import User, UserRegister, UserLogin
from auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register")
def register(user_data: UserRegister, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    is_admin = user_data.email == "admin@example.com"
    user = User(email=user_data.email, hashed_password=hash_password(user_data.password), is_admin=is_admin)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User registered"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
