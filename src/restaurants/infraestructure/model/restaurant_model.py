

from datetime import time
from sqlmodel import Field, SQLModel
from src.common.db.database import Base

class RestaurantModel(Base):

    __tablename__ = "restaurants"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    location: str
    opening_time: time
    closing_time: time