


from uuid import UUID

from pydantic import BaseModel


class GetMenuEntrySchema(BaseModel):
    """
    Schema for getting a menu entry.
    """
    restaurant_id: UUID 