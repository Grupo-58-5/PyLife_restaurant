
from uuid import UUID
from pydantic import BaseModel
from src.restaurants.application.schemas.entry.create_table_schema import TableLocation

class TableRestaurantResponse(BaseModel):
    id: UUID
    table_number: int
    seats: int
    location: TableLocation
