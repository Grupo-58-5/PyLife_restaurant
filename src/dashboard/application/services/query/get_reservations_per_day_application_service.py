

from datetime import date
from typing import Tuple, List
from src.shared.utils.result import Result

from src.shared.utils.i_application_service import IApplicationService
from src.dashboard.application.schemas.response.reservations_per_day_response import ReservationsPerDayItemResponse
from src.reservations.infraestructure.repository.reservation_repository_impl import ReservationRepositoryImpl

class GetReservationsPerDayApplicationService(IApplicationService[Tuple[date, date, str], Result[List[ReservationsPerDayItemResponse]]]):
    def __init__(self, reservation_repo: ReservationRepositoryImpl):
        self.reservation_repo = reservation_repo

    async def execute(self, date_range: Tuple[date, date, str]) -> Result[List[ReservationsPerDayItemResponse]]:
        start, end, group_by = date_range
        try:
            if group_by == "day":
                data = await self.reservation_repo.get_reservations_grouped_by_day("day", start, end)
            elif group_by == "week":
                data = await self.reservation_repo.get_reservations_grouped_by_day("week", start, end)
            else:
                return Result.failure(None, "Invalid grouping", 422)

            result = [ReservationsPerDayItemResponse(period=str(key), count=value) for key, value in data]
            return Result.success(result)
        except Exception as e:
            return Result.failure(
                error=e,
                messg=f"Error retrieving reservations per day: {e}",
                code=500
            )