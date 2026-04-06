from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import func
from database import SessionLocal
from models import Offer


def deactivate_offers():
    db = SessionLocal()
    db.query(Offer).filter(
        Offer.is_active == True,
        Offer.end_offer_date < func.now()
    ).update({"is_active": False})
    db.commit()


if __name__ == "__main__":
    print("Starting offer deactivation")
    deactivate_offers()
    print("job cron completed")