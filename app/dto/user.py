from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    name: str
    email: str
    password: str


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    id: int
    name: str
    email: str

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

