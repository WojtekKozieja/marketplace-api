from sqlalchemy import func
from database import SessionLocal
from models import Offer
import logging

logger = logging.getLogger(__name__)

def deactivate_offers():
    db = SessionLocal()
    try:
        count = db.query(Offer).filter(
            Offer.is_active == True,
            Offer.end_offer_date < func.now()
        ).update({"is_active": False})
        db.commit()
        logger.info(f"Deactivated {count} offers")
    except Exception as e:
        logger.error(f"ERROR during deactivating offers: {e}")
        db.rollback()
    finally:
        db.close()



if __name__ == "__main__":
    print("Starting offer deactivation")
    deactivate_offers()
    print("job cron completed")