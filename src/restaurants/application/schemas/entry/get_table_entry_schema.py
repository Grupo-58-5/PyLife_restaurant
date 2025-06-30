


from uuid import UUID

from pydantic import BaseModel

from src.restaurants.domain.entity.table_entity import TableLocation


class GetTableEntrySchema(BaseModel):
    """
    Schema for getting a table entry.
    """
    restaurant_id: UUID 
    capacity: int = 2
    location: TableLocation | None = None