

from datetime import date
from typing import Tuple, List
from src.shared.utils.result import Result

from src.shared.utils.i_application_service import IApplicationService
from src.dashboard.application.schemas.response.reservations_per_day_response import ReservationsPerDayItemResponse
from src.reservations.infraestructure.repository.reservation_repository_impl import ReservationRepositoryImpl

class GetReservationsPerDayApplicationService(IApplicationService[Tuple[date, date], Result[List[ReservationsPerDayItemResponse]]]):
    def __init__(self, reservation_repo: ReservationRepositoryImpl):
        self.reservation_repo = reservation_repo

    async def execute(self, date_range: Tuple[date, date]) -> Result[List[ReservationsPerDayItemResponse]]:
        try:
            start, end = date_range
            raw_data = await self.reservation_repo.get_reservations_grouped_by_day(start, end)
            result = [ReservationsPerDayItemResponse(date=day, count=count) for day, count in raw_data]
            return Result.success(result)
        except Exception as e:
            return Result.failure(
                error=e,
                messg=f"Error retrieving reservations per day: {e}",
                code=500
            )