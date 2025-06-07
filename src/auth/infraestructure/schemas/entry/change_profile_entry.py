import re
from pydantic import BaseModel,Field, field_validator, ValidationError
from fastapi import HTTPException

class ChangeProfileEntry(BaseModel):

    name: str | None = Field(default=None,min_length=3,examples=['John Doe'])
    email: str | None = Field(default=None,examples=['johndoe@gmail.com'])
    password: str | None = Field(default=None)

    @field_validator('email')
    def valid_email(cls,email: str) -> bool:
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            raise HTTPException(status_code=409,detail={'msg':'Wrong email format'})
        return email