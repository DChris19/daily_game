import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from core_config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.private_key_path.read_text(),
    algorithm: str = settings.algorithm,
    expire_time_delta: timedelta | None = None,
    expire_minutes: int = settings.access_token_expire_minutes,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expire_time_delta or timedelta(minutes=expire_minutes))
    to_encode.update(exp=expire, iat=now)
    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.public_key_path.read_text(),
    algorithm: str = settings.algorithm,
) -> dict:
    return jwt.decode(token, public_key, algorithms=[algorithm])


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)