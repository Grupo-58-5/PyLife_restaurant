import jwt
from uuid import UUID
from datetime import datetime, timedelta, timezone
import time
from typing import Final, List
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from src.shared.application.ports.auth_handler import AuthHandler
from src.shared.config.settings import settings
from src.shared.utils.result import Result
from src.auth.domain.enum.role import Roles

JWT_ALGORITHM: Final = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES: Final = settings.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET: Final = settings.SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer("/auth/log_in")

class JWTAuthAdapter(AuthHandler):

    async def sign(self, id:UUID ,role:str, scopes: List[str] | None = None, expire_time: timedelta | None = None)-> str :
        'Create the token for the user'

        if expire_time:
            expire = datetime.now(timezone.utc) + expire_time
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        print("Rol del usuario: ",role)

        if scopes is None:
            if role == Roles.CLIENT:
                scopes = ['client:read','client:write']
            elif role == Roles.ADMIN:
                scopes = ['admin:read','admin:write']

        payload: dict = {
            "id": str(id),
            "role": str(role),
            "expires": str(expire),
            "scopes": scopes
        }

        encoded_jwt = jwt.encode(payload, SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    async def decode(self, token: str =  Depends(oauth2_scheme)) -> Result[dict]:
        'Decode the user information from the token'

        try:
            payload: dict = jwt.decode(token, SECRET, algorithms=[JWT_ALGORITHM])
            if datetime.fromisoformat(payload['expires']) >= datetime.now(timezone.utc):
                return Result[dict].success(payload)
            else:
                return Result.failure(Exception,'The time of your JWT has expired')
        except BaseException as e:
            if 'Signature verification failed' in str(e):
                return Result.failure(e,'Signature verification failed because of an invalid token')
            if 'Invalid crypto padding' in str(e):
                return Result.failure(e,'Your JWT token is not complete, check it please')
            if 'Not enough segments' in str(e):
                return Result.failure(e,'Your JWT token is not complete, check it please')

            print('decodeJWT e:',e)
            return Result.failure(e,'There is no clue about this error')