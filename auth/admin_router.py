from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete
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


@router.delete("/reset-db", status_code=status.HTTP_200_OK)
async def reset_database(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    await db.execute(delete(User))
    await db.commit()
    return {"detail": "all tables cleared"}