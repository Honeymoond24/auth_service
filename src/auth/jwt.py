import datetime
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.auth.config import auth_config
from src.auth.exceptions import AuthRequired, InvalidToken
from src.auth.schemas import JWTData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
with open("keys/private_key.pem", "r") as file:
    PRIVATE_KEY = file.read()
with open("keys/public_key.pem", "r") as file:
    PUBLIC_KEY = file.read()


def create_access_token(
        data: dict,
        expires_delta: Optional[datetime.timedelta] = datetime.timedelta(minutes=auth_config.JWT_EXPIRE_MINUTES),
):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=auth_config.JWT_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=auth_config.JWT_ALGORITHM)
    return encoded_jwt


async def parse_jwt_user_data_optional(
    token: str = Depends(oauth2_scheme),
) -> JWTData | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, PUBLIC_KEY, algorithms=[auth_config.JWT_ALGORITHM]
        )
    except JWTError:
        raise InvalidToken()

    return JWTData(**payload)


async def parse_jwt_user_data(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    if not token:
        raise AuthRequired()

    return token
