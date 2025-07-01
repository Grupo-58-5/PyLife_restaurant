

from datetime import datetime
from pydantic import BaseModel, Field

from src.reservations.application.schemas.entry.reservation_schema_entry import ReservationStatus


class GetReservationsSchemaEntry(BaseModel):
    """
    Schema for getting reservations with optional filters and pagination.
    """
    reservation_status: ReservationStatus | None = None
    date: datetime | None = Field(
        None,
        example="2025-01-01",
        description="Date to filter reservations. If provided, only reservations on this date will be returned."
    )
    page: int = 1
    page_size: int = 10