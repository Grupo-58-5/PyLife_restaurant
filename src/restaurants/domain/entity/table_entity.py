


from uuid import UUID
from typing import List, Optional

class TableEntity:
    def __init__(self, id: UUID, table_number: int, seats: int, location: Optional[str] = None):
        self.id = id
        self.table_number = table_number
        self.seats = seats
        self.location = location

    def __repr__(self):
        return f"TableEntity(id={self.id}, table_number={self.table_number}, seats={self.seats}, location={self.location})"
    
    def get_id(self) -> UUID:
        return self.id
    
    def get_table_number(self) -> int:
        return self.table_number
    
    def get_seats(self) -> int:
        return self.seats
    
    def get_location(self) -> Optional[str]:
        return self.location

