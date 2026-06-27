from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "key" / "jwt_private.pem"
    public_key_path: Path = BASE_DIR / "key" / "jwt_public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60 * 24

    admin_username: str
    admin_password: str

    class Config:
        env_file = ".env"


settings = AuthJWT()