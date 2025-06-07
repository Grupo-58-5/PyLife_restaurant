from abc import ABC, abstractmethod
from typing import List

from src.auth.domain.user import User
from src.shared.utils.result import Result

class IUserRepository(ABC):

    @abstractmethod
    async def create_user(self, user: User) -> Result[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, id: str) -> Result[User]:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Result[User]:
        pass

    @abstractmethod
    async def get_all(self, page: int, page_size: int) -> Result[List[User]]:
        pass

    @abstractmethod
    async def verify_email(self, email: str) -> Result[bool]:
        pass

    @abstractmethod
    async def update_profile(self, user: User) -> Result[User]:
        pass

    @abstractmethod
    async def delete_user(self, user: User) -> Result[bool]:
        pass