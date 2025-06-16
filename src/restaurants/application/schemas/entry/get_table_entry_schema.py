


from uuid import UUID

from pydantic import BaseModel


class GetTableEntrySchema(BaseModel):
    """
    Schema for getting a table entry.
    """
    restaurant_id: UUID 