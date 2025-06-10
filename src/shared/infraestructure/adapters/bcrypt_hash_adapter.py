from bcrypt import checkpw,hashpw,gensalt

from src.shared.application.ports.hash_handler import HashHelper

class BcryptHashAdapter(HashHelper):

    async def verify_password(self, regular_password:str, hashed_password:str)->bool:
        if checkpw(regular_password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
        else: return False

    async def get_password_hashed(self, password:str):
        encoded = hashpw(
            password.encode('utf-8'),
            gensalt()
        )

        decoded = encoded.decode('utf-8')
        return decoded