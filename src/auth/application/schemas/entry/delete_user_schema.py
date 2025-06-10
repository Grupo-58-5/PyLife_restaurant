from pydantic import BaseModel, Field
from uuid import UUID

class DeleteUserSchema(BaseModel):
    id: UUID = Field(...)