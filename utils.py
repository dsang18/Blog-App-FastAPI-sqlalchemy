from passlib.context import CryptContext

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

def has_password(text_pwd):
    return pwd_content.hash(text_pwd)

def verify_password(text_pwd, hashed_pwd):
    return pwd_content.verify(text_pwd, hashed_pwd)