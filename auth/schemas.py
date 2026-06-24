from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    username: Annotated[str, MaxLen(20), MinLen(3)]
    password: str
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    username: str
    password: bytes
    email: EmailStr
    active: bool = True
    is_admin: bool = False


class TokenInfo(BaseModel):
    access_token: str
    token_type: str