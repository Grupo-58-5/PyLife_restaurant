from typing import List
from uuid import UUID, uuid4
from src.auth.domain.repository.user_repository_interface import IUserRepository
from src.reservations.application.schemas.entry.reservation_schema_entry import ReservationSchemaEntry
from src.reservations.application.schemas.response.reservation_schema_response import PreOrderSchemaResponse, ReservationSchemaResponse
from src.reservations.domain.repository.reservation_repository import IReservationRepository
from src.reservations.domain.reservation import Reservation
from src.reservations.domain.vo.reservation_dish_vo import ReservationDishVO
from src.reservations.domain.vo.reservation_schedule_vo import ReservationSchedule
from src.reservations.domain.vo.reservation_status_vo import ReservationStatus
from src.restaurants.domain.entity.table_entity import TableEntity
from src.restaurants.domain.repository.i_menu_repository import IMenuRepository
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.repository.i_table_repository import ITableRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class CreateReservationService(IApplicationService[ReservationSchemaEntry, Result[ReservationSchemaResponse]]):
    def __init__(
        self,
        reservation_repository: IReservationRepository,
        restaurant_repository: IRestaurantRepository
    ):
        self.repository = reservation_repository
        self.restaurant_repository = restaurant_repository

    #TODO: Pre ordernar los menus
    async def execute(self, data: ReservationSchemaEntry) -> Result[ReservationSchemaResponse]:
        try:

            restaurant = await self.restaurant_repository.get_restaurant_by_id(data.restaurant_id)
            if restaurant is None:
                return Result[ReservationSchemaResponse].failure(BaseException,f"Restaurant not found",404)

            pre_order: List[ReservationDishVO] = []

            for menu_id in data.dishes or []:
                item = next((i for i in restaurant.get_menu() if i.get_id == menu_id), None)

                if item is None:
                    return Result[ReservationSchemaResponse].failure(Exception,f'Dish #{menu_id} does not belong to the restaurant menu)',400) 
                pre_order.append(ReservationDishVO.create(menu_id=item.get_id,name=item.get_name()))

            verify_reservation: Result[bool] = await self.repository.verify_reservations_by_date_and_table(
                restaurant_id=data.restaurant_id,
                start_time=data.start_time,
                finish_time=data.finish_time,
                table_id=data.table_id
            )

            if verify_reservation.is_error() is True:
                return Result[ReservationSchemaResponse].failure(verify_reservation.error,verify_reservation.get_error_message(),verify_reservation.get_error_code())
            elif verify_reservation.value is False:
                return Result[ReservationSchemaResponse].failure(BaseException,'Table not available',409)

            verify_reservations_user: Result[bool] = await self.repository.verify_reservations_by_date_and_user(
                start_time=data.start_time,
                finish_time=data.finish_time,
                client_id=data.client_id
            )
            if verify_reservations_user.is_error() is True:
                return Result[ReservationSchemaResponse].failure(verify_reservations_user.error,verify_reservations_user.get_error_message(),verify_reservations_user.get_error_code())
            elif verify_reservations_user.value is False:
                return Result[ReservationSchemaResponse].failure(BaseException,'Client with pending reservation at that time',409)

            reservation_id: UUID = uuid4()

            reservation = Reservation.create(
                reservation_id,
                data.client_id,
                data.restaurant_id,
                data.table_id,
                ReservationStatus.PENDING,
                ReservationSchedule.create(
                    start_time=data.start_time.replace(tzinfo=None),
                    end_time=data.finish_time.replace(tzinfo=None)
                ),
                pre_order if len(pre_order) > 0 else None
            )

            result = await self.repository.create_reservation(reservation)
            if result.is_error() is True:
                return Result[ReservationSchemaResponse].failure(result.error,result.get_error_message(),result.get_error_code())

            response = ReservationSchemaResponse(
                reservation_id = reservation_id,
                client_id = reservation.get_client(),
                restaurant_id = reservation.get_restaurant(),
                table_id = reservation.get_table(),
                start_time = reservation.get_schedule().start_time,
                finish_time = reservation.get_schedule().end_time,
                status = reservation.get_status(),
                pre_order=[PreOrderSchemaResponse(id=item.get_menu_id(),name=item.get_name()) for item in pre_order] if len(pre_order) > 0 else None
            )
            return Result[ReservationSchemaResponse].success(response)
        except Exception as e:
            raise Exception(f"Error creating reservation: {str(e)}") from e