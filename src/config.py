from pydantic import (
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    DEV_MODE: bool = Field(validation_alias='DEV_MODE')
    SERVER_NAME: str = Field(validation_alias='SERVER_NAME')

    JWT_ALGORITHM: str = Field(validation_alias='JWT_ALGORITHM')
    JWT_EXPIRE_MINUTES: int = Field(validation_alias='JWT_EXPIRE_MINUTES')

    DB_HOST: str = Field(validation_alias='POSTGRES_HOST')
    DB_PORT: str = Field(validation_alias='POSTGRES_PORT')
    DB_NAME: str = Field(validation_alias='POSTGRES_DB')
    DB_USER: str = Field(validation_alias='POSTGRES_USER')
    DB_PASS: str = Field(validation_alias='POSTGRES_PASSWORD')
    # pg_dsn: PostgresDsn = 'postgres://user:pass@localhost:5432/foobar'

    # domains: Set[str] = set()

    # model_config = SettingsConfigDict(env_prefix='my_prefix_')


settings = Settings()
# print(Settings().model_dump())
# print(f"{settings.DB_HOST=} {settings.DB_PORT=} {settings.DB_NAME=} {settings.DB_USER=} {settings.DB_PASS=}")
