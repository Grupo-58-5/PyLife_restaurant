
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel

#from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel

if TYPE_CHECKING:
    from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel



class MenuModel(SQLModel, table=True):

    """
    Model for the Menu entity. It represents a menu in the database.
    """
    __tablename__ = "menus"
    
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True, nullable=False)
    description: str = Field(nullable=False)
    category: str = Field(index=True,nullable=False)
    available: bool = Field(default=True, nullable=True)

    restaurant_id: UUID = Field(foreign_key="restaurants.id", nullable=False)
    restaurant: Optional["RestaurantModel"] = Relationship(back_populates="menu_items")