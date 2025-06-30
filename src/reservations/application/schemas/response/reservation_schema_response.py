from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Optional

class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    COMPLETED = "completed"

class PreOrderSchemaResponse(BaseModel):
    id: UUID
    name: str

class ReservationSchemaResponse(BaseModel):
    
    reservation_id: UUID  = Field(..., description="Reservation ID must be a UUID.")
    client_id: UUID = Field(..., description="Client ID must be a UUID.")
    restaurant_id: UUID = Field(..., description="Restaurant ID must be a UUID.")
    table_id: UUID = Field(..., description="Table ID must be a UUID.")
    start_time: datetime = Field(..., description="Start time of the reservation.")
    finish_time: datetime = Field(..., description="Finish time of the reservation.")
    status: ReservationStatus = Field(..., description="Reservation status.")
    pre_order: Optional[List[PreOrderSchemaResponse]] = Field(default=None, description="List of the plates pre-order in the reservation")
    class Config:
        from_attributes = True

class ReservationBaseResponse(BaseModel):
    
    id: UUID  = Field(..., description="Reservation ID must be a UUID.")
    status: ReservationStatus = Field(..., description="Reservation status.")
    start_time: datetime = Field(..., description="Start time of the reservation.")
    finish_time: datetime = Field(..., description="Finish time of the reservation.")
    client_id: UUID = Field(..., description="Client ID must be a UUID.")
    table_id: UUID = Field(..., description="Table ID must be a UUID.")
    pre_order: Optional[List[PreOrderSchemaResponse]] = Field(default=None, description="List of the plates pre-order in the reservation")


class ReservationResponse(BaseModel):
    
    id: UUID  = Field(..., description="Reservation ID must be a UUID.")
    status: ReservationStatus = Field(..., description="Reservation status.")
    start_time: datetime = Field(..., description="Start time of the reservation.")
    finish_time: datetime = Field(..., description="Finish time of the reservation.")
    client_id: UUID = Field(..., description="Client ID must be a UUID.")
    table_id: UUID = Field(..., description="Table ID must be a UUID.")

class AllReservationsResponse(BaseModel):
    """
    Schema for all reservations response.
    """
    restaurant_id: UUID = Field(..., description="Restaurant ID must be a UUID.")
    restaurant_name: str = Field(..., description="Name of the restaurant.")
    reservations: List[ReservationResponse] = Field(..., description="List of all reservations.")