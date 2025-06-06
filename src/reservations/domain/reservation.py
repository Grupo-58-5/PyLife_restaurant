
from uuid import UUID

from src.reservations.domain.vo.reservation_schedule_vo import ReservationSchedule
from src.reservations.domain.vo.reservation_status_vo import ReservationStatus


class Reservation:

    def __init__(self, id: UUID, client_id: UUID, restaurant_id: UUID, table_restaurant_id: UUID, status: ReservationStatus, reservation_schedule: ReservationSchedule):
        '''Use the create method insted of this'''
        id = id,
        client_id = client_id,
        restaurant_id = restaurant_id,
        table_restaurant_id = table_restaurant_id,
        status = status,
        schedule = reservation_schedule

    @classmethod
    def create(cls,  id: UUID, client_id: UUID, restaurant_id: UUID, table_restaurant_id: UUID, status: ReservationStatus, reservation_schedule: ReservationSchedule):
        """Factory method to create a Reservation instance."""
        if not all([id, client_id, restaurant_id, table_restaurant_id, status, reservation_schedule]):
            raise ValueError("All parameters are required to create a Reservation.")
        return cls(id, client_id, restaurant_id, table_restaurant_id, status, reservation_schedule)
