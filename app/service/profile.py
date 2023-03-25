from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.database import get_session
from app.dto.application import ProfileSchema
from app.repository.profile import ProfileCreateRepository, TeacherReadRepository, ProfileUpdateRepository
from app.repository.user import UserGetRepository


class CreateProfile:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self, data, current_user2) -> ProfileSchema:
        async with self.async_session.begin() as session:
            user_id = await UserGetRepository.get_user_by_email(
                session, current_user2
            )
            profile = await ProfileCreateRepository.create_profile(
                session, bio=data.bio, position=data.position, user_id=user_id,
            )
            return ProfileSchema.from_orm(profile)


class UpdateProfile:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session
        
    async def execute(self, profile_id: int, position: str, bio: str) -> ProfileSchema:
        async with self.async_session.begin() as session:
            profile = await ProfileUpdateRepository.read_profile(session, profile_id)
            if not profile: 
                raise HTTPException(status_code=404)

            await ProfileUpdateRepository.update(session, profile, position, bio)
            return ProfileSchema.from_orm(profile)


class ReadTeacher:
    def __init__(self, session: async_sessionmaker = Depends(get_session)) -> None:
        self.async_session = session

    async def execute(self, id: int):
        async with self.async_session() as session:
            user = await TeacherReadRepository.read_by_id(
                session, id
            )
            if not user:
                raise HTTPException(status_code=404)
            # return ReadUserResponse.from_orm(user
            return user
