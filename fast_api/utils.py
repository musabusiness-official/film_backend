from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated= "auto")

def hash(password : str):
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain_password : str, password : str):
    bool = pwd_context.verify(plain_password, password)
    return bool