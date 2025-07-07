from datetime import date, datetime
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy import desc, func, text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload

from src.dashboard.application.schemas.response.top_dishes_response_schema import TopDishesResponseSchema
from src.reservations.domain.repository.reservation_repository import IReservationRepository
from src.reservations.domain.reservation import Reservation
from src.reservations.domain.vo.reservation_status_vo import ReservationStatus
from src.reservations.infraestructure.mappers.reservation_mapper import ReservationMapper
from src.reservations.infraestructure.models.pre_order_model import PreOrder
from src.reservations.infraestructure.models.reservation_model import ReservationModel
from src.restaurants.infraestructure.model.menu_model import MenuModel
from src.shared.utils.result import Result

# TODO: Reemplazar por Result en las respuestas
class ReservationRepositoryImpl(IReservationRepository):

    db: AsyncSession

    def __init__(self,db: AsyncSession):
        super().__init__()
        self.db = db

    async def get_all_restaurant_reservations(self, restaurant_id: UUID, page: int, page_size: int) -> List[Reservation]:
        offset = (page - 1) * page_size
        statement = (
            select(ReservationModel)
            .where(ReservationModel.restaurant_id == restaurant_id)
            .options(
                selectinload(ReservationModel.table),
                selectinload(ReservationModel.client),
                selectinload(ReservationModel.restaurant)
            )
            .offset(offset)
            .limit(page_size)
        )
        result: Optional[List[ReservationModel]] = (await self.db.exec(statement)).all()
        print("Lista de reservaciones: ",result)
        reservations: List[Reservation] = [ReservationMapper.to_domain(x) for x in result]

        return Result[List[Reservation]].success(reservations)

    async def get_all_users_reservations(self, client_id: UUID, page: int, page_size: int) -> Result[List[Reservation]]:
        try:
            offset = (page - 1) * page_size
            statement = (
                select(ReservationModel)
                .where(
                    ReservationModel.client_id == client_id,
                    ReservationModel.status != ReservationStatus.COMPLETED,
                    ReservationModel.status != ReservationStatus.CANCELED,
                )
                .options(
                    selectinload(ReservationModel.table),
                    selectinload(ReservationModel.client),
                    selectinload(ReservationModel.restaurant),
                    selectinload(ReservationModel.dishes)
                )
                .offset(offset)
                .limit(page_size)
            )
            result: Optional[List[ReservationModel]] = (await self.db.exec(statement)).all()
            print("Lista de reservaciones: ",result)

            reservations: List[Reservation] = [ReservationMapper.to_domain(x) for x in result]

            return Result[List[Reservation]].success(reservations)
        except BaseException as e:
            print(f"Error {e}")
            return Result[bool].failure(e,str(e),500)

    async def get_reservations_by_date(self, date: datetime) -> List[Reservation]:
        pass

    async def verify_reservations_by_date_and_user(self, start_time: datetime, finish_time: datetime, client_id: UUID) -> Result[bool]:
        try:
            statement = (
                select(ReservationModel)
                .where(
                    ReservationModel.client_id == client_id,
                    ReservationModel.status != ReservationStatus.COMPLETED,
                    ReservationModel.status != ReservationStatus.CANCELED,
                    start_time.replace(tzinfo=None) <= ReservationModel.finish_time,
                    finish_time.replace(tzinfo=None) > ReservationModel.start_time,
                )
            )
            result: Optional[List[ReservationModel]] = (await self.db.exec(statement)).all()
            print("Lista de reservaciones: ",result)

            if result is None or len(result) == 0:
                return Result[bool].success(True)

            return Result[bool].success(result)
        except BaseException as e:
            return Result[bool].failure(e,'Failed query',500)

    async def verify_reservations_by_date_and_table(self, restaurant_id: UUID, start_time: datetime, finish_time: datetime,table_id: UUID) -> Result[bool]:

        try:
            statement = (
                select(ReservationModel)
                .where(
                    ReservationModel.restaurant_id == restaurant_id,
                    ReservationModel.table_id == table_id,
                    ReservationModel.status != ReservationStatus.COMPLETED,
                    ReservationModel.status != ReservationStatus.CANCELED,
                    start_time.replace(tzinfo=None) <= ReservationModel.finish_time,
                    finish_time.replace(tzinfo=None) > ReservationModel.start_time,
                )
            )
            result: Optional[List[ReservationModel]] = (await self.db.exec(statement)).all()
            print("Lista de reservaciones: ",result)

            if result is None or len(result) == 0:
                return Result[bool].success(True)

            return Result[bool].success(False)
        except BaseException as e:
            print(f"Error {e}")
            return Result[bool].failure(e,'Failed query',500)

    async def create_reservation(self, reservation: Reservation) -> Result[Reservation]:
        try:
            reservation_model: ReservationModel = ReservationMapper.to_model(reservation)
            self.db.add(reservation_model)
            await self.db.commit()
            await self.db.refresh(reservation_model)
            for dish in reservation.get_dishes() or []:

                pre_order = PreOrder(
                    dish_id=dish.get_menu_id(),
                    reservation_id=reservation.get_id()
                )
                self.db.add(pre_order)
                await self.db.commit()
                await self.db.refresh(pre_order)
            return Result[Reservation].success(reservation)
        except BaseException as e:
            print(f"Error {e}")
            return Result[Reservation].failure(e,f"Failed insert in Reservation Table: {str(e)}",500)

    async def update_reservation(self, reservation_id: UUID, reservation: Reservation) -> Result[Reservation]:
        try:
            statement = (
                select(ReservationModel)
                .where(
                    ReservationModel.id == reservation_id
                )
                .options(
                    selectinload(ReservationModel.table),
                    selectinload(ReservationModel.client),
                    selectinload(ReservationModel.restaurant),
                    selectinload(ReservationModel.dishes)
                )
            )
            reservation_model: Optional[ReservationModel] = (await self.db.exec(statement)).one_or_none()
            if reservation_model is None:
                return Result[Reservation].failure(BaseException,'Reservation Not Found',404)

            reservation_model.status = reservation.get_status()
            reservation_model.start_time = reservation.get_schedule().start_time
            reservation_model.finish_time = reservation.get_schedule().end_time
            await self.db.commit()
            await self.db.refresh(reservation_model)
            print("Reservasion actualizada: ",reservation_model)
            return Result[Reservation].success(ReservationMapper.to_domain(reservation_model))
        except BaseException as e:
            return Result.failure(e,str(e),500)

    async def cancel_reservation(self, reservation_id: UUID, reservation: Reservation) -> Result[Reservation]:
        try:
            statement = (
                select(ReservationModel)
                .where(
                    ReservationModel.id == reservation_id
                )
                .options(
                    selectinload(ReservationModel.table),
                    selectinload(ReservationModel.client),
                    selectinload(ReservationModel.restaurant),
                    selectinload(ReservationModel.dishes)
                )
            )
            reservation_model: Optional[ReservationModel] = (await self.db.exec(statement)).one_or_none()
            reservation_model.status = reservation.get_status()
            await self.db.commit()
            await self.db.refresh(reservation_model)
            return Result[Reservation].success(ReservationMapper.to_domain(reservation_model))
        except BaseException as e:
            return Result.failure(e,str(e),500)


    ## ? This method will return a list of reservations filtered by status and date 
    async def get_restaurant_reservations_filtered(self, restaurant_id: UUID, page: int, page_size: int, status: ReservationStatus | None, date: datetime | None) -> list[Reservation]:
        try:
            offset = (page - 1) * page_size
            statement = (
                select(ReservationModel)
                .where(
                    ReservationModel.restaurant_id == restaurant_id,
                    ReservationModel.status == status.value.upper() if status else True,
                    ReservationModel.start_time >= date if date else True
                )
                .options(
                    selectinload(ReservationModel.table),
                    selectinload(ReservationModel.client),
                    selectinload(ReservationModel.restaurant),
                    selectinload(ReservationModel.dishes)
                )
                .offset(offset)
                .limit(page_size)
            )
            result: Optional[List[ReservationModel]] = (await self.db.exec(statement)).all()

            reservations: List[Reservation] = [ReservationMapper.to_domain(x) for x in result if x is not None]
            return reservations
        except BaseException as e:
            print(f"Error {e}")
    
    async def get_reservation_by_id(self, reservation_id: UUID) -> Optional[Reservation]:
        try:
            statement = (
                select(ReservationModel)
                .where(
                    ReservationModel.id == reservation_id
                )
                .options(
                    selectinload(ReservationModel.table),
                    selectinload(ReservationModel.client),
                    selectinload(ReservationModel.restaurant),
                    selectinload(ReservationModel.dishes)
                )
            )
            result: Optional[ReservationModel] = (await self.db.exec(statement)).one_or_none()
            if result is None:
                return None
            return ReservationMapper.to_domain(result)
        except BaseException as e:
            print(f"Error {e}")
            return None
        

    async def get_top_dishes(
        self, 
        restaurant_id: UUID, 
        start_date: datetime, 
        end_date: datetime
    ) -> Result[List[TopDishesResponseSchema]]:
        try:
            # consulta con sqlAlchemy
            if start_date is None or end_date is None:
                return Result.failure(
                    ValueError("Start date and end date must be provided"),
                    "Start date and end date are required",
                    400
                )
            if start_date > end_date:
                return Result.failure(
                    ValueError("Start date cannot be after end date"),
                    "Start date must be before end date",
                    400
                )
            # Consulta para obtener los platos más pedidos en un restaurante en un rango de fechas
            query = text("""
                SELECT d.id as dish_id, d.name as dish_name, COUNT(*) as quantity
                FROM reservations r, menus d, public."PreOrder" p
                WHERE :restaurant_id = r.restaurant_id
                AND r.id = p.reservation_id
                AND p.dish_id = d.id
                GROUP BY d.id, d.name
                ORDER BY quantity DESC
                LIMIT 5
            """)

            result = await self.db.execute(query, {"restaurant_id": str(restaurant_id)})
            result = result.all()
            print("Top dishes result: ", result)

            response: List[TopDishesResponseSchema] = [
                TopDishesResponseSchema(
                    dish_id=menu.dish_id,
                    dish_name=menu.dish_name,
                    quantity=menu.quantity,
                    top= index + 1
                ) for index, menu in enumerate(result)
            ]

            return Result[List[TopDishesResponseSchema]].success(response)

        except Exception as e:
            print(f"Error: {str(e)}")
            return Result.failure(e, "Failed to fetch top dishes", 500)

    async def get_reservations_grouped_by_day(self, start_date: date, end_date: date) -> List[Tuple[date, int]]:
        statement = (
            select(func.date(ReservationModel.date), func.count(ReservationModel.id))
            .where(ReservationModel.date >= start_date, ReservationModel.date <= end_date)
            .group_by(func.date(ReservationModel.date))
            .order_by(func.date(ReservationModel.date))
        )
        results = await self.db.exec(statement)
        return results.all()  # List of tuples (date, count)
