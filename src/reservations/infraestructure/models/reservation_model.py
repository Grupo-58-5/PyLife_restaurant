from datetime import datetime
from typing import TYPE_CHECKING, Optional
from src.reservations.domain.reservation import ReservationStatus
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4

from src.reservations.infraestructure.models.pre_order_model import PreOrder

if TYPE_CHECKING:
    from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel
    from src.restaurants.infraestructure.model.menu_model import MenuModel
    from src.restaurants.infraestructure.model.table_model import TableModel
    from src.auth.infraestructure.model.user_model import UserModel

class ReservationModel(SQLModel, table=True):
    """Model for reservations in the database."""

    __tablename__ = "reservations"

    id: UUID = Field(default_factory = uuid4, primary_key=True, index=True)

    client_id: UUID = Field(foreign_key="users.id", nullable=False)
    client: "UserModel" = Relationship(back_populates="reservations")

    restaurant_id: UUID = Field(foreign_key="restaurants.id", nullable=False)
    restaurant: Optional["RestaurantModel"] = Relationship(back_populates="reservations")

    table_id: UUID = Field(foreign_key="tables.id", nullable=False)
    table: Optional["TableModel"] = Relationship(back_populates="reservations")

    start_time: datetime = Field(nullable=False)
    finish_time: datetime = Field(nullable=False)
    status: ReservationStatus = Field(default=ReservationStatus.PENDING, nullable=False, index=True)

    dishes: list["MenuModel"] = Relationship(
        back_populates="reservations", link_model=PreOrder
    )