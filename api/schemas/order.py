from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal

class OrderedOffers(BaseModel):
    offer_id: int
    quantity: int


class OrderDetailsRespone(BaseModel):
    #order_id: int
    offer_id: int
    #order_date: datetime
    unit_price: Decimal = Field(decimal_places=2)
    quantity: int
    title: str
    photo: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class OrderDetailsToOrder(BaseModel):
    offer_id: int
    unit_price: Decimal = Field(decimal_places=2)
    quantity: int
    title: str
    photo: str

class OrderOfferRespone(BaseModel):
    order_id: int
    buyer_id: int
    order_date: datetime
    order_details: list[OrderDetailsToOrder]

    model_config = ConfigDict(from_attributes=True)