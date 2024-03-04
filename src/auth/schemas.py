from typing import Optional, Annotated

from pydantic import BaseModel, Field, UUID4, Strict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class JWTData(BaseModel):
    user_id: Annotated[UUID4, Strict(False)] = Field(alias="sub")
    is_superuser: bool = False
