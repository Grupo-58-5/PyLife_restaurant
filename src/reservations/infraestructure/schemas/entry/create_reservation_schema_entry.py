from uuid import UUID
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator, root_validator, model_validator
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

    @model_validator(mode="after")
    def validate_reservation(self):
        """Validations before confirming a reservation."""
        if self.start_time >= self.finish_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Finish time must be later than start time.")

        if self.duration_hours > 4:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Maximum reservation duration is 4 hours.")

        return self

    @field_validator("dishes")
    def max_five_dishes(cls, value: Optional[List[UUID]]) -> Optional[List[UUID]]:
        if value is not None and len(value) > 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can select at most 5 dishes for a reservation.")
        return value
