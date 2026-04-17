from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import insert, and_, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2 import errors
from schemas.offer import OfferResponse
from schemas.favourites import FavouriteOfferResponse
from database import get_db
from routers.auth import get_current_user
from models import favourites, Offer, User


router = APIRouter(prefix="/users/me/favourites", tags=["Favourites"])

@router.get("")
def get_favourite_offers(
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Page[OfferResponse]:
    offers = db.query(Offer).join(
        favourites, and_(
            Offer.offer_id == favourites.c.offer_id,
            Offer.is_active == True
        )
        ).filter(
            favourites.c.user_id == current_user_id,
            Offer.end_offer_date > func.now()
        )
    
    return paginate(db, offers.order_by(Offer.offer_id))


@router.post(
        "/{offer_id}",
        response_model=FavouriteOfferResponse
)
def add_fav_offers(
    offer_id: int,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    offer = db.query(Offer).filter(
        Offer.offer_id == offer_id,
        Offer.is_active == True,
        Offer.end_offer_date > func.now()
    ).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    try:
        result = insert(favourites).values(
            {"user_id": current_user_id, "offer_id": offer_id}
            )
        
        db.execute(result)
        db.commit()
        return {
            "user_id": current_user_id,
            "offer_id": offer_id
        }

    except IntegrityError as e:
        db.rollback()
        
        if isinstance(e.orig, errors.UniqueViolation):
            raise HTTPException(status_code=409, detail="offers is already in favourites")
        raise HTTPException(status_code=500, detail="Database error")


@router.delete("/{offer_id}")
def del_fav_offers(
        offer_id: int,
        current_user_id: int = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == current_user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    count_deleted = db.query(favourites).filter(
        favourites.c.user_id == current_user_id,
        favourites.c.offer_id == offer_id
    ).delete(synchronize_session=False)

    if not count_deleted:
        raise HTTPException(status_code=400, detail=f"offer not found")

    db.commit()

    return {"message": "Favourite offer removed"}
