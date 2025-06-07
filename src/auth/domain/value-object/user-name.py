import re

class UserName:

    full_name: str

    def __init__(self, full_name: str):

        if full_name is None:
            raise ValueError("Invalid name value can't be None")


        self.full_name = full_name

    @property
    def email(self):
        return self.email

    @staticmethod
    def create(full_name: str):
        return UserName(full_name=full_name)