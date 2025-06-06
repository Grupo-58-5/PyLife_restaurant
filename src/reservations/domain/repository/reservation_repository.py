
from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.reservations.domain.reservation import Reservation

class IReservationRepository(ABC):

    @abstractmethod
    def get_all_restaurant_reservations(self, restaurant_id: UUID) -> List[Reservation]:
        pass

    @abstractmethod
    def get_reservation_by_id(self, reservation_id: UUID) -> Reservation:
        pass

    @abstractmethod
    def create_reservation(self, reservation: Reservation) -> Reservation:
        pass

    @abstractmethod
    def update_reservation(self, reservation_id: UUID, reservation: Reservation) -> Reservation:
        pass
    


