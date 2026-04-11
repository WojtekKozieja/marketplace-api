from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas.user import LogInUser
import bcrypt

router = APIRouter(prefix="/authorizations", tags=["Authorizations"])

@router.post("/login")
def log_in(
    user: LogInUser,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="email not found")
    if bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        return {"messege": "login successful"}
    else:
        raise HTTPException(status_code=401, detail="wrong password")


