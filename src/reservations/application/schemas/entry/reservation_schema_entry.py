from uuid import UUID
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from datetime import datetime
from enum import Enum
from typing import List, Optional

class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    COMPLETED = "completed"

class ReservationSchemaEntry(BaseModel):

    client_id: UUID = Field(..., description="Client ID must be a valid UUID.")
    restaurant_id: UUID = Field(..., description="Restaurant ID must be a valid UUID.")
    table_id: UUID = Field(..., description="Table ID must be a valid UUID.")
    dishes: Optional[List[UUID]] = Field(default=None, description="List of dish IDs.")
    start_time: datetime = Field(..., description="Start time of the reservation.")
    finish_time: datetime = Field(..., description="Finish time of the reservation.")
    status: ReservationStatus = Field(default=ReservationStatus.PENDING, description="Reservation status.")

    @property
    def duration_hours(self) -> float:
        """Calculate the duration in hours."""
        return (self.finish_time - self.start_time).total_seconds() / 3600
    

class ChangeStatusSchemaEntry(BaseModel):
    """Schema for changing the status of a reservation."""
    status: ReservationStatus = Field(..., description="New status for the reservation.")