from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import PriceLogs

router = APIRouter(prefix="/price_log", tags=["Price Logs"])

@router.get("/search_price_logs")
def get_price_logs(offer_id: int, db: Session = Depends(get_db)):
    result = db.query(PriceLogs).filter(PriceLogs.offer_id == offer_id).all()
    return result