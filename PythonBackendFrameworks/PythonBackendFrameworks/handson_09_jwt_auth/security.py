from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError

# bcrypt uses an intentionally slow, tunable "work factor" hashing algorithm,
# so brute-forcing a stolen password hash is computationally expensive.
# MD5/SHA-256 are designed to be FAST, which is exactly wrong for passwords -
# fast hashes let an attacker try billions of guesses per second.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "dev-only-secret-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    """Returns the subject (email) or raises JWTError if invalid/expired."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["sub"]
