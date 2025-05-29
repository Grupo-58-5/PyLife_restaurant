


from datetime import time
from uuid import UUID

from pydantic import BaseModel


class BaseRestaurantResponse(BaseModel):
    """
    Base schema for restaurant response.
    
    """
    id: UUID
    name: str
    location: str
    opening_time: time
    closing_time: time

    class Config:
        orm_mode = True
