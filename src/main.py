import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from src.auth.router import router as auth_router
from src.config import settings
from src.database.database import async_session_maker


@asynccontextmanager
async def lifespan(_: FastAPI):
    print(f"{_=} starting")
    await startup()
    yield
    print("Shutdown")


app = FastAPI(
    title=f"Auth API {settings.SERVER_NAME}",
    description=f"API for Auth service {settings.SERVER_NAME}",
    lifespan=lifespan,
)

app.include_router(auth_router)


async def startup():
    print("Startup")
    async with async_session_maker() as session:
        sql = text("""CREATE EXTENSION IF NOT EXISTS "pgcrypto";""")
        await session.execute(sql)
        await session.commit()


@app.get("/ping")
async def perfect_ping():
    await asyncio.sleep(1)  # non-blocking I/O operation

    return {"pong": "pong"}
