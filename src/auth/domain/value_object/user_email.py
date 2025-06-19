import re

class UserEmail:

    email: str

    def __init__(self, email: str):

        if email is None:
            raise ValueError("Invalid email value can't be None")

        email_regex = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )

        valid = bool(email_regex.match(email))

        if (valid != True):
            raise ValueError("Invalid email value")

        self.email = email

    def get_value(self):
        return self.email

    @staticmethod
    def create(email: str):
        return UserEmail(email=email)