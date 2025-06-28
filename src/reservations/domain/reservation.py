
from typing import List, Optional
from uuid import UUID

from src.reservations.domain.vo.reservation_dish_vo import ReservationDishVO
from src.reservations.domain.vo.reservation_schedule_vo import ReservationSchedule
from src.reservations.domain.vo.reservation_status_vo import ReservationStatus


class Reservation:

    # TODO: Agregar los platos de la reservacion
    def __init__(
        self,
        id: UUID,
        client_id: UUID,
        restaurant_id: UUID,
        table_restaurant_id: UUID,
        status: ReservationStatus,
        reservation_schedule: ReservationSchedule,
        dishes: Optional[List[ReservationDishVO]]
    ):
        '''Use the create method insted of this'''
        self.id = id
        self.client_id = client_id
        self.restaurant_id = restaurant_id
        self.table_restaurant_id = table_restaurant_id
        self.status = status
        self.reservation_schedule = reservation_schedule
        self.dishes = dishes

    @classmethod
    def create(cls,  id: UUID, client_id: UUID, restaurant_id: UUID, table_restaurant_id: UUID, status: ReservationStatus, reservation_schedule: ReservationSchedule, dishes: Optional[List[ReservationDishVO]]):
        """Factory method to create a Reservation instance."""
        if not all([id, client_id, restaurant_id, table_restaurant_id, status, reservation_schedule]):
            raise ValueError("All parameters are required to create a Reservation.")
        return cls(id, client_id, restaurant_id, table_restaurant_id, status, reservation_schedule,dishes)

    def get_id(self) -> UUID:
        return self.id

    def get_client(self) -> UUID:
        return self.client_id

    def get_restaurant(self) -> UUID:
        return self.restaurant_id

    def get_table(self) -> UUID:
        return self.table_restaurant_id

    def get_dishes(self) -> Optional[List[ReservationDishVO]]:
        return self.dishes

    def get_status(self) -> ReservationStatus:
        return self.status

    def get_schedule(self) -> ReservationSchedule:
        return self.reservation_schedule

    def cancel_reservation(self) -> None:
        if self.status in [ReservationStatus.PENDING,ReservationStatus.CONFIRMED]:
            self.status = ReservationStatus.CANCELED
        else: raise Exception(f"Can't change the status to Canceled, current status {self.status}")

    def __repr__(self):
        return f"Reservation(id={self.id},client_id={self.client_id},restaurant_id={self.restaurant_id},table_restaurant_id={self.table_restaurant_id},status={self.status},reservation_schedule={self.reservation_schedule})"

    def __str__(self):
        pass
