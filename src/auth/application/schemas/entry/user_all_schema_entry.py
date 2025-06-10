from uuid import UUID
from pydantic import BaseModel, Field

class UserAllSchemaEntry(BaseModel):
    """Schema to get all users in the database."""

    skip: int = Field(default=1)
    limit: int = Field(default=10)