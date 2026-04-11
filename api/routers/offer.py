from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Offer, Subcategory
from sqlalchemy import func, or_
from datetime import timedelta
from schemas.offer import AddOffer, OfferResponse, OfferUpdate, ExtendOffer
from schemas.price_log import PriceLogsResponse
from models import PriceLogs

router = APIRouter(prefix="/offers", tags=["Offers"])

def filter_offers_by_active_status(db, is_active: bool | None):
    if is_active == True:
        offers = db.query(Offer).filter(
            Offer.is_active == is_active,
            Offer.end_offer_date > func.now()
        )
    elif is_active == False:
        offers = db.query(Offer).filter(
            or_(
                Offer.is_active == False,
                Offer.end_offer_date <= func.now()
            )
        )
    else:
        offers = db.query(Offer)
    return offers


@router.get(
        "", 
        tags=(["Offers"]), 
        description=
        """
            If you choose category_id and subcategory_id, it will find offers matching to subcategory even if category_id dont match to subcategory_id.\n
            Check section "Category and Subcategory" to find matching category_id to subcategory_id.
        """,
        response_model=list[OfferResponse]
)
def get_offers(
    category_id: int    | None = None,
    subcategory_id: int | None = None,
    min_price: float    | None = None,
    max_price: float    | None = None,
    is_active: bool    | None = None,
    db: Session = Depends(get_db)):

    #if not subcategory_id and not category_id:
    #    raise HTTPException(status_code=404, detail="You must choose category_id or subcategory_id.")

    result = filter_offers_by_active_status(db, is_active)
    
    if subcategory_id:
        result = result.filter(Offer.subcategory_id == subcategory_id)
    elif category_id:
        result = result.join(Offer.subcategory).filter(Subcategory.category_id == category_id)

    if(max_price):
        result = result.filter(Offer.unit_price <= max_price)
    if(min_price):
        result = result.filter(Offer.unit_price >= min_price)

    return result.all()


@router.get("/{offer_id}", response_model=OfferResponse)
def get_offers_by_id(offer_id: int, db: Session = Depends(get_db)):
    return db.query(Offer).filter(Offer.offer_id == offer_id).first()


@router.get("/{offer_id}/price_logs", response_model=list[PriceLogsResponse])
def get_price_logs(offer_id: int, db: Session = Depends(get_db)):
    result = db.query(PriceLogs).filter(PriceLogs.offer_id == offer_id).all()
    return result


@router.post("", response_model=OfferResponse)
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


@router.patch('/{offer_id}')
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


@router.patch("/{offer_id}/end-date", response_model=OfferResponse)
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