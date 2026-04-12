from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from datetime import datetime

class PriceLogsResponse(BaseModel):
    new_price: Decimal
    changed_date: datetime

    model_config = ConfigDict(from_attributes=True)