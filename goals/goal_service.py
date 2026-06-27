from datetime import datetime, timezone, timedelta
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from goals.goal_models import Goal


async def create_goal(db: AsyncSession, user_id: int, title: str,
                      description: str | None, scheduled_at: datetime | None) -> Goal:
    new_goal = Goal(
        user_id=user_id,
        title=title,
        description=description,
        scheduled_at=scheduled_at,
    )
    db.add(new_goal)
    await db.commit()
    await db.refresh(new_goal)
    return new_goal


async def get_user_goals(db: AsyncSession, user_id: int) -> list[Goal]:
    result = await db.execute(
        select(Goal).where(Goal.user_id == user_id)
    )
    return result.scalars().all()


async def complete_goal(db: AsyncSession, goal_id: int, user_id: int) -> Goal | None:
    result = await db.execute(
        select(Goal).where(Goal.id == goal_id, Goal.user_id == user_id)
    )
    goal = result.scalar_one_or_none()
    if not goal:
        return None

    today = datetime.now(timezone.utc).date()

    if goal.last_completed_at:
        last_date = goal.last_completed_at.date()
        if last_date == today:
            return goal
        elif last_date == today - timedelta(days=1):
            goal.streak_count += 1
        else:
            goal.streak_count = 1
    else:
        goal.streak_count = 1

    goal.is_completed = True
    goal.last_completed_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(goal)
    return goal


async def delete_goal(db: AsyncSession, goal_id: int, user_id: int) -> bool:
    result = await db.execute(
        select(Goal).where(Goal.id == goal_id, Goal.user_id == user_id)
    )
    goal = result.scalar_one_or_none()
    if not goal:
        return False
    await db.delete(goal)
    await db.commit()
    return True


def get_streak_message(streak_count: int, title: str) -> str:
    if streak_count == 1:
        return f"Відмінний початок! Перше виконання цілі '{title}'!"
    elif streak_count < 7:
        return f"Молодець! Ти виконуєш '{title}' вже {streak_count} дні підряд!"
    elif streak_count < 30:
        weeks = streak_count // 7
        return f"Неймовірно! Вже {weeks} тиждень(і) дотримуєшся плану з '{title}'!"
    else:
        return f"Легенда! {streak_count} днів підряд виконуєш '{title}'!"