from abc import ABC,abstractmethod

class HashHelper(ABC):

    @abstractmethod
    async def verify_password(self,regular_password:str, hashed_password:str)->bool:
        pass
    
    @abstractmethod
    async def get_password_hashed(self,password:str):
        pass