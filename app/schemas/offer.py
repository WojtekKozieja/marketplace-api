from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum
from decimal import Decimal

class OfferDuration(int, Enum):
    thirty_days = 30
    ninety_days = 90
    one_hundred_eightly_days = 180
    three_hundred_sixty_days = 360


class AddOffer(BaseModel):
    subcategory_id: int
    unit_price:     Decimal = Field(gt=0, decimal_places=2)
    quantity:       int = Field(gt=0)
    title:          str = Field(min_length=1, max_length=50)
    description:    str = Field(min_length=1, max_length=1000)
    photo:          str = Field(min_length=1, max_length=100)
    offer_duration: int = Field(gt=0, description="Duration of the offer in days")


class OfferResponse(BaseModel):
    offer_id:           int
    seller_id:          int
    subcategory_id:     int
    unit_price:         Decimal
    quantity:           int
    title:              str
    description:        str
    photo:              str
    start_offer_date:   datetime
    end_offer_date:     datetime
    is_active:          bool

    model_config = ConfigDict(from_attributes=True)


class OfferUpdate(BaseModel):
    unit_price:     Decimal | None = Field(default=None, gt=0, decimal_places=2)
    quantity:       int | None = Field(default=None, gt=0)
    title:          str | None = Field(default=None, min_length=1, max_length=50)
    description:    str | None = Field(default=None, min_length=1, max_length=1000)
    photo:          str | None = Field(default=None, min_length=1, max_length=100)


class ExtendOffer(BaseModel):
    extra_days:     int = Field(gt=0, description="Number of days to extend the offer")