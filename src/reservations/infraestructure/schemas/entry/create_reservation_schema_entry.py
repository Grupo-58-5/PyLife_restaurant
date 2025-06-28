from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum
from typing import List, Optional

class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    COMPLETED = "completed"

class CreateReservationSchemaEntry(BaseModel):

    restaurant_id: UUID = Field(..., description="Restaurant ID must be a valid UUID.")
    table_id: UUID = Field(..., description="Table ID must be a valid UUID.")
    dishes: List[UUID] = Field(default=None, description="List of dish IDs.")
    start_time: datetime = Field(..., description="Start time of the reservation.")
    finish_time: datetime = Field(..., description="Finish time of the reservation.")

    @property
    def duration_hours(self) -> float:
        """Calculate the duration in hours."""
        return (self.finish_time - self.start_time).total_seconds() / 3600

    @classmethod
    def validate_reservation(cls, reservation_data: "CreateReservationSchemaEntry"):
        """Validations before confirming a reservation."""
        if reservation_data.start_time >= reservation_data.finish_time:
            raise ValueError("Finish time must be later than start time.")

        if reservation_data.duration_hours > 4:
            raise ValueError("Maximum reservation duration is 4 hours.")

        if reservation_data.table_id is None:
            raise ValueError("A table must be selected for the reservation.")

    @field_validator("dishes")
    def max_five_dishes(cls, value: Optional[List[UUID]]) -> Optional[List[UUID]]:
        if value is not None and len(value) > 5:
            raise ValueError("You can select at most 5 dishes for a reservation.")
        return value
