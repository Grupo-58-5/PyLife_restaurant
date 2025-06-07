from pydantic import BaseModel, Field

class UserSchemaEntry(BaseModel):
    """Schema for register a new user."""

    name: str = Field(...,min_length=3)
    email: str = Field(...)
    password: str = Field(...)