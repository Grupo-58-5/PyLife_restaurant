


from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.reservations.infraestructure.models.reservation_model import ReservationModel
from src.restaurants.domain.entity.table_entity import TableEntity
from src.restaurants.domain.repository.i_table_repository import ITableRepository
from src.restaurants.domain.restaurant import Restaurant
from src.restaurants.infraestructure.mappers.restaurant_mapper import TableMapper
from src.restaurants.infraestructure.model.table_model import TableModel
from src.shared.utils.result import Result
from sqlalchemy.orm import selectinload


class TableRepositoryImpl(ITableRepository):

    """
    Implementation of the ITableRepository interface.
    This class is responsible for managing the table data.
    """

    def __init__(self, db : AsyncSession):
        super().__init__()
        self.db = db

    async def get_table(self, restaurant_id: UUID) -> List[TableEntity]:

        statement = (
            select(TableModel)
            .where(TableModel.restaurant_id == restaurant_id)
            .where(TableModel.is_active == True)  # Assuming we only want active tables
        )
        table_model = (await self.db.exec(statement)).all()
        return [TableMapper.to_domain(t) for t in table_model]


    async def get_table_by_id(self, table_id: UUID) -> Result[TableEntity]:
        try:
            statement = (
                select(TableModel).
                where(TableModel.id == table_id)
                .options(
                    selectinload(TableModel.reservations),
                    selectinload(TableModel.restaurant)
                )
            )
            table_model = (await self.db.exec(statement)).one_or_none()
            if not table_model:
                return Result.failure(
                    error=ValueError(f"Table with id {table_id} not found"),
                    messg=f"Table with id {table_id} not found"
                )
            return Result.success(TableMapper.to_domain(table_model))
        except Exception as e:
            return Result.failure(error=e, messg="Error retrieving table by id")

    async def create_item_table(self, table_data: TableEntity, restaurant_id: UUID) -> Result[TableEntity]:
        try:
            table_model = TableMapper.to_model(table_data)
            table_model.restaurant_id = restaurant_id
            self.db.add(table_model)
            await self.db.commit()
            await self.db.refresh(table_model)
            return Result.success(TableMapper.to_domain(table_model))
        except Exception as e:
            return Result.failure(error=e, messg="Error saving table")

    async def update_item_table(self, table_id: UUID, table_data: TableEntity) -> Result[TableEntity]:
        try:
            statement = select(TableModel).where(TableModel.id == table_id)
            table_model = (await self.db.exec(statement)).one_or_none()
            if not table_model:
                return Result.failure(
                    error=ValueError(f"Table with id {table_id} not found"),
                    messg=f"Table with id {table_id} not found"
                )
            table_model.table_number = table_data.table_number
            table_model.capacity = table_data.seats
            table_model.location = table_data.location.value if hasattr(table_data.location, "value") else table_data.location
            self.db.add(table_model)
            await self.db.commit()
            await self.db.refresh(table_model)
            return Result.success(TableMapper.to_domain(table_model))
        except Exception as e:
            return Result.failure(error=e, messg="Error updating table")

    ## ? this will delete the table from the database if it is not used in any reservation
    async def delete_item_table_or_disable(self, table_id: UUID) -> Result[bool]:
        try:
            check_statement = select(ReservationModel).where(ReservationModel.table_id == table_id)
            reservation_model = (await self.db.exec(check_statement)).one_or_none()
            result_table = await self.db.exec(select(TableModel).where(TableModel.id == table_id))
            table_model = result_table.one_or_none()
            
            if not table_model:
                return Result.failure(
                    error=ValueError(f"Table with id {table_id} not found"),
                    messg=f"Table with id {table_id} not found",
                    code=404
                )
            if reservation_model is not None:
                #? if the table is used in a reservation, we can disable it instead of deleting
                
                table_model.is_active = False  # Assuming there is an is_active field to disable the table
                self.db.add(table_model)
                await self.db.commit()
                return Result.success(True)
            else:
                await self.db.delete(table_model)
                await self.db.commit()
                return Result.success(True)
        except Exception as e:
            print('Error aqui: ', e)
            return Result.failure(error=e, messg="Error deleting table")
