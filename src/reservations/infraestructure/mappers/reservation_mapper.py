from src.reservations.domain.reservation import Reservation
from src.reservations.domain.vo.reservation_dish_vo import ReservationDishVO
from src.reservations.domain.vo.reservation_schedule_vo import ReservationSchedule
from src.reservations.infraestructure.models.reservation_model import ReservationModel


class ReservationMapper:

    @staticmethod
    def to_domain(reservation_model: ReservationModel) -> Reservation:
        return Reservation.create(
            id = reservation_model.id,
            client_id = reservation_model.client_id,
            restaurant_id = reservation_model.restaurant_id,
            table_restaurant_id = reservation_model.table_id,
            reservation_schedule = ReservationSchedule.create(
                start_time=reservation_model.start_time,
                end_time=reservation_model.finish_time
            ),
            status = reservation_model.status,
            dishes = [ReservationDishVO.create(menu_id=item.id,name=item.name) for item in reservation_model.dishes]
        )

    @staticmethod
    def to_model(reservation: Reservation) -> ReservationModel:
        return ReservationModel(
            id=reservation.get_id(),
            status=reservation.get_status(),
            start_time=reservation.get_schedule().start_time,
            finish_time=reservation.get_schedule().end_time,
            client_id=reservation.get_client(),
            restaurant_id=reservation.get_restaurant(),
            table_id=reservation.get_table()
        )
