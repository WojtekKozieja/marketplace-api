from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime
from enum import Enum
from decimal import Decimal

class OfferDuration(int, Enum):
    thirty_days = 30
    ninety_days = 90
    one_hundred_eightly_days = 180
    three_hundred_sixty_days = 360


class AddOffer(BaseModel):
    seller_id:      int
    subcategory_id: int
    unit_price:     Decimal = Field(gt=0, decimal_places=2)
    quantity:       int = Field(gt=0)
    title:          str
    description:    str
    photo:          str
    offer_duration: int = Field(gt=0)


class OfferResponse(BaseModel):
    offer_id:           int
    seller_id:          int
    subcategory_id:     int
    unit_price:         Decimal = Field(gt=0, decimal_places=2)
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
    quantity:       int | None = None
    title:          str | None = None
    description:    str | None = None
    photo:          str | None = None


class ExtendOffer(BaseModel):
    extra_days:     int = Field(gt=0)