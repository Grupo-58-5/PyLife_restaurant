


from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class TableModel(SQLModel):
    """Model for mesas in the database."""
    
    __tablename__ = "Mesa"

    id: UUID = Field(default_factory = uuid4, primary_key=True, index=True)
    restaurant_id: UUID = Field(foreign_key="restaurants.id", nullable=False)
    table_number: int = Field(nullable=False, gt=0)
    capacity: int = Field(nullable=False, gt=0)