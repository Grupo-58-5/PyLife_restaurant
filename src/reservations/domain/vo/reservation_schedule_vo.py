from datetime import datetime, timedelta


class ReservationSchedule():
    def __init__(self, start_time: datetime, end_time: datetime | None):
        '''Use the create method insted of this'''
        end_time = end_time if end_time else start_time + timedelta(hours=4)
        self.validate(start_time, end_time)
        self.start_time = start_time
        self.end_time = end_time

    def validate(start_time: datetime, end_time: datetime):
        """Reservations schedule Validations"""
        if start_time >= end_time:
            raise ValueError("Finish time must be later than start time.")
        duration = (end_time - start_time).total_seconds() / 3600
        if duration > 4:
            raise ValueError("Maximum reservation duration is 4 hours.")
    
    @classmethod
    def create(cls, start_time: datetime, end_time: datetime | None = None):
        """Factory method to create a ReservationSchedule instance."""
        return cls(start_time, end_time)
