from pydantic import BaseModel,Field
from src.auth.domain.enum.role import Roles

class SignUpResponse(BaseModel):
    role: Roles = Field(...,index=True)
    message: str = Field(...,index=True)

    model_config = {
        "extra": "ignore"
    }