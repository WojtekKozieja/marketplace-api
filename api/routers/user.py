from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User, Offer, favourites
from sqlalchemy import func, insert
from pydantic import EmailStr
import bcrypt
from psycopg2 import errors

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/users_activate_offers")
def get_users_offers(user_id: int, db: Session = Depends(get_db)):
    users_offers = db.query(User, Offer).join(Offer).filter(
        User.user_id == user_id,
        Offer.is_active == True,
        Offer.end_offer_date > func.now()
    ).all()

    return [
        {**user.__dict__, **offer.__dict__}
        for user, offer in users_offers
    ]


@router.get("/favorite_offers")
def get_favorite_offers(user_id: int, db: Session = Depends(get_db)):
    offers = db.query(Offer).join(
        favourites, Offer.offer_id == favourites.c.offer_id 
        ).filter(
            favourites.c.user_id == user_id,
            Offer.is_active == True,
            Offer.end_offer_date > func.now()
        ).all()
    
    return offers


@router.post("/Create_user")
def create_user(
    first_name: str,
    second_name: str,
    email: EmailStr,
    password: str,
    db: Session = Depends(get_db)
):
    if len(password) > 72:
        raise HTTPException(status_code=400, detail="Password is too long")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')
    user = User(
        first_name = first_name,
        second_name = second_name,
        email = email,
        password = hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/log_in")
def log_in(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="email not found")
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return {"messege": "login successful"}
    else:
        raise HTTPException(status_code=401, detail="wrong password")


@router.post("/add_favourite_offers", description= "In query body you must input list of offer_id")
def add_fav_offers(
    user_id: int,
    offers_id: list[int],
    db: Session = Depends(get_db)
):
    try:
        fav_offers = insert(favourites).values([
            {"user_id": user_id, "offer_id": offer_id}
            for offer_id in offers_id
        ])

        db.execute(fav_offers)
        db.commit()
        return "favourite offers added successfully"

    except IntegrityError as e:
        db.rollback()
        
        if isinstance(e.orig, errors.UniqueViolation):
            raise HTTPException(status_code=409, detail="Some offers are already in favourites")
        elif isinstance(e.orig, errors.ForeignKeyViolation):
            raise HTTPException(status_code=400, detail="User or Offer/s not exists")
        else:
            raise HTTPException(status_code=500, detail="Database error")
    except:
        raise HTTPException(status_code=500, detail=f"{e}")


@router.delete("/delete_favourite_offers")
def del_fav_offers(
        user_id: int,
        offers_id: list[int],
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    count_deleted = db.query(favourites).filter(
        favourites.c.user_id == user_id,
        favourites.c.offer_id.in_(offers_id)
    ).delete(synchronize_session=False)

    if count_deleted != len(offers_id):
        raise HTTPException(
            status_code=400,
            detail=f"Only {count_deleted} of {len(offers_id)} offers found in favourites"
        )

    db.commit()

    return {"message": f"Deleted {count_deleted} favourites offers"}
