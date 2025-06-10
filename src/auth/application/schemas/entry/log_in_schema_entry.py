from pydantic import BaseModel, Field

class LogInSchemaEntry(BaseModel):

    email: str = Field(...)
    password: str = Field(...)