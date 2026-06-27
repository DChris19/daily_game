from datetime import datetime
from pydantic import BaseModel


class GoalCreate(BaseModel):
    title: str
    description: str | None = None
    scheduled_at: datetime | None = None


class GoalUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    scheduled_at: datetime | None = None


class GoalResponse(BaseModel):
    id: int
    title: str
    description: str | None
    scheduled_at: datetime | None
    is_completed: bool
    streak_count: int
    last_completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class GoalCompleteResponse(BaseModel):
    goal: GoalResponse
    message: str