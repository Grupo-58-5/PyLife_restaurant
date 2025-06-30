


from src.reservations.application.schemas.entry.reservation_schema_entry import ChangeStatusSchemaEntry
from src.reservations.application.schemas.response.reservation_schema_response import PreOrderSchemaResponse, ReservationSchemaResponse
from src.reservations.domain.repository.reservation_repository import IReservationRepository
from src.reservations.domain.vo.reservation_status_vo import ReservationStatus
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class ChangeReservationStatusApplicationService(IApplicationService[tuple[str, ChangeStatusSchemaEntry], Result[ReservationSchemaResponse]]):

    def __init__(self, repo_reservation: IReservationRepository):
        super().__init__()
        self.repo_reservation = repo_reservation

    async def execute(self, data: tuple[str, ChangeStatusSchemaEntry]) -> Result[ReservationSchemaResponse]:
        reservation_id, change_status = data

        try:
            reservation = await self.repo_reservation.get_reservation_by_id(reservation_id)
            if reservation is None:
                return Result[ReservationSchemaResponse].failure(
                    error=ValueError("Reservation not found"),
                    messg="The reservation with the provided ID does not exist.",
                    code=404
                )

            reservation.change_status(ReservationStatus[change_status.status.upper()])

            print(f"Changing status of reservation {reservation_id} to {change_status.status}")
            updated_reservation = await self.repo_reservation.update_reservation(reservation_id, reservation)
            if updated_reservation.is_error():
                return Result[ReservationSchemaResponse].failure(updated_reservation.error, updated_reservation.get_error_message(), updated_reservation.get_error_code())

            updated_reservation = updated_reservation.result()
            return Result[ReservationSchemaResponse].success(
                ReservationSchemaResponse(
                    reservation_id=updated_reservation.get_id(),
                    client_id=updated_reservation.get_client(),
                    restaurant_id=updated_reservation.get_restaurant(),
                    table_id=updated_reservation.get_table(),
                    start_time=updated_reservation.get_schedule().start_time,
                    finish_time=updated_reservation.get_schedule().end_time,
                    status=updated_reservation.get_status(),
                    pre_order=[
                        PreOrderSchemaResponse(
                            id=p.get_menu_id(),
                            name=p.get_name()
                        ) for p in updated_reservation.get_dishes()
                    ],
                )
            )
        except ValueError as ve:
            return Result[ReservationSchemaResponse].failure(ve, str(ve), 400)
        except Exception as e:
            return Result[ReservationSchemaResponse].failure(e, str(e), 500)