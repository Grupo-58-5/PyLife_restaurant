



from datetime import time


class RestaurantSchedule:
    def __init__(self, opening_time: time, closing_time: time):
        self.validate(opening_time, closing_time)
        self._opening_time = opening_time
        self._closing_time = closing_time

    def validate(self, opening_time: time, closing_time: time) -> None:
        """Validates the restaurant schedule."""
        if opening_time >= closing_time:
            raise ValueError("Closing hour must be greather than opening hour")
        if not (0 <= opening_time.hour < 24 and 0 <= closing_time.hour < 24):
            raise ValueError("Opening and closing hours must be valid times of the day")
    
    @classmethod
    def create(cls, opening_time: time, closing_time: time) -> "RestaurantSchedule":
        """Factory method to create a RestaurantSchedule instance."""
        return cls(opening_time, closing_time)

    @property
    def opening_time(self) -> time:
        return self._opening_time
    
    @property
    def closing_time(self) -> time:
        return self._closing_time
    
    def __repr__(self):
        return f"RestaurantSchedule( opening_time={self._opening_time}, closing_time={self._closing_time})"