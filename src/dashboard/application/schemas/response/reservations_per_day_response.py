from datetime import date
from pydantic import BaseModel

class ReservationsPerDayItemResponse(BaseModel):
    date: date
    count: int