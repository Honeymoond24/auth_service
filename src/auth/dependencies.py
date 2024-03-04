import datetime
from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.config import settings

with open("keys/private_key.pem", "r") as file:
    PRIVATE_KEY = file.read()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Load your public key from a file or environment variable
with open("keys/public_key.pem", "r") as file:
    PUBLIC_KEY = file.read()


async def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["ES256"])
        print(f"{payload=}")
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return username
