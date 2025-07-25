
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.dashboard.application.schemas.response.top_dishes_response_schema import TopDishesResponseSchema
from src.reservations.domain.reservation import Reservation
from src.reservations.domain.vo.reservation_status_vo import ReservationStatus
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
    async def create_reservation(self, reservation: Reservation) -> Result[Reservation]:
        pass

    @abstractmethod
    async def update_reservation(self, reservation_id: UUID, reservation: Reservation) -> Result[Reservation]:
        pass

    @abstractmethod
    async def cancel_reservation(self, reservation_id: UUID, reservation: Reservation) -> Result[Reservation]:
        pass
    
    @abstractmethod
    async def get_restaurant_reservations_filtered(self, restaurant_id: UUID, page: int, page_size: int, status: ReservationStatus | None, date: datetime | None) -> List[Reservation]:
        pass

    @abstractmethod
    async def get_reservation_by_id(self, reservation_id: UUID) -> Optional[Reservation]:
        """Get a reservation by its ID."""
        pass

    @abstractmethod
    async def get_top_dishes(self, restaurant_id: UUID, start_date: datetime, end_date: datetime) -> Result[List[TopDishesResponseSchema]]:
        """Get the top dishes for a restaurant within a date range."""
        pass