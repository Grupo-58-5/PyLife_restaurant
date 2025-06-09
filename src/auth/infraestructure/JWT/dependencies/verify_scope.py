from fastapi import Depends, HTTPException, status, Request
from typing import List

from src.auth.infraestructure.repository.user_repository_impl import UserRepositoryImpl
from src.auth.infraestructure.JWT.JWT_auth_adapter import JWTAuthAdapter
from src.auth.domain.user import User

class VerifyScope:

    jwt_handler: JWTAuthAdapter

    def __init__(self, scopes: List[str] | None, jwt_handler: JWTAuthAdapter | None = None):
        self.scopes = scopes
        self.jwt_handler = jwt_handler

    async def __call__(self, request: Request):
        header = request.headers.get("Authorization")
        if header == None:
            raise HTTPException(status_code=400, detail="Token header invalid")
        header = header.split()
        token = header[1]
        decode = await self.jwt_handler.decode(token=token)

        if decode.is_error() is True:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=decode.get_error_message(),
            )

        payload = decode.value
#        print("Payload: ",payload)
        token_scopes = payload.get("scopes", [])
        if not (set(token_scopes) & set(self.scopes)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Doesn't have the scopes required",
            )