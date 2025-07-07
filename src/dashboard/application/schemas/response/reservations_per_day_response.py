from datetime import date
from pydantic import BaseModel

class ReservationsPerDayItemResponse(BaseModel):
    period: str
    count: int
