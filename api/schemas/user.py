from pydantic import BaseModel, EmailStr, ConfigDict

class UserResponse(BaseModel):
    user_id: int
    first_name: str
    second_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    password: str


class LogInUser(BaseModel):
    email: EmailStr
    password: str

class FavouriteOffer(BaseModel):
    user_id: int
    offer_id: int