
from uuid import UUID
from pydantic import BaseModel, Field


class DeleteMenuSchema(BaseModel):
    menu_id: UUID = Field(...),
    restaurant_id: UUID = Field(...)
