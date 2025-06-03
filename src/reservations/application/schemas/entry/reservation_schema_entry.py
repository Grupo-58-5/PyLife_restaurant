from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Optional

class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    COMPLETED = "completed"

class ReservationSchemaEntry(BaseModel):

    id: int = Field(..., gt=0, description="Reservation ID must be a positive integer.")
    client_id: int = Field(..., gt=0, description="Client ID must be a positive integer.")
    restaurant_id: int = Field(..., gt=0, description="Restaurant ID must be a positive integer.")
    table_id: int = Field(..., gt=0, description="Table ID must be a positive integer.")
    start_time: datetime = Field(..., description="Start time of the reservation.")
    finish_time: datetime = Field(..., description="Finish time of the reservation.")
    status: ReservationStatus = Field(default=ReservationStatus.PENDING, description="Reservation status.")
    
    @property
    def duration_hours(self) -> float:
        """Calculate the duration in hours."""
        return (self.finish_time - self.start_time).total_seconds() / 3600

    @classmethod
    def validate_reservation(cls, reservation_data: "ReservationSchemaEntry"):
        """Validations before confirming a reservation."""
        if reservation_data.start_time >= reservation_data.finish_time:
            raise ValueError("Finish time must be later than start time.")
        
        if reservation_data.duration_hours > 4:
            raise ValueError("Maximum reservation duration is 4 hours.")

        if reservation_data.table_id is None:
            raise ValueError("A table must be selected for the reservation.")