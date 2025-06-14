from src.auth.domain.user import User
from src.auth.domain.value_object.user_email import UserEmail
from src.auth.domain.value_object.user_name import UserName
from src.auth.domain.value_object.user_password import UserPassword
from src.auth.infraestructure.model.user_model import UserModel

class UserMapper:

    @staticmethod
    def to_domain(user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            name=UserName.create(user_model.name),
            email=UserEmail.create(user_model.email),
            password=UserPassword.create(user_model.password),
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