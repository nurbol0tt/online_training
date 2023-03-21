from typing import AsyncIterator

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette import status

from app.db.database import get_session
from app.dto.application import UserSchema
from app.repository.user import (
    UserCreateRepository,
    UserReadRepository,
    UserUpdateRepository,
    UserAllReadRepository,
    UserDeleteRepository, UserLoginRepository,
)
from app.utils.auth.hashing import Hasher
from app.utils.auth.my_token import create_access_token


class CreateNotebook:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self, data) -> UserSchema:
        async with self.async_session.begin() as session:
            user = await UserCreateRepository.create_user(
                session, name=data.name, email=data.email,
                password=Hasher.get_password_hash(data.password)
            )
            return UserSchema.from_orm(user)


class ReadUser:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self, user_id: int) -> UserSchema:
        async with self.async_session() as session:
            notebook = await UserReadRepository.read_by_id(
                session, user_id, include_profile=True
            )
            if not notebook:
                raise HTTPException(status_code=404)
            return UserSchema.from_orm(notebook)


class ReadAllUser:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self) -> AsyncIterator[UserSchema]:
        async with self.async_session() as session:
            async for notebook in UserAllReadRepository.read_all(
                    session, include_profile=True
            ):
                yield UserSchema.from_orm(notebook)


class UpdateUser:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self, user_id: int, name: str, email: str) -> UserSchema:
        async with self.async_session.begin() as session:
            user = await UserUpdateRepository.read_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=404)
            await UserUpdateRepository.update(session, user, name, email)
            return UserSchema.from_orm(user)


class DeleteUser:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self, user_id: int) -> None:
        async with self.async_session.begin() as session:
            user = await UserDeleteRepository.read_by_id(session, user_id)
            if not user:
                return
            await UserDeleteRepository.delete(session, user)


class LoginUser:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self, request):
        async with self.async_session.begin() as session:
            user = await UserLoginRepository.login(session, request)

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Invalid Credentials")
            if not Hasher.verify_password(user.password, request.password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Incorrect password")
            access_token = await create_access_token(data={"sub": request.username})
            return {"access_token": access_token, "token_type": "bearer"}
