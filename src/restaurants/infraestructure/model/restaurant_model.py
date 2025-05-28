

from datetime import time
from sqlmodel import SQLModel, Field

class RestaurantModel(SQLModel, table=True):

    __tablename__ = "restaurantS"
    id: int | None = Field(primary_key=True, index=True)
    name: str = Field(index=True, nullable=False)
    location: str = Field(index=True, nullable=False)
    opening_time: time = Field(nullable=False)
    closing_time: time = Field(nullable=False)