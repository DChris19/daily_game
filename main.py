from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base
from auth.auth_router import router as auth_router
from auth.register_router import router as register_router
from auth.admin_router import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(register_router)
app.include_router(admin_router)