
from abc import ABC, abstractmethod
from uuid import UUID

from PyLife_restaurant.src.reservations.domain.reservation import Reservation

class IReservationRepository(ABC):

    @abstractmethod
    def get_all_reservations(self) -> list[Reservation]:
        pass

    @abstractmethod
    def get_reservation_by_id(self, reservation_id: UUID) -> Reservation:
        pass

    @abstractmethod
    def create_reservation(self, reservation: None) -> Reservation:
        pass

    @abstractmethod
    def update_reservation(self, reservation_id: UUID, reservation: None) -> Reservation:
        pass
    


