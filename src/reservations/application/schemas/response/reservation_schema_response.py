from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Optional

class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    COMPLETED = "completed"

class ReservationSchemaResponse(BaseModel):
    
    client_id: int = Field(..., gt=0, description="Client ID must be a positive integer.")
    restaurant_id: int = Field(..., gt=0, description="Restaurant ID must be a positive integer.")
    table_id: int = Field(..., gt=0, description="Table ID must be a positive integer.")
    start_time: datetime = Field(..., description="Start time of the reservation.")
    finish_time: datetime = Field(..., description="Finish time of the reservation.")
    status: ReservationStatus = Field(..., description="Reservation status.")

    class Config:
        orm_mode = True
