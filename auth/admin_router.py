from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from auth.models import User
from auth.auth_router import get_current_active_user

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="admin access required",
        )
    return current_user


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "active": u.active,
            "is_admin": u.is_admin,
        }
        for u in users
    ]


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="cannot delete yourself",
        )
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    await db.delete(user)
    await db.commit()
    return {"detail": f"user {user.username} deleted"}


@router.delete("/reset-db", status_code=status.HTTP_200_OK)
async def reset_database(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    await db.execute(delete(User))
    await db.commit()
    return {"detail": "all tables cleared"}