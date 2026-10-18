from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from backend.config import settings

ALGO = "HS256"


def hash_password(p: str) -> str:
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()


def verify_password(p: str, hashed: str) -> bool:
    return bcrypt.checkpw(p.encode(), hashed.encode())


def create_token(sub: str, role: str, minutes: int | None = None, **extra) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=minutes or settings.jwt_expire_min)
    return jwt.encode({"sub": sub, "role": role, "exp": exp, **extra}, settings.jwt_secret, algorithm=ALGO)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[ALGO])
