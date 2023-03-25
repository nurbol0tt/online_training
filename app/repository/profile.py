from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entity.user import Profile, User


class ProfileCreateRepository:

    @classmethod
    async def create_profile(
            cls, session: AsyncSession, bio: str, position: str, user_id: int
    ) -> Profile:
        profile = Profile(bio=bio, position=position, user_id=user_id)
        session.add(profile)
        await session.flush()
        return profile


class ProfileUpdateRepository:

    @classmethod
    async def read_profile(cls, session: AsyncSession, profile_id: int) -> Optional[Profile]:
        result = await session.execute(select(Profile).where(Profile.id == profile_id))
        return result.scalar_one_or_none()

    @classmethod
    async def update(cls, session: AsyncSession, profile, position: str, bio: str) -> None:
        profile.position = position
        profile.bio = bio
        await session.flush()
        await session.refresh(profile)


class UserGetRepository:

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, current_user2):
        result = await session.execute(select(User).where(User.email == current_user2))
        user = result.scalar_one_or_none()
        return user.id


class TeacherReadRepository:
    @classmethod
    async def read_by_id(
            cls, session: AsyncSession, id: int):
        stmt = select(User).where(User.role_id == id)
        result = await session.execute(stmt.order_by(User.id))
        return result.scalars().all()
