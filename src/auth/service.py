from datetime import datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.models import UserDAO
from src.core.security import hash_password
from src.database.database import async_session_maker


async def register(
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    await UserDAO.create(
        username=form_data.username,
        hashed_password=hash_password(form_data.password),
    )


async def test():
    async with async_session_maker() as session:
        # stmt = (
        #     select(User)
        #     .where(User.username == 'test234')
        #     # .limit(1)
        # )
        # result = await session.execute(stmt)
        # db_user = result.scalars().first()
        # # db_user = result.one()
        # print(f"\n\n{db_user=}\n\n")
        # db_user = result.fetchone()
        # print(f"\n\n{db_user=}\n\n")
        # if db_user:
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")

        # stmt = insert(User).values(
        #     username=f'test{datetime.now().timestamp()}',
        #     hashed_password=hash_password('test'),
        #     is_verified=True,
        # )
        # await session.execute(stmt)
        # await session.commit()
        await UserDAO.create(
            username=f'test{datetime.now().timestamp()}',
            hashed_password=hash_password('test'),
            is_verified=False,
        )


if __name__ == '__main__':
    import asyncio

    asyncio.run(test())
