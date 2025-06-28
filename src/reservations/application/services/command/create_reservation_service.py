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
        repo_menu: IMenuRepository
    ):
        self.repository = reservation_repository
        self.repo_menu = repo_menu

    #TODO: Pre ordernar los menus
    async def execute(self, data: ReservationSchemaEntry) -> Result[ReservationSchemaResponse]:
        try:

            menu: List[ReservationDishVO] = []
            for menu_id in data.dishes:
                item = await self.repo_menu.get_menu_resturant(menu_id,data.restaurant_id)
                if item.is_error() is True:
                    return Result[ReservationSchemaResponse].failure(item.error,item.get_error_message(),item.get_error_code())
                menu.append(ReservationDishVO.create(menu_id=item.value.get_id(),name=item.value.get_name()))

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
                menu if len(menu) > 0 else None
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
                pre_order=[PreOrderSchemaResponse(id=item.get_menu_id(),name=item.get_name()) for item in menu] if len(menu) > 0 else None
            )
            return Result[ReservationSchemaResponse].success(response)
        except Exception as e:
            raise Exception(f"Error creating reservation: {str(e)}") from e