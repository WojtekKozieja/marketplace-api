from pydantic import BaseModel, ConfigDict

class SubcategoryResponse(BaseModel):
    subcategory_id: int
    subcategory_name: str

    model_config = ConfigDict(from_attributes=True)