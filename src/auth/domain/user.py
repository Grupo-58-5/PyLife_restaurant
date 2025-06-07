from uuid import UUID
from src.auth.domain.enum.role import  Roles

class User:

    def __init__(self,
        id: UUID,
        name: str,
        email: str,
        password: str,
        role: Roles | None = Roles.CLIENT
    ):
        self.id: str = id
        self.name: str = name
        self.email: str = email
        self.password: str = password
        self.role: Roles = role

    def get_id(self) -> UUID:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_password(self) -> str:
        return self.password

    def get_role(self) -> Roles:
        return self.role

    def change_name(self, name: str) -> None:
        self.name = name

    def change_email(self, email: str) -> None:
        self.email = email

    def change_password(self, password: str) -> None:
        self.password = password

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, role={self.role})"