from uuid import UUID
from pydantic import BaseModel, Field
from src.auth.domain.enum.role import Roles

class UserAllSchemaeResponse(BaseModel):
    """Schema for response to show all users."""

    id: UUID = Field(...)
    name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    role: Roles = Field(...)