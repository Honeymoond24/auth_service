import datetime
from typing import AsyncGenerator, Annotated

from sqlalchemy import MetaData, NullPool, String, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column

from src.config import settings

# from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, REDIS_HOST, REDIS_PORT

DATABASE_URL = (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
                f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
str_256 = Annotated[str, 256]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=text("TIMEZONE('utc', now())"),
)]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships aren't used in __repr__. because it could cause unexpected queries."""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=True,  # logging
)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
