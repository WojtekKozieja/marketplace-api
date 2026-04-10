from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from enum import Enum


class OfferDuration(int, Enum):
    thirty_days = 30
    ninety_days = 90
    one_hundred_eightly_days = 180
    three_hundred_sixty_days = 360


class AddOffer(BaseModel):
    seller_id:      int
    subcategory_id: int
    unit_price:     float
    quantity:       int
    title:          str
    description:    str
    photo:          str
    offer_duration: int

    @field_validator("offer_duration")
    def duration_must_be_positive(cls, offer_duration):
        if offer_duration <= 0:
            raise ValueError("Offer duration must be positive")
        return offer_duration


class OfferResponse(BaseModel):
    offer_id:           int
    seller_id:          int
    subcategory_id:     int
    unit_price:         float
    quantity:           int
    title:              str
    description:        str
    photo:              str
    start_offer_date:   datetime
    end_offer_date:     datetime
    is_active:          bool

    model_config = ConfigDict(from_attributes=True)


class OfferUpdate(BaseModel):
    unit_price:     float | None = None
    quantity:       int | None = None
    title:          str | None = None
    description:    str | None = None
    photo:          str | None = None


class ExtendOffer(BaseModel):
    extra_days:     int

    @field_validator("extra_days")
    def extra_days_must_be_positive(cls, extra_days):
        if extra_days <= 0:
            raise ValueError("Offer duration must be positive")
        return extra_days