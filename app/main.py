from fastapi import FastAPI
from routers import user, category, offer, order, favourite, auth, my_offer
from scheduled_deactivate_offers import deactivate_offers
from fastapi_pagination import add_pagination
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

app = FastAPI(
    title="Marketplace API",
    description="""
API for online marketplace

### Test credentials
You can use the existing test account or create a new one via 'POST /users'.

**email/username:** user@test.com\n
**password:** MarketplaceAPI
    """,
    version="1.0.0"
)

add_pagination(app)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(my_offer.router)
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