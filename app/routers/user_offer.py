from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models import Offer
from schemas.offer import OfferResponse, AddOffer, OfferUpdate, ExtendOffer
from routers.auth import get_current_user
from routers.offer import filter_offers_by_active_status

router = APIRouter(prefix="/users", tags=["User Offers"])

@router.get("/me/offers", response_model=list[OfferResponse])
def get_users_offers(
    is_active: bool | None = None,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    offers = filter_offers_by_active_status(db, is_active)
    offers = offers.filter(Offer.seller_id == current_user_id).all()

    return offers


@router.post("/me/offers", response_model=OfferResponse)
def create_offer(
    new_offer: AddOffer,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)):

    new_offer = Offer(
        seller_id = current_user_id,
        unit_price = new_offer.unit_price,
        quantity = new_offer.quantity,
        title = new_offer.title,
        description = new_offer.description,
        photo = new_offer.photo,
        subcategory_id = new_offer.subcategory_id,
        end_offer_date = func.now() + timedelta(days=new_offer.offer_duration)
    )

    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return new_offer


@router.patch('/{offer_id}')
def change_offer(
    offer_id: int,
    data: OfferUpdate,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)):

    offer = db.query(Offer).filter(
        Offer.offer_id == offer_id,
        Offer.seller_id == current_user_id
    ).first()

    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(offer, field, value)

    db.commit()
    db.refresh(offer)
    return offer


@router.patch("/{offer_id}/end-date", response_model=OfferResponse)
def update_end_offer_day(
    offer_id: int,
    extra_days: ExtendOffer,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    offer = db.query(Offer).filter(
        Offer.offer_id == offer_id,
        Offer.is_active == True,
        Offer.end_offer_date > func.now(),
        Offer.seller_id == current_user_id
    ).first()
    
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    offer.end_offer_date = offer.end_offer_date + timedelta(days=extra_days.extra_days)
    db.commit()
    db.refresh(offer)
    return offer




