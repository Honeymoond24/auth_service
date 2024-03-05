import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# from src.config import settings
from src.database.database import get_async_session, metadata
from src.main import app

# DATABASE
# engine_test = create_async_engine(settings.TEST_DB_DSN, poolclass=NullPool)
engine_test = create_async_engine("postgresql+asyncpg://postgres:postgres@test_db:5432/test", poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    print("running migrations..")
    os.system("alembic upgrade head")
    yield
    os.system("alembic downgrade base")


# SETUP
@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client: TestClient = TestClient(
    app,
    # transport=WSGITransport(app=app),
    # base_url='http://localhost:8000',
)


def test_register():
    response = client.post("/auth/register", data={
        "username": "string",
        "password": "string",
    })
    print(client.base_url)
    print(response.url, response.text)
    assert response.status_code == 201

# @pytest.fixture(scope="session")
# async def ac() -> AsyncGenerator[AsyncClient, None]:
#     async with AsyncClient(transport=WSGITransport(app=app), base_url="http://127.0.0.1:8000") as ac:
#         yield ac
