


from datetime import time
from uuid import UUID

from pydantic import BaseModel


class BaseRestaurantResponse(BaseModel):
    """
    Base schema for restaurant response.
    
    """
    id: UUID
    name: str
    address: str
    opening_hour: time
    closing_hour: time

    class Config:
        orm_mode = True
