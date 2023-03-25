from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, select, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

from app.entity.mixin import TimestampMixin

Base: DeclarativeBase = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    user = relationship("User", back_populates="role")


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    photo = Column(LargeBinary)
    position = Column(String)
    bio = Column(Text)
    views = Column(Integer)
    count_student = Column(Integer)
    count_course = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    rating = relationship('Rating', back_populates="profile")


class RatingStar(Base):
    __tablename__ = "ratings_stars"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, default=0)


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    star = Column(Integer, ForeignKey('ratings_stars.id'))
    profile_id = Column(Integer, ForeignKey("profiles.id"))

    profile = relationship('Profile', back_populates="rating")
