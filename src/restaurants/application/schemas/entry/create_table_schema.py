from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, validator
from datetime import time
from enum import Enum

class TableLocation(Enum):
    INDOOR = "Indoor"
    OUTDOOR = "Outdoor"
    WINDOW = "Window"
    TERRACE = "Terrace"
    PRIVATE = "Private"
    BAR = "Bar"

class CreateTableSchema(BaseModel):
    """Schema for creating a new table entry."""

    table_number: int = Field(..., gt=0, description=" Table number must be a positive integer.")
    seats: int = Field(..., gt=0, description="Number of seats at the table.")
    location: TableLocation = Field(description="Table location.")
    

class UpdateTableSchema(BaseModel):
    """Schema for updating an existing table entry."""

    id: UUID | None = Field(default=None, description="Table ID, required for updates.")
    table_number: int | None = Field(default=None, gt=0, description="Table number must be a positive integer.")
    seats: int | None = Field(default=None, gt=0, ge=2, le=12, description="Number of seats at the table.")
    location: TableLocation | None = Field(default=None, description="Table location.")