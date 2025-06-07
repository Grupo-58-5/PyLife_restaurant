import re
from uuid import UUID,uuid4
from sqlmodel import SQLModel, Field
from pydantic import field_validator
from src.auth.domain.enum.role import Roles

class UserModel(SQLModel, table=True):

    __tablename__ = "user"
    id: UUID | None = Field(primary_key=True, default_factory=uuid4,index=True)
    name: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(index=True, nullable=False)
    role: Roles = Field(default=Roles.CLIENT,nullable=False)

    @field_validator('email')
    def valid_email(cls,email: str) -> bool:
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None