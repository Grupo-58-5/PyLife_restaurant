


from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

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

    def __init__(self, db : Session):
        super().__init__()
        self.db = db

    async def get_table(self, restaurant_id: UUID) -> List[TableEntity]:

        statement = statement = (
            select(TableModel)
            .where(TableModel.restaurant_id == restaurant_id)
        )    
        table_model = self.db.exec(statement).all()
        return [TableMapper.to_domain(t) for t in table_model] 
    


    async def get_table_by_id(self, table_id: UUID) -> Result[TableEntity]:
        try:
            statement = select(TableModel).where(TableModel.id == table_id)
            table_model = self.db.exec(statement).one_or_none()
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
            self.db.commit()
            self.db.refresh(table_model)
            return Result.success(TableMapper.to_domain(table_model))
        except Exception as e:
            return Result.failure(error=e, messg="Error saving table")

    async def update_item_table(self, table_id: UUID, table_data: TableEntity) -> Result[TableEntity]:
        try:
            statement = select(TableModel).where(TableModel.id == table_id)
            table_model = self.db.exec(statement).one_or_none()
            if not table_model:
                return Result.failure(
                    error=ValueError(f"Table with id {table_id} not found"),
                    messg=f"Table with id {table_id} not found"
                )
            table_model.table_number = table_data.table_number
            table_model.capacity = table_data.seats
            table_model.location = table_data.location.value if hasattr(table_data.location, "value") else table_data.location
            self.db.add(table_model)
            self.db.commit()
            self.db.refresh(table_model)
            return Result.success(TableMapper.to_domain(table_model))
        except Exception as e:
            return Result.failure(error=e, messg="Error updating table")

    async def delete_item_table(self, table_id: UUID) -> Result[bool]:
        try:
            statement = select(TableModel).where(TableModel.id == table_id)
            table_model = self.db.exec(statement).one_or_none()
            if not table_model:
                return Result.failure(
                    error=ValueError(f"Table with id {table_id} not found"),
                    messg=f"Table with id {table_id} not found"
                )
            self.db.delete(table_model)
            self.db.commit()
            return Result.success(True)
        except Exception as e:
            return Result.failure(error=e, messg="Error deleting table")
