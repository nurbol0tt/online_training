from io import BytesIO

from fastapi import HTTPException
from sqlalchemy import select
from starlette.responses import StreamingResponse

from app.entity.user import Profile


class ProfilePhotoRepository:

    @classmethod
    async def create_photo(cls, session, photo, user_id):
        result = await session.execute(select(Profile).where(Profile.user_id == user_id))
        profile = result.scalar()

        profile.photo = photo
        await session.flush()


class ProfilePhotoReadRepository:

    @classmethod
    async def read_photo(cls, session, photo_id):
        query = select(Profile).where(Profile.id == photo_id)
        result = await session.execute(query)
        photo = result.scalar()

        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")

        return StreamingResponse(BytesIO(photo.photo), media_type="image/jpeg")


class ProfilePhotoUpdateRepository:

    @classmethod
    async def update_photo(cls, session, photo, user_id):
        result = await session.execute(select(Profile).where(Profile.user_id == user_id))
        profile = result.scalar()

        profile.photo = photo
        await session.flush()
        return StreamingResponse(BytesIO(profile.photo), media_type="image/jpeg")


class ProfilePhotoDeleteRepository:

    @classmethod
    async def delete_photo(cls, session, user_id):
        result = await session.execute(select(Profile).where(Profile.user_id == user_id))
        profile = result.scalar()

        profile.photo = None
        await session.flush()