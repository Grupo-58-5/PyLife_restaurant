from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ReservationStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    COMPLETED = "completed"

@dataclass
class Reservation:
    id: int
    client_id: int
    restaurant_id: int
    table_id: int  
    start_time: datetime
    finish_time: datetime
    status: ReservationStatus = ReservationStatus.PENDING

    def validate_reservation(self):
        """Validaciones antes de confirmar una reserva."""
        if self.start_time >= self.finish_time:
            raise ValueError("Finish time must be later than start time.")
        
        duration = (self.finish_time - self.start_time).total_seconds() / 3600
        if duration > 4:
            raise ValueError("Maximum reservation duration is 4 hours.")
        
        if self.table_id is None:
            raise ValueError("A table must be selected for the reservation.")