from passlib.context import CryptContext


def hash_password(password: str) -> str:
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(password, hashed_password)


if __name__ == '__main__':
    # print(hash_password("JQI6c6UuZn0sH2uqH"))
    # print(verify_password("JQI6c6UuZn0sH2uqH", "$2b$12$xOoEImf3c7GaIu.yO21tL.2XtmMD6sKH7afHMGkd0JnbzvPe5VQ16"))
    pass
