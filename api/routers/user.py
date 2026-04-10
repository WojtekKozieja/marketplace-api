from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User, Offer, favourites
from sqlalchemy import func, insert
import bcrypt
from psycopg2 import errors
from schemas.user import UserCreate, UserResponse, LogInUser, FavouriteOffer
from schemas.offer import OfferResponse

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/users_active_offers/{user_id}", response_model=OfferResponse)
def get_users_offers(user_id: int, db: Session = Depends(get_db)):
    user_offers = db.query(Offer).join(Offer).filter(
        User.user_id == user_id,
        Offer.is_active == True,
        Offer.end_offer_date > func.now()
    ).all()

    return user_offers


@router.get("/favorite_offers/{user_id}", response_model=OfferResponse)
def get_favorite_offers(user_id: int, db: Session = Depends(get_db)):
    offers = db.query(Offer).join(
        favourites, Offer.offer_id == favourites.c.offer_id 
        ).filter(
            favourites.c.user_id == user_id,
            Offer.is_active == True,
            Offer.end_offer_date > func.now()
        ).all()
    
    return offers


@router.post("/create_user", response_model=UserResponse)
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


@router.post("/log_in")
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


@router.post(
        "/add_favourite_offers", 
        description= "In query body you must input list of offer_id", 
        response_model=FavouriteOffer
)
def add_fav_offers(
    fav_offer: FavouriteOffer,
    db: Session = Depends(get_db)
):
    try:
        result = insert(favourites).values(
            {"user_id": fav_offer.user_id, "offer_id": fav_offer.offer_id}
            )
        
        db.execute(result)
        db.commit()
        return {
            "user_id": fav_offer.user_id,
            "offer_id": fav_offer.offer_id
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


@router.delete("/{user_id}/delete_favourite_offers/{offer_id}")
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
        favourites.c.offer_id == (offer_id)
    ).delete(synchronize_session=False)

    if not count_deleted:
        raise HTTPException(status_code=400, detail=f"offer not found")

    db.commit()

    return {"message": "Favourite offer removed"}
