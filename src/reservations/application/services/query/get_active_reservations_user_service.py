from typing import List
from src.reservations.application.schemas.entry.get_reservations_by_user_schema_entry import GetReservationsByUserSchemaEntry
from src.reservations.application.schemas.response.get_reservations_by_user_schema_response import GetReservationsByUserSchemaResponse, RestaurantResponse, TableResponse, PreOrderSchemaResponse
from src.reservations.domain.repository.reservation_repository import IReservationRepository
from src.reservations.domain.reservation import Reservation
from src.restaurants.domain.repository.i_menu_repository import IMenuRepository
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.repository.i_table_repository import ITableRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result

class GetActiveReservationsUserService(IApplicationService[GetReservationsByUserSchemaEntry,Result[List[GetReservationsByUserSchemaResponse]]]):

    def __init__(self, repo_reservation: IReservationRepository, repo_table: ITableRepository, repo_restaurant: IRestaurantRepository):
        super().__init__()
        self.repo_reservation = repo_reservation
        self.repo_restaurant = repo_restaurant
        self.repo_table = repo_table

    async def execute(self, data: GetReservationsByUserSchemaEntry) -> Result[List[GetReservationsByUserSchemaResponse]]:

        reservations: Result[List[Reservation]] = await self.repo_reservation.get_all_users_reservations(
            client_id=data.client_id,
            page=data.skip,
            page_size=data.limit
        )

        if reservations.is_error() is True:
            return Result[List[Reservation]].failure(reservations.error,reservations.get_error_message(),reservations.get_error_code())

        response: List[GetReservationsByUserSchemaResponse] = []
        for r in reservations.value:
            restaurant = await self.repo_restaurant.get_restaurant_by_id(r.get_restaurant())
            restaurant_response = RestaurantResponse.model_validate({
                "restaurant_id": str(restaurant.get_id()),
                "restaurant_name": restaurant.get_name()
            })
            table = await self.repo_table.get_table_by_id(r.get_table())
            table_response = TableResponse.model_validate({
                "table_id": str(table.value.get_id()),
                "table_number": table.value.get_table_number(),
                "seats": table.value.get_seats(),
                "location": table.value.get_location()
            })
            menu = [PreOrderSchemaResponse.model_validate({"id": str(item.get_menu_id()),"name": item.get_name()}) for item in r.get_dishes()]
            response.append(GetReservationsByUserSchemaResponse.model_validate({
                "reservation_id": str(r.get_id()),
                "start_time": r.get_schedule().start_time,
                "finish_time": r.get_schedule().end_time,
                "status": r.get_status(),
                "restaurant": restaurant_response,
                "table": table_response,
                "pre_order": menu if len(menu) > 0 else None
            }))

        return Result[List[GetReservationsByUserSchemaResponse]].success(response)