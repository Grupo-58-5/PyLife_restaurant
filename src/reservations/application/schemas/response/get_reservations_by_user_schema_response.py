from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from src.reservations.domain.vo.reservation_status_vo import ReservationStatus

class TableResponse(BaseModel):
    table_id: str = Field(...,examples=['3fa85f64-5717-4562-b3fc-2c963f66afa6'])
    table_number: int = Field(...,examples=[1])
    seats: int = Field(...,examples=[2])
    location: str = Field(examples=['INDOOR'])

class RestaurantResponse(BaseModel):
    restaurant_id: str
    restaurant_name: str

class PreOrderSchemaResponse(BaseModel):
    id: str = Field(...,examples=['3fa85f64-5717-4562-b3fc-2c963f66afa6'])
    name: str

class GetReservationsByUserSchemaResponse(BaseModel):

    reservation_id: str = Field(...,examples=['3fa85f64-5717-4562-b3fc-2c963f66afa6'])
    start_time: datetime = Field(...)
    finish_time: datetime = Field(...)
    status: ReservationStatus = Field(...)
    restaurant: RestaurantResponse = Field(...)
    table: TableResponse = Field(...)
    pre_order: Optional[List[PreOrderSchemaResponse]] = Field(default=None)
