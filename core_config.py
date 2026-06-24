from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "key" / "jwt_private.pem"
    public_key_path: Path = BASE_DIR / "key" / "jwt_public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


settings = AuthJWT()