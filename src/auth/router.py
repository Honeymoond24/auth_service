import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import get_current_user
from src.auth.exceptions import InvalidCredentials
from src.auth.jwt import create_access_token, parse_jwt_user_data
from src.auth.models import UserDAO, User
from src.auth.schemas import Token, AccessTokenResponse, JWTData
from src.core.security import hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, str]:
    await UserDAO.create(
        username=form_data.username,
        hashed_password=hash_password(form_data.password),
    )
    return {
        "username": form_data.username,
    }


@router.get("/users/me")
async def read_users_me(
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        current_user: dict = Depends(get_current_user),
):
    user = await UserDAO.find_one_or_none(current_user)
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = await UserDAO.find_one_or_none_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise InvalidCredentials()

    access_token = create_access_token(
        data={"sub": user.id},
    )
    refresh_token = create_access_token(
        data={"sub": user.id},
        expires_delta=datetime.timedelta(days=7),
    )

    return AccessTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
