from routers import user, category, offer, order, price_log
from scheduled_deactivate_offers import deactivate_offers
from database import app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

app.include_router(user.router)
app.include_router(category.router)
app.include_router(offer.router)
app.include_router(order.router)
app.include_router(price_log.router)

sheduler = BackgroundScheduler()
sheduler.add_job(
    deactivate_offers,
    CronTrigger(hour=3, minute=0)
)

sheduler.start()