


from uuid import uuid4
from PyLife_restaurant.src.reservations.application.schemas.entry.reservation_schema_entry import ReservationSchemaEntry
from PyLife_restaurant.src.reservations.application.schemas.response.reservation_schema_response import ReservationSchemaResponse
from PyLife_restaurant.src.reservations.domain.repository.reservation_repository import IReservationRepository
from PyLife_restaurant.src.reservations.domain.reservation import Reservation
from src.shared.utils.i_application_service import IApplicationService


class CreateReservationService(IApplicationService[ReservationSchemaEntry, ReservationSchemaResponse]):
    def __init__(self, restaurant_repository: IReservationRepository):
        self.repository = restaurant_repository

    async def execute(self, data: ReservationSchemaEntry) -> ReservationSchemaResponse:
        try:
            reservation_id = uuid4()

            reservation = Reservation(
                id = reservation_id,
                client_id = data.client_id,
                restaurant_id = data.restaurant_id,
                table_id = data.table_id,  
                start_time = data.start_time,
                finish_time = data.finish_time,
                status = data.status
            )

            await self.repository.create_reservation(reservation)

            return ReservationSchemaResponse(
                client_id = reservation.client_id,
                restaurant_id = reservation.restaurant_id,
                table_id = reservation.table_id,
                start_time = reservation.start_time,
                finish_time = reservation.finish_time,
                status = reservation.status
            )
        except Exception as e:
            raise Exception(f"Error creating reservation: {str(e)}") from e