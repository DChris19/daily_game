from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from auth.auth_router import router as auth_router
from auth.register_router import router as register_router
from auth.admin_router import router as admin_router
from goals.goal_router import router as goals_router

import auth.models
import goals.goal_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # під час розробки — дозволяємо всім
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(register_router)
app.include_router(admin_router)
app.include_router(goals_router)