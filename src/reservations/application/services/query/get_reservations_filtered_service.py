


from src.reservations.application.schemas.entry.get_application_schema_entry import GetReservationsSchemaEntry
from src.reservations.application.schemas.response.reservation_schema_response import AllReservationsResponse, ReservationResponse
from src.reservations.domain.repository.reservation_repository import IReservationRepository
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class GetReservationsFilteredApplicationService(IApplicationService[tuple[str, GetReservationsSchemaEntry], Result[AllReservationsResponse]]):

    def __init__(self, reservation_repo: IReservationRepository, restaurant_repo: IRestaurantRepository):
        super().__init__()
        self.reservation_repo = reservation_repo
        self.restaurant_repo = restaurant_repo

    async def execute(self, data: tuple[str, GetReservationsSchemaEntry]) -> Result[AllReservationsResponse]:
        try:
            restaurant_id, entry = data


            restaurant = await self.restaurant_repo.get_restaurant_by_id(restaurant_id)
            if restaurant is None:
                return Result[AllReservationsResponse].failure(
                    ValueError("Restaurant not found"),
                    f"The restaurant with the provided {restaurant_id} does not exist." ,
                    404
                )
            
            reservations = await self.reservation_repo.get_restaurant_reservations_filtered(
                restaurant_id=restaurant_id,
                page=entry.page,
                page_size=entry.page_size,
            )

            if entry.reservation_status:
                print(f"Filtering reservations by status: {entry.reservation_status.value}")
                print(reservations[0].get_status())
                reservations = [res for res in reservations if res.get_status().value == entry.reservation_status.value]
            if entry.date:
                reservations = [res for res in reservations if res.get_schedule().start_time.date() >= entry.date.date()]

            return Result[AllReservationsResponse].success(
                AllReservationsResponse(
                    restaurant_id=restaurant_id,
                    restaurant_name=restaurant.get_name(),
                    reservations=[
                        ReservationResponse(
                            id=reservation.get_id(),
                            client_id=reservation.get_client(),
                            table_id=reservation.get_table(),
                            start_time=reservation.get_schedule().start_time,
                            finish_time=reservation.get_schedule().end_time,
                            status=reservation.get_status().value,
                        ) for reservation in reservations  
                    ] 
                )
            )
        except Exception as e:
            return Result[AllReservationsResponse].failure(
                e,
                str(e),
                500
            )
