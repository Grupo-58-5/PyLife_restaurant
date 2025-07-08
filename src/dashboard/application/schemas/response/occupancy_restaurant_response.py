from typing import List
from pydantic import BaseModel
from uuid import UUID

class OccupancyItemResponse(BaseModel):
    """
    Schema for the response of restaurant occupancy.
    """
    restaurant_id: UUID
    restaurant_name: str
    occupancy: float

class OccupancyResponse(BaseModel):
    data: List[OccupancyItemResponse]

