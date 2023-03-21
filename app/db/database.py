import logging
from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.utils.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

logger = logging.getLogger(__name__)


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# async_engine = create_async_engine(DATABASE_URL, connect_args={}, future={})
#
# AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
#
#
# async def async_get_db():
#     async with AsyncSessionLocal() as db:
#         yield db
#         await db.commit()


# DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#
# async_engine = create_async_engine(DATABASE_URL, echo=True)
#
# AsyncLocalSession = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
#
#
# @asynccontextmanager
# async def get_async_session():
#     session = AsyncLocalSession()
#     try:
#         yield session
#     except Exception as e:
#         print(e)
#         await session.rollback()
#     finally:
#         await session.close()
#
#
# def async_session(func):
#     async def wrapper(*args, **kwargs):
#         async with get_async_session() as session:
#             return await func(session, *args, **kwargs)
#     return wrapper


# engine = create_async_engine(
#     DATABASE_URL,
#     future=True,
#     echo=True,
#     execution_options={"isolation_level": "AUTOCOMMIT"},
# )
#
# # create session for the interaction with database
# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
#
#
# async def get_db() -> Generator:
#     """Dependency for getting async session"""
#     try:
#         session: AsyncSession = async_session()
#         yield session
#     finally:
#         await session.close()


async_engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)
