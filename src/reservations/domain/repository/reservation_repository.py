
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from uuid import UUID

from src.reservations.domain.reservation import Reservation
from src.shared.utils.result import Result

class IReservationRepository(ABC):

    @abstractmethod
    async def get_all_restaurant_reservations(self, restaurant_id: UUID, page: int, page_size: int) -> List[Reservation]:
        pass

    @abstractmethod
    async def get_all_users_reservations(self, client_id: UUID, page: int, page_size: int) -> Result[List[Reservation]]:
        pass

    @abstractmethod
    async def get_reservations_by_date(self, date: datetime) -> List[Reservation]:
        pass

    @abstractmethod
    async def verify_reservations_by_date_and_user(self, start_time: datetime, finish_time: datetime, client_id: UUID) -> Result[bool]:
        pass

    @abstractmethod
    async def verify_reservations_by_date_and_table(self, restaurant_id: UUID, start_time: datetime, finish_time: datetime, table_id: UUID) -> Result[bool]:
        pass

    @abstractmethod
    async def get_reservation_by_id(self, reservation_id: UUID) -> Result[Reservation]:
        pass

    @abstractmethod
    async def create_reservation(self, reservation: Reservation) -> Result[Reservation]:
        pass

    @abstractmethod
    async def update_reservation(self, reservation_id: UUID, reservation: Reservation) -> Result[Reservation]:
        pass

    @abstractmethod
    async def cancel_reservation(self, reservation_id: UUID, reservation: Reservation) -> Result[Reservation]:
        pass
    


