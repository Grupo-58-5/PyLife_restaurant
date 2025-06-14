import re
from uuid import UUID
from typing import Optional
from src.auth.domain.enum.role import  Roles
from src.auth.domain.value_object.user_email import UserEmail
from src.auth.domain.value_object.user_name import UserName
from src.auth.domain.value_object.user_password import UserPassword

class User:

    def __init__(self,
        id: UUID,
        name: UserName,
        email: UserEmail,
        password: UserPassword,
        role: Roles | None = Roles.CLIENT,
        reservations: list[str] = None
    ):
        self.id: str = id
        self.name: UserName = name
        self.email: UserEmail = email
        self.password: UserPassword = password
        self.role: Roles = role
        self.reservations: list[str] = reservations

    def get_id(self) -> UUID:
        return self.id

    def get_name(self) -> str:
        return self.name.full_name

    def get_email(self) -> str:
        return self.email.email

    def get_password(self) -> str:
        return self.password.password

    def get_role(self) -> Roles:
        return self.role

    def get_reservations(self) -> Optional[list[str]]:
        return self.reservations

    def change_name(self, name: UserName) -> None:
        self.name = name

    def change_email(self, email: UserEmail) -> None:
        self.email = email

    def change_password(self, password: UserPassword) -> None:
        self.password = password

    def add_reservation(self,reservation: str) -> None:

        uuid_regex = re.compile(
            r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
        )

        valid = bool(uuid_regex.match(id))

        if (valid is False):
            raise ValueError('Wrong reservation ID, must be a UUID')

        self.reservations.append(reservation)

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name.get_value(),
            "email": self.email.get_value(),
            "password": self.password.get_value(),
            "role": self.role,
        }

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, role={self.role}, reservations={self.reservations})"

