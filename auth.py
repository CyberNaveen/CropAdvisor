import os
import jwt
import datetime
import bcrypt 

SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

# -------------------
# Password Hashing
# -------------------
def hash_password(plain: str) -> str:
    """Hash a plain text password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain text password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

# -------------------
# JWT Helpers
# -------------------
def create_jwt(user_id: int, username: str) -> str:
    """Create a JWT token with user_id and username."""
    payload = {
        "sub": str(user_id) if user_id is not None else None,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALG)

def decode_jwt(token: str):
    """Decode a JWT token and return the payload, or None if invalid/expired."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALG])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
