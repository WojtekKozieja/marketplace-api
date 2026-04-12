from pydantic import BaseModel, ConfigDict

class CurrentUserResponse(BaseModel):
    user_id: int

    model_config = ConfigDict(from_attributes=True)
