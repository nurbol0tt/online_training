from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

from app.entity.mixin import TimestampMixin

Base: DeclarativeBase = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    role = Column(Integer, ForeignKey('roles.id'))

    profile = relationship('Profile', back_populates="owner")

    @classmethod
    async def read_by_id(
            cls, session: AsyncSession, user_id: int,
    ):
        query = select(User).where(User.id == user_id)
        res = await session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    bio = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="profile")
