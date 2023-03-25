from typing import Optional, AsyncIterator

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.entity.user import User


class UserReadRepository:

    @classmethod
    async def read_by_id(
            cls, session: AsyncSession, user_id: int, include_profile: bool = False
    ) -> Optional[User]:
        # Create a select query to retrieve the user by their ID
        stmt = select(User).where(User.id == user_id)

        # If the `include_profile` flag is set, also retrieve the user's profile
        # if include_profile:
        #     stmt = stmt.options(selectinload(User.profile))

        # Execute the query and return the result
        # Note: The `order_by` clause sorts the result by ID in ascending order
        return await session.scalar(stmt.order_by(User.id))


class UserCreateRepository(UserReadRepository):

    @classmethod
    async def read_by_email(cls, session: AsyncSession, email: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @classmethod
    async def create_user(
            cls, session: AsyncSession, email: str, name: str, password: str, role: int,
    ) -> User:

        if await cls.read_by_email(session, email):
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(name=name, email=email,  password=password, role_id=role)
        session.add(user)
        await session.flush()

        # To fetch profile
        new = await cls.read_by_id(session, user.id)
        if not new:
            raise RuntimeError()
        return new


class UserAllReadRepository:

    @classmethod
    async def read_all(
            cls, session: AsyncSession, include_profile: bool
    ) -> AsyncIterator[User]:

        stmt = select(User)

        if include_profile:
            stmt = stmt.options(selectinload(User.profile))
        stream = await session.stream_scalars(stmt.order_by(User.id))
        async for row in stream:
            yield row


class UserUpdateRepository(UserReadRepository):

    @classmethod
    async def update(cls, session: AsyncSession, user, name: str, email: str) -> None:
        user.name = name
        user.email = email
        await session.flush()
        await session.refresh(user)


class UserDeleteRepository(UserReadRepository):

    @classmethod
    async def delete(cls, session: AsyncSession, user: int) -> None:
        await session.delete(user)
        await session.flush()


class UserLoginRepository(UserReadRepository):

    @classmethod
    async def login(cls, session: AsyncSession, request):
        result = await session.execute(select(User).where(User.email == request.username))
        return result.scalar_one_or_none()


class UserGetEmailRepository:

    @classmethod
    async def read_by_email(cls, session: AsyncSession, username: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.email == username))
        return result.scalar_one_or_none()


class UserGetRepository:

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, current_user2):
        result = await session.execute(select(User).where(User.email == current_user2))
        user = result.scalar_one_or_none()
        return user.id
