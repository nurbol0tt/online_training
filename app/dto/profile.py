from fastapi import UploadFile
from pydantic import Field, BaseModel

from app.dto.application import ProfileSchema, UserSchema


class CreateProfileResponse(ProfileSchema):
    pass


class CreateProfileRequest(BaseModel):
    position: str
    bio: str


class UpdateProfileRequest(ProfileSchema):

    class Config:
        orm_mode = True


class UpdateProfileResponse(ProfileSchema):
    pass


class ReadProfileResponse(ProfileSchema):
    user_name: UserSchema

    class Config:
        orm_mode = True


class PhotoRequest(BaseModel):
    photo: UploadFile

