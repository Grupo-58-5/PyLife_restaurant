

from datetime import time, datetime
from sqlmodel import Field, SQLModel
from src.common.db.database import Base

import uuid

class ReservationModel(SQLModel, Base):
    """Model for reservations in the database."""
    
    __tablename__ = "reservations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    init_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    end_date: datetime = Field(default_factory=datetime.utcnow, nullable=True)
    status: str = Field(default="pending", nullable=False)