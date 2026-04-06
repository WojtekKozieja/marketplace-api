from routers import user, category, offer, order, price_log
from database import app

app.include_router(user.router)
app.include_router(category.router)
app.include_router(offer.router)
app.include_router(order.router)
app.include_router(price_log.router)
