from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from datetime import time

class TableLocation(str, Enum):
    INSIDE = "Inside"
    TERRACE = "Terrace"

class CreateTableSchema(BaseModel):
    """Schema for creating a new table entry."""

    table_number: int = Field(..., gt=0, description=" Table number must be a positive integer.")
    seats: int = Field(..., gt=0, description="Number of seats at the table.")
    location: TableLocation = Field(default=TableLocation.INSIDE, description="Table location.")

    @classmethod
    def validate_table(cls, table_data: "CreateTableSchema"):
        """Validate the capacity of people"""
        if table_data.seats >= 2 and table_data.seats <= 12:
            raise ValueError("Number of people out of range.")
