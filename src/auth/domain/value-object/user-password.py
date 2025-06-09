class UserPassword:

    password: str

    def __init__(self, password: str):

        if password is None:
            raise ValueError("Invalid password value can't be None")


        self.password = password

    @property
    def password(self):
        return self.password

    @staticmethod
    def create(password: str):
        return UserPassword(password=password)