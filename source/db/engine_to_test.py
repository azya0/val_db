import asyncio
from asyncio import WindowsSelectorEventLoopPolicy

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing_extensions import AsyncGenerator

from config import get_settings

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

async_engine = create_async_engine(
    url=get_settings().SQLALCHEMY_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)


async_session_factory = async_sessionmaker(async_engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_session_factory()

    async with async_session:
        try:
            yield async_session
            await async_session.commit()
        except SQLAlchemyError as exc:
            await async_session.rollback()
            raise exc
        finally:
            await async_session.close()
