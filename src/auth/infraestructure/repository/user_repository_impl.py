from uuid import UUID
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from typing import Optional, List

from src.shared.utils.result import Result
from src.auth.domain.user import User
from src.auth.infraestructure.model.user_model import UserModel
from src.auth.domain.repository.user_repository_interface import IUserRepository
from src.auth.infraestructure.mappers.user_mapper import UserMapper


class UserRepositoryImpl(IUserRepository):

    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db

    async def create_user(self, user: User) -> Result[User]:

        try:
            user_model = UserMapper.to_model(user)
            self.db.add(user_model)
            await self.db.commit()
            await self.db.refresh(user_model)
            return Result[User].success(user)
        except BaseException as e:
            print("Error: ",e)
            return Result.failure(e,'Failed insert into User')

    async def get_user_by_id(self, id: str) -> Result[User]:
        query = select(UserModel).where(UserModel.id == UUID(id))
        result: Optional[UserModel] = (await self.db.exec(query)).first()

        if result is None:
            return Result.failure(HTTPException(status_code=404, detail="User not found"),"User not found")

        user = UserMapper.to_domain(result)

        return Result[User].success(user)

    async def get_user_by_email(self, email: str) -> Result[User]:
        query = select(UserModel).where(UserModel.email == email)
        result: Optional[UserModel] = (await self.db.exec(query)).first()

        if result is None:
            return Result.failure(HTTPException(status_code=404, detail="User not found"),"User not found")

        user = UserMapper.to_domain(result)

        return Result[User].success(user)

    async def get_all(self, page: int, page_size: int) -> Result[List[User]]:
        offset = (page - 1) * page_size
        query = select(UserModel).offset(offset).limit(page_size)
        result: Optional[List[UserModel]] = (await self.db.exec(query)).all()
        print("Lista de usuarios: ",result)
        users: List[User] = [UserMapper.to_domain(x) for x in result]

        return Result[List[User]].success(users)

    async def verify_email(self, email: str) -> Result[bool]:
        query = select(UserModel).where(UserModel.email == email)
        result: Optional[UserModel] = (await self.db.exec(query)).first()

        if result is None:
            return Result[bool].success(False)

        return Result[bool].success(True)

    async def update_profile(self, user: User) -> Result[User]:
        try:
            user_model: Optional[UserModel] = await self.db.get(UserModel, user.id)
            for field, value in user.__dict__().items():
                setattr(user_model, field, value)
            await self.db.commit()
            await self.db.refresh(user_model)
            print("User actualizado: ",user_model)
            return Result[User].success(UserMapper.to_domain(user_model=user_model))
        except BaseException as e:
            print(e)
            return Result.failure(e,f'Failed to update user')

    async def delete_user(self, user: User) -> Result[bool]:
        try:
            user_model: Optional[UserModel] = await self.db.get(UserModel, user.get_id())
            await self.db.delete(user_model)
            await self.db.commit()
            return Result[bool].success(True)
        except BaseException as e:
            print("Error: ",e)
            return Result[bool].failure(error=e,messg='DELETE failed')