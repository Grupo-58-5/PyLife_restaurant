from datetime import time
from typing import List, TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    # Referencias de tipo para evitar ciclos
    from .table_model import TableModel

if TYPE_CHECKING:
    from src.restaurants.infraestructure.model.menu_model import MenuModel
    from src.reservations.infraestructure.models.reservation_model import ReservationModel


class RestaurantModel(SQLModel, table=True):
    """Model representing a restaurant in the database."""

    __tablename__ = "restaurants"
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True, nullable=False)
    location: str = Field(index=True, nullable=False)
    opening_time: time = Field(nullable=False)
    closing_time: time = Field(nullable=False)

    tables: List["TableModel"] = Relationship(back_populates="restaurant")
    menu_items: List["MenuModel"] = Relationship(back_populates="restaurant")
    reservations: Optional[List["ReservationModel"]] = Relationship(back_populates="restaurant")
