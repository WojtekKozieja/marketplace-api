from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User, Offer, favourites
from sqlalchemy import func, insert, or_, and_
import bcrypt
from psycopg2 import errors
from schemas.user import UserCreate, UserResponse, FavouriteOffer, FavouriteOfferResponse
from schemas.offer import OfferResponse
from routers.offer import filter_offers_by_active_status
from datetime import timedelta
from schemas.offer import AddOffer, OfferResponse, OfferUpdate, ExtendOffer



router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    return user


@router.get("/{user_id}/offers", response_model=list[OfferResponse])
def get_users_offers(
    user_id: int,
    is_active: bool | None = None,
    db: Session = Depends(get_db)
):
    offers = filter_offers_by_active_status(db, is_active)
    offers = offers.filter(Offer.seller_id == user_id).all()

    return offers


@router.get("/{user_id}/favourites", response_model=list[OfferResponse])
def get_favorite_offers(user_id: int, db: Session = Depends(get_db)):
    offers = db.query(Offer).join(
        favourites, and_(
            Offer.offer_id == favourites.c.offer_id,
            Offer.is_active == True
        )
        ).filter(
            favourites.c.user_id == user_id,
            Offer.end_offer_date > func.now()
        ).all()
    
    return offers


@router.post("", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    if len(user.password) > 72:
        raise HTTPException(status_code=400, detail="Password is too long")
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')
    
    db_user = User(
        first_name = user.first_name,
        second_name = user.second_name,
        email = user.email,
        password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post(
        "/{user_id}/favourites/{offer_id}",
        response_model=FavouriteOfferResponse
)
def add_fav_offers(
    user_id: int,
    offer_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = insert(favourites).values(
            {"user_id": user_id, "offer_id": offer_id}
            )
        
        db.execute(result)
        db.commit()
        return {
            "user_id": user_id,
            "offer_id": offer_id
        }

    except IntegrityError as e:
        db.rollback()
        
        if isinstance(e.orig, errors.UniqueViolation):
            raise HTTPException(status_code=409, detail="offers is already in favourites")
        elif isinstance(e.orig, errors.ForeignKeyViolation):
            raise HTTPException(status_code=400, detail="User or Offer/s not exists")
        else:
            raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")


@router.delete("/{user_id}/favourites/{offer_id}")
def del_fav_offers(
        user_id: int,
        offer_id: int,
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    count_deleted = db.query(favourites).filter(
        favourites.c.user_id == user_id,
        favourites.c.offer_id == offer_id
    ).delete(synchronize_session=False)

    if not count_deleted:
        raise HTTPException(status_code=400, detail=f"offer not found")

    db.commit()

    return {"message": "Favourite offer removed"}
