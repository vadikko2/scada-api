import typing

import aio_pika
import redis.asyncio as redis
from aio_pika import abc, pool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import session as sql_session

from infrastructire import repository, settings

S = typing.TypeVar("S")


class SessionFactory(typing.Protocol[S]):
    def __call__(self) -> S:
        ...


class RepositoryFactory(typing.Protocol[S]):
    def __call__(self, session: S) -> repository.Repository:
        ...


class SQLAlchemySessionFactory(SessionFactory):
    def __call__(self) -> sql_session.AsyncSession:
        return async_sessionmaker(
            create_async_engine(
                settings.get_mysql_url(),
                isolation_level="REPEATABLE READ",
            )
        )()


class RedisClientFactory:
    def __call__(self) -> redis.Redis:
        return redis.Redis.from_url(settings.get_redis_url())


class SQLAlchemyRepositoryFactory(RepositoryFactory):
    def __call__(self, session: sql_session.AsyncSession):
        return repository.SQLAlchemyRepository(session=session)


async def amqp_connection_pool_factory(url: str) -> abc.AbstractRobustConnection:
    return await aio_pika.connect_robust(url=url, virtualhost="scada")


async def amqp_channel_pool_factory(connection_pool: pool.Pool) -> aio_pika.Channel:
    async with connection_pool.acquire() as connection:
        return await connection.channel()
