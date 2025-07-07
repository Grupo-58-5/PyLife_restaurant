from pydantic import BaseModel
from datetime import date

class ReservationsPerDayEntry(BaseModel):
    start_date: date
    end_date: date