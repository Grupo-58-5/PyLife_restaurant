from src.auth.domain.user import User
from src.auth.infraestructure.model.user_model import UserModel

class UserMapper:

    @staticmethod
    def to_domain(user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password=user_model.password,
            role=user_model.role
        )

    @staticmethod
    def to_model(data: User) -> UserModel:
        return UserModel(
            id=data.get_id(),
            name=data.get_name(),
            email=data.get_email(),
            password=data.get_password(),
            role=data.get_role()
        )