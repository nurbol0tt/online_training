from typing import Optional, List

from pydantic import BaseModel, Field

from app.dto.application import UserSchema, ProfileSchema, RoleSchema


class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    email: str = Field(..., min_length=8, max_length=64)
    password: str = Field(..., min_length=3, max_length=64)
    role: int


class CreateUserResponse(UserSchema):
    pass


class CurrentUser(BaseModel):
    id: int
    name: str
    email: str
    password: str


class ReadAllUserResponse(BaseModel):
    users: list[UserSchema]


class ReadUserResponse(UserSchema):
    # profile: List[ProfileSchema]
    pass


class UpdateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    email: str = Field(..., min_length=8, max_length=64)

    class Config:
        orm_mode = True


class UpdateUserResponse(UserSchema):
    pass


class TokenData(BaseModel):
    email: Optional[str] = None



