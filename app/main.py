from routers import user, category, offer, order, user_offer, favourite
#from token import router
from routers import auth
from scheduled_deactivate_offers import deactivate_offers
from database import app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(user_offer.router)
app.include_router(favourite.router)
app.include_router(category.router)
app.include_router(offer.router)
app.include_router(order.router)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

sheduler = BackgroundScheduler()
sheduler.add_job(
    deactivate_offers,
    CronTrigger(hour=3, minute=0)
)

sheduler.start()