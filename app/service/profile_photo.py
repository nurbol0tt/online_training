from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.database import get_session
from app.repository.profile import UserGetRepository
from app.repository.profile_photo import (
    ProfilePhotoRepository,
    ProfilePhotoReadRepository,
    ProfilePhotoUpdateRepository, ProfilePhotoDeleteRepository,
)


class CreateProfilePhoto:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self, photo, current_user2):
        async with self.async_session.begin() as session:
            user_id = await UserGetRepository.get_user_by_email(
                session, current_user2
            )

            photo = await ProfilePhotoRepository.create_photo(
                session, photo, user_id=user_id
            )
            return photo


class ReadProfilePhoto:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self, photo_id):
        async with self.async_session.begin() as session:

            photo = await ProfilePhotoReadRepository.read_photo(
                session, photo_id
            )
            return photo


class UpdateProfilePhotoUser:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self, photo, current_user2):
        async with self.async_session.begin() as session:
            user_id = await UserGetRepository.get_user_by_email(
                session, current_user2
            )

            photo = await ProfilePhotoUpdateRepository.update_photo(
                session, photo, user_id=user_id
            )
            return photo


class DeleteProfilePhoto:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self, current_user2) -> None:
        async with self.async_session.begin() as session:
            user_id = await UserGetRepository.get_user_by_email(
                session, current_user2
            )

            photo = await ProfilePhotoDeleteRepository.delete_photo(
                session, user_id=user_id
            )
            return photo
