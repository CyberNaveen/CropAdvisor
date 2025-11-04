import os, jwt
from passlib.hash import bcrypt

SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

def hash_password(plain: str) -> str:
    return bcrypt.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)

def create_jwt(user_id: int, username: str) -> str:
    payload = {"sub": str(user_id), "username": username}
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALG)
