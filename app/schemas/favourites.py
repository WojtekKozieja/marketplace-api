from pydantic import BaseModel, ConfigDict

class FavouriteOfferResponse(BaseModel):
    user_id: int
    offer_id: int

    model_config = ConfigDict(from_attributes=True)