from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt
from models import User
from schemas.user import UserCreate, UserResponse
from routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("")
def get_users(db: Session = Depends(get_db)) -> Page[UserResponse]:
    return paginate(db, db.query(User).order_by(User.user_id))


@router.get("/me", response_model=UserResponse)
def get_user(
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(User).filter(User.user_id == current_user_id).first()


@router.post("", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):  
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')
    
    db_user = User(
        first_name = user.first_name,
        second_name = user.second_name,
        email = user.email,
        password = hashed_password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
