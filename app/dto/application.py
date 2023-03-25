from pydantic import BaseModel


class ProfileSchema(BaseModel):
    position: str
    bio: str

    class Config:
        orm_mode = True


class RoleSchema(BaseModel):
    title: str

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
