import uuid

from fastapi import HTTPException
from sqlalchemy import select, delete, update, Result
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.database.database import async_session_maker


class BaseDAO:
    model = None  # This should be overridden by subclasses

    @classmethod
    async def create(cls, **kwargs):
        async with async_session_maker() as session:
            obj = cls.model(**kwargs)
            session.add(obj)
            try:
                await session.commit()
                await session.refresh(obj)
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")
            return obj

    @classmethod
    async def find_all(cls) -> list:
        async with async_session_maker() as session:
            stmt = select(cls.model)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, model_id: uuid.UUID | int):
        async with async_session_maker() as session:
            stmt = select(cls.model).where(cls.model.id == model_id).limit(1)
            result: Result[tuple[cls]] = await session.execute(stmt)
            return result.scalars().one_or_none()

    @classmethod
    async def find_one_or_none_by_username(cls, username: str):
        async with async_session_maker() as session:
            stmt = select(cls.model).where(cls.model.username == username).limit(1)
            result: Result[tuple[cls]] = await session.execute(stmt)
            return result.scalars().one_or_none()

    @classmethod
    async def update(cls, model_id: int, **kwargs):
        async with async_session_maker() as session:
            stmt = (
                update(cls.model).
                where(cls.model.id == model_id).
                values(**kwargs).
                execution_options(synchronize_session="fetch")
            )
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete(cls, model_id: int):
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(cls.model.id == model_id)
            await session.execute(stmt)
            await session.commit()
