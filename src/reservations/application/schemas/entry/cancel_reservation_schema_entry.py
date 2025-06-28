from uuid import UUID
from pydantic import BaseModel, Field

class CancelReservationSchemaEntry(BaseModel):

    """Schema to change the status of the reservation for Cancel."""

    client_id: UUID = Field(...)
    reservation_id: UUID = Field(...)