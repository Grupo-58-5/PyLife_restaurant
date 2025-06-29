


from uuid import UUID
from typing import List, Optional
from enum import Enum

class TableLocation(Enum):
    INDOOR = "Indoor"
    OUTDOOR = "Outdoor"
    WINDOW = "Window"
    TERRACE = "Terrace"
    PRIVATE = "Private"
    BAR = "Bar"

class TableEntity:
    
    def __init__(self, id: UUID, table_number: int, seats: int, location: TableLocation):
        if not seats or seats < 2 or seats > 12:
            raise ValueError("Invalid capacity, must be between 2 and 12 seats")
        self.id = id
        self.table_number = table_number
        self.seats = seats
        self.location = location

    def __repr__(self):
        return f"TableEntity(id={self.id}, table_number={self.table_number}, seats={self.seats}, location={self.location})"
    
    def __eq__(self, other):
        if not isinstance(other, TableEntity):
            return False
        return self.id == other.id
    
    @classmethod
    def create(cls, id: UUID, table_number: int, seats: int, location: TableLocation) -> "TableEntity":
        """Factory method to create a tableEntity instance."""
        return cls(id, table_number, seats, location)

    def get_id(self) -> UUID:
        return self.id
    
    def get_table_number(self) -> int:
        return self.table_number
    
    def get_seats(self) -> int:
        return self.seats
    
    def get_location(self) -> Optional[str]:
        return self.location.value
    
    def set_table_number(self, table_number: int):
        if table_number <= 0:
            raise ValueError("Table number must be a positive integer.")
        self.table_number = table_number

    def set_seats(self, seats: int):
        if not seats or seats < 2 or seats > 12:
            raise ValueError("Invalid capacity, must be between 2 and 12 seats")
        self.seats = seats

    def set_location(self, location: TableLocation):
        if not isinstance(location, TableLocation):
            raise ValueError("Invalid location type.")
        self.location = location
    
