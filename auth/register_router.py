from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from auth.models import User
from auth.schemas import UserCreate
from jwt_utils import hash_password
from core_config import settings

router = APIRouter(prefix="/auth", tags=["register"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username already taken",
        )

    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email already registered",
        )

    is_admin = (
        user_data.username == settings.admin_username
        and user_data.password == settings.admin_password
    )

    new_user = User(
        username=user_data.username,
        password=hash_password(user_data.password),
        email=user_data.email,
        is_admin=is_admin,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "is_admin": new_user.is_admin,
    }