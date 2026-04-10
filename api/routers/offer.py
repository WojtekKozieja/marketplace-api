from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Offer, Subcategory
from sqlalchemy import func
from datetime import timedelta
from schemas.offer import AddOffer, OfferResponse, OfferUpdate, ExtendOffer

router = APIRouter(prefix="/offer", tags=["Offers"])


@router.get("/all_offers", response_model=list[OfferResponse])
def get_offers(db: Session = Depends(get_db)):
    offers = db.query(Offer).all()
    return offers


@router.get("/{offer_id}/search_offer_by_id", response_model=OfferResponse)
def get_offers_by_id(offer_id: int, db: Session = Depends(get_db)):
    return db.query(Offer).filter(Offer.offer_id == offer_id).first()


@router.get(
        "/search_active_offers", 
        tags=(["Offers"]), 
        description=
        """
            You must choose category_id or subcategory_id.\n
            If you choose both, it will find offers matching to subcategory even if category_id dont match to subcategory_id.\n
            Check section "Category and Subcategory" to find matching category_id to subcategory_id.
        """,
        response_model=list[OfferResponse]
)
def get_search_active_offers(
    category_id: int    | None = None,
    subcategory_id: int | None = None,
    min_price: float    | None = None,
    max_price: float    | None = None,
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


@router.post("/add_offer", response_model=OfferResponse)
def create_offer(
    new_offer: AddOffer,
    db: Session = Depends(get_db)):

    new_offer = Offer(
        seller_id = new_offer.seller_id,
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




@router.patch('/{offer_id}/change_offer')
def change_offer(
    offer_id: int,
    data: OfferUpdate,
    db: Session = Depends(get_db)):

    offer = db.query(Offer).filter(Offer.offer_id == offer_id).first()

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(offer, field, value)

    db.commit()
    db.refresh(offer)
    return offer


@router.patch("/{offer_id}/extend_offer", response_model=OfferResponse)
def update_end_offer_day(
    offer_id: int,
    extra_days: ExtendOffer,
    db: Session = Depends(get_db)
):
    offer = db.query(Offer).filter(
        Offer.offer_id == offer_id,
        Offer.is_active == True,
        Offer.end_offer_date > func.now()
        ).first()
    
    if not offer:
        raise HTTPException(status_code=404, detail="Wrong offer_id. You can extend only active offers.")
    
    offer.end_offer_date = offer.end_offer_date + timedelta(days=extra_days.extra_days)
    db.commit()
    db.refresh(offer)
    return offer
