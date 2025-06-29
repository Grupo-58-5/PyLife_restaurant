
from uuid import UUID
from pydantic import BaseModel
from src.restaurants.application.schemas.entry.create_table_schema import TableLocation

class BaseTableResponse(BaseModel):

    table_number: int
    seats: int
    location: str | TableLocation
    

class TableDetailsResponse(BaseTableResponse):
    id: UUID
    
class RestaurantTableResponse(BaseModel):

    """Schema for the response of a restaurant's table."""
    restaurant_id: UUID
    restaurant_name: str
    tables: list[TableDetailsResponse]
