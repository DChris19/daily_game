from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from auth.auth_router import get_current_active_user
from auth.models import User
from goals.goal_schemas import GoalCreate, GoalResponse, GoalCompleteResponse
from goals import goal_service

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal_data: GoalCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await goal_service.create_goal(
        db=db,
        user_id=current_user.id,
        title=goal_data.title,
        description=goal_data.description,
        scheduled_at=goal_data.scheduled_at,
    )


@router.get("", response_model=list[GoalResponse])
async def get_my_goals(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await goal_service.get_user_goals(db=db, user_id=current_user.id)


@router.patch("/{goal_id}/complete", response_model=GoalCompleteResponse)
async def complete_goal(
    goal_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    goal = await goal_service.complete_goal(
        db=db, goal_id=goal_id, user_id=current_user.id
    )
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="goal not found",
        )
    message = goal_service.get_streak_message(goal.streak_count, goal.title)
    return GoalCompleteResponse(goal=goal, message=message)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    deleted = await goal_service.delete_goal(
        db=db, goal_id=goal_id, user_id=current_user.id
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="goal not found",
        )