from datetime import timedelta
from uuid import UUID
from abc import ABC,abstractmethod

class AuthHandler(ABC):

    @abstractmethod
    async def sign(self,id:UUID ,role:str, expire_time: timedelta | None = None)-> str :
        'Create the token for the user'
        pass


    @abstractmethod
    async def decode(self,token:str):
        'Decode the user information from the token'
        pass