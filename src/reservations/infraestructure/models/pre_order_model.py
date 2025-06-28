from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel,Field


class PreOrder(SQLModel, table=True):

    __tablename__ = "PreOrder"

    dish_id: Optional[UUID] = Field(
        primary_key=True,foreign_key="menus.id", default=None
    )
    reservation_id: Optional[UUID] = Field(
        primary_key=True,foreign_key="reservations.id", default=None
    )
