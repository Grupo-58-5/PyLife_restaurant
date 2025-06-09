from pydantic import BaseModel, Field

class LogInSchemaResponse(BaseModel):
    token: str