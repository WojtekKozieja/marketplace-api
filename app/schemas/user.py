from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserResponse(BaseModel):
    user_id: int
    first_name: str
    second_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=30)
    second_name: str = Field(min_length=1, max_length=30)
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8, max_length=72)
