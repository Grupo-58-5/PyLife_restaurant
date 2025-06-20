
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel
from src.restaurants.infraestructure.model.table_model import TableModel

from src.restaurants.infraestructure.model.menu_model import MenuModel


from src.shared.db.database import engine
from sqlmodel import SQLModel

# async def create_tables():
#     SQLModel.metadata.create_all(engine)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)