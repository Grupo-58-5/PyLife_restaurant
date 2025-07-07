from sqlmodel import Field
from typing_extensions import Literal
from pydantic import BaseModel
from datetime import date

class ReservationsPerDayEntry(BaseModel):
    start_date: date = Field(..., description="Range start date")
    end_date: date = Field(..., description="End date of range")
    group_by: Literal["day", "week"] = Field(..., description="Grouping: 'day' or 'week'")
