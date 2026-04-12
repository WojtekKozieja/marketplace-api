from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal

class OrderResponse(BaseModel):
    order_id: int
    buyer_id: int
    order_date: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderOffers(BaseModel):
    offer_id: int
    quantity: int


class OrderDetailRespone(BaseModel):
    offer_id: int
    unit_price: Decimal = Field(decimal_places=2)
    quantity: int
    title: str
    photo: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class OrderOfferRespone(BaseModel):
    order_id: int
    buyer_id: int
    order_date: datetime
    order_details: list[OrderDetailRespone]

    model_config = ConfigDict(from_attributes=True)