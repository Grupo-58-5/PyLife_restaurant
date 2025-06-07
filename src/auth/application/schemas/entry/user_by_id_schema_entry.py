from pydantic import BaseModel, Field
from uuid import UUID

class UserByIdSchemaEntry(BaseModel):
    id: UUID = Field(...)