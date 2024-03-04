from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    JWT_ALGORITHM: str = Field(validation_alias='JWT_ALGORITHM')
    JWT_EXPIRE_MINUTES: int = Field(validation_alias='JWT_EXPIRE_MINUTES')

    # REFRESH_TOKEN_KEY: str = "refreshToken"
    JWT_EXPIRE_REFRESH_DAYS: int = Field(validation_alias='JWT_EXPIRE_REFRESH_DAYS')

    # SECURE_COOKIES: bool = True


auth_config = AuthConfig()
