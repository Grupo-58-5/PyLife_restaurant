

from datetime import time
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

class RestaurantModel(SQLModel, table=True):
    """Model representing a restaurant in the database."""

    __tablename__ = "restaurants"
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True, nullable=False)
    location: str = Field(index=True, nullable=False)
    opening_time: time = Field(nullable=False)
    closing_time: time = Field(nullable=False)