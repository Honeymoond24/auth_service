import datetime
import uuid

from sqlalchemy import Boolean, String, UUID, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.database.dao import BaseDAO
from src.database.database import Base, created_at, updated_at


class User(Base):
    __tablename__ = "user"

    """
    Run this command in psql to enable uuid_generate_v4():
        `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`
    """
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, server_default=func.uuid_generate_v4()
    )

    username: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class UserDAO(BaseDAO):
    model = User


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, server_default=func.uuid_generate_v4()
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), index=True, nullable=False
    )
    token: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )

    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False
    )

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class RefreshTokenDAO(BaseDAO):
    model = RefreshToken
