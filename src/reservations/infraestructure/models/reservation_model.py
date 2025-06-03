

from datetime import datetime
from PyLife_restaurant.src.reservations.domain.reservation import ReservationStatus
from sqlmodel import Field, SQLModel
from src.common.db.database import Base
from uuid import UUID, uuid4


class ReservationModel(SQLModel, Base):
    """Model for reservations in the database."""
    
    __tablename__ = "reservations"

    id: UUID = Field(default_factory = uuid4, primary_key=True, index=True)
    client_id: int = Field(foreign_key="clients.id", nullable=False)
    restaurant_id: UUID = Field(foreign_key="restaurants.id", nullable=False)
    table_id: int = Field(foreign_key="tables.id", nullable=False)
    start_time: datetime = Field(nullable=False)
    finish_time: datetime = Field(nullable=False)
    status: ReservationStatus = Field(default=ReservationStatus.PENDING, nullable=False, index=True)
