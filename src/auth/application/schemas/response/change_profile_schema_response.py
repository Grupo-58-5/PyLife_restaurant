from pydantic import BaseModel


class ChangeProfileSchemaResponse(BaseModel):

    name: str | None
    email: str | None
    password: str | None