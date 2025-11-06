import os, jwt, datetime
from passlib.hash import bcrypt

SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

def hash_password(plain: str) -> str:
    return bcrypt.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)

def create_jwt(user_id: int, username: str) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1) 
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALG)

def decode_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALG])
    except jwt.ExpiredSignatureError:
        return None 
    except jwt.InvalidTokenError:
        return None
