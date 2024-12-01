from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.auth import UserCreate, UserLogin
from models.user import User
from database import get_db

router = APIRouter()

@router.post("/login/")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email, User.password == user.password).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    cleaned_user = {
        "id": db_user.id,
        "email": db_user.email,
        "name": db_user.name
    }
    return {
        "message": "Login successful",
        "user": cleaned_user
    }

@router.post("/register/")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email, password=user.password, name=user.name)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}