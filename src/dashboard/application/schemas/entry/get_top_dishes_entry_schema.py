



from datetime import datetime
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel, Field


class GetTopDishesEntrySchema(BaseModel):
    restaurant_id: UUID
    start_date: datetime = Field(
        default='2025-01-01',
        example="2025-01-01"
    )
    end_date: datetime= Field(
        default='2025-07-01',                      
        example="2025-07-01"
    )

    ## ? validate end_date is after start_date
    def validate_dates(self):
        if self.start_date >= self.end_date:
            raise HTTPException(
                status_code=400,
                detail="End date must be after start date"
            )
    
    def __init__(self, **data):
        super().__init__(**data)
        self.validate_dates()
