from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.entity.mixin import TimestampMixin
from app.entity.user import Base


class TypeCategory(Base):
    __tablename__ = "type_categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class GonnaLearn(Base):
    __tablename__ = "gonna_learn"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class Include(Base):
    __tablename__ = "gonna_learn"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class LanguageCategory(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class ContentCategory(Base):
    __tablename__ = "content_categories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class CourseContent(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    file = Column(String)
    video = Column(String)
    orders = relationship('Order', backref='customer')
    type_category = Column(Integer, ForeignKey('content_categories.id'))


class Course(TimestampMixin, Base):
    __tablename = "courses"
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    description = Column(String)
#     type_category = Column(Integer, ForeignKey('type_categories.id'))
#     video_course =
#     language Category =
    old_price = Column(Integer, default=0)
    new_price= Column(Integer, default=0)
#     includes Category

    user = relationship("User", back_populates="course")
