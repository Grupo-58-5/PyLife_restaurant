


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
    
    # def filter_by_seats(tables: List[TableEntity], min_seats: int) -> List[TableEntity]:
    #     return [table for table in tables if table.get_seats() >= min_seats]

    # def filter_by_location(tables: List[TableEntity], location: str) -> List[TableEntity]:
    #     return [table for table in tables if table.get_location() == location]

    # def filter_by_seats_and_location(tables: List[TableEntity], min_seats: int, location: str) -> List[TableEntity]:
    #     return [table for table in tables if table.get_seats() >= min_seats and table.get_location() == location]

