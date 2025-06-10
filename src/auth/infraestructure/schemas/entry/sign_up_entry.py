import re
from pydantic import BaseModel,Field, field_validator, ValidationError
from fastapi import HTTPException

class SignUpEntry(BaseModel):
    name: str = Field(...,min_length=3,examples=['John Doe'])
    email: str = Field(...,examples=['johndoe@gmail.com'])
    password: str = Field(...)

    @field_validator('email')
    def valid_email(cls,email: str) -> bool:
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            raise HTTPException(status_code=409,detail={'msg':'Wrong email format'})
        return email