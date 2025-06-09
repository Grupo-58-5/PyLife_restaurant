from pydantic import BaseModel, Field
from src.auth.domain.enum.role import Roles

class UserSchemaeResponse(BaseModel):
    """Schema for response to register a new user."""

    id: str = Field(...)
    role: Roles = Field(...)
    message: str = Field(...)