


from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4


if TYPE_CHECKING:
    # Referencias de tipo para evitar ciclos
    from .restaurant_model import RestaurantModel

class TableModel(SQLModel, table=True):
    """Model for mesas in the database."""
    __tablename__ = "tables"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    table_number: int = Field(nullable=False, gt=0)
    capacity: int = Field(nullable=False, gt=0)
    location: Optional[str] = Field(default=None, nullable=True)

    restaurant_id: UUID | None = Field(default=None, foreign_key="restaurants.id")
    restaurant: Optional["RestaurantModel"] = Relationship(back_populates="tables")