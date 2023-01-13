from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verificar(simple_password, hashed_password):
    return pwd_context.verify(simple_password, hashed_password)
    