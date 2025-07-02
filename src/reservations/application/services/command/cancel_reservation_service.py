from src.reservations.application.schemas.entry.cancel_reservation_schema_entry import CancelReservationSchemaEntry
from src.reservations.domain.repository.reservation_repository import IReservationRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result

class CancelReservationService(IApplicationService[CancelReservationSchemaEntry, Result[str]]):

    def __init__(self, repo_reservation: IReservationRepository):
        super().__init__()
        self.repo_reservation = repo_reservation

    async def execute(self, data: CancelReservationSchemaEntry) -> Result[str]:

        try:
            find_reservation = await self.repo_reservation.get_reservation_by_id(data.reservation_id)
            if find_reservation is None:
                return Result[str].failure(BaseException,f"Reservation not found",404)

            reservation = find_reservation
            if reservation.get_client() != data.client_id:
                return Result[str].failure(Exception,'Reservation not belonging to the user',403)
            reservation.cancel_reservation()

            update = await self.repo_reservation.cancel_reservation(data.reservation_id,reservation)
            if update.is_error() is True:
                return Result[str].failure(update.error,update.get_error_message(),update.get_error_code())

            return Result[str].success("Reservantion canceled")
        except Exception as e:
            return Result[str].failure(e,str(e),500)