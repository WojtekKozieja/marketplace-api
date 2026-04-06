from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Offer, Subcategory
from sqlalchemy import func
from datetime import timedelta
from enum import Enum
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/offer", tags=["Offers"])


@router.get("/all_offers")
def get_offers(db: Session = Depends(get_db)):
    offers = db.query(Offer).all()
    return offers


@router.get("/search_offer_by_id")
def get_offers_by_id(offer_id: int, db: Session = Depends(get_db)):
    return db.query(Offer).filter(Offer.offer_id == offer_id).first()


@router.get("/search_active_offers", tags=(["Offers"]), description="""
    You must choose category_id or subcategory_id.\n
    If you choose both, it will find offers matching to subcategory even if category_id dont match to subcategory_id.\n
    Check section "Category and Subcategory" to find matching category_id to subcategory_id.
""")
def get_search_active_offers(
    category_id: int = None,
    subcategory_id: int = None,
    min_price: float = None,
    max_price: float = None,
    db: Session = Depends(get_db)):

    if not subcategory_id and not category_id:
        raise HTTPException(status_code=404, detail="You must choose category_id or subcategory_id.")

    result = db.query(Offer).filter(
            Offer.is_active == True,
            Offer.end_offer_date > func.now()
        )
    
    if subcategory_id:
        result = db.query(Offer).filter(Offer.subcategory_id == subcategory_id)
    elif category_id:
        result = db.query(Offer).join(Offer.subcategory).filter(Subcategory.category_id == category_id)

    if(max_price):
        result = result.filter(Offer.unit_price <= max_price)
    if(min_price):
        result = result.filter(Offer.unit_price >= min_price)

    return result.all()


class OfferDuration(int, Enum):
    thirty_days = 30
    ninety_days = 90
    one_hundred_eightly_days = 180
    three_hundred_sixty_days = 360

@router.post("/add_offer")
def create_offer(
    seller_id: int,
    subcategory_id: int,
    unit_price: float,
    quantity: int,
    title: str,
    description: str,
    photo: str,
    offer_duration: OfferDuration = None,
    db: Session = Depends(get_db)):

    new_offer = Offer(
        seller_id = seller_id,
        unit_price = unit_price,
        quantity = quantity,
        title = title,
        description = description,
        photo = photo,
        subcategory_id = subcategory_id,
        end_offer_date = func.now() + timedelta(days=offer_duration)
    )

    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return new_offer


class OfferUpdate(BaseModel):
    unit_price:     Optional[float] = None
    quantity:       Optional[int] = None
    title:          Optional[str] = None
    description:    Optional[str] = None
    photo:          Optional[str] = None


@router.put('/change_offer')
def change_offer(
    changing_offer_id: int,
    data: OfferUpdate,
    db: Session = Depends(get_db)):

    offer = db.query(Offer).filter(Offer.offer_id == changing_offer_id).first()

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(offer, field, value)

    db.commit()
    db.refresh(offer)
    return offer


@router.put("/extend_offer")
def update_end_offer_day(offer_id: int, extra_days: OfferDuration, db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(
        Offer.offer_id == offer_id,
        Offer.is_active == True,
        Offer.end_offer_date > func.now()
        ).first()
    
    if not offer:
        raise HTTPException(status_code=404, detail="Wrong offer_id. You can extend only active offers.")
    
    offer.end_offer_date = offer.end_offer_date + timedelta(days=extra_days)
    db.commit()
    db.refresh(offer)
    return offer
