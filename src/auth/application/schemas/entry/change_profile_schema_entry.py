from pydantic import BaseModel, Field

class ChangeProfileSchemaEntry(BaseModel):

    id: str = Field(...)
    name: str | None
    email: str | None
    password: str | None