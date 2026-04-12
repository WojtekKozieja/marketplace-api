from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from database import get_db
from models import Offer, Subcategory
from schemas.offer import OfferResponse
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

    result = filter_offers_by_active_status(db, is_active)
    
    if subcategory_id:
        result = result.filter(Offer.subcategory_id == subcategory_id)
    elif category_id:
        result = result.join(Offer.subcategory).filter(Subcategory.category_id == category_id)

    if max_price:
        result = result.filter(Offer.unit_price <= max_price)
    if min_price:
        result = result.filter(Offer.unit_price >= min_price)

    return result.all()


@router.get("/{offer_id}", response_model=OfferResponse)
def get_offers_by_id(offer_id: int, db: Session = Depends(get_db)):
    result = db.query(Offer).filter(Offer.offer_id == offer_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    return result


@router.get("/{offer_id}/price_logs", response_model=list[PriceLogsResponse])
def get_price_logs(offer_id: int, db: Session = Depends(get_db)):
    result = db.query(PriceLogs).filter(PriceLogs.offer_id == offer_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Offer not found")

    return result