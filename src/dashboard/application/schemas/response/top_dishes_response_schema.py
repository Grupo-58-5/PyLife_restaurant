


from uuid import UUID
from pydantic import BaseModel


class TopDishesResponseSchema(BaseModel):
    dish_name: str
    dish_id: UUID
    top: int
    quantity: int
