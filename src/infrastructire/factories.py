import typing

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import session as sql_session

from infrastructire import settings, repository

S = typing.TypeVar("S")


class SessionFactory(typing.Protocol[S]):

    def __call__(self) -> S: ...


class RepositoryFactory(typing.Protocol[S]):
    def __call__(self, session: S) -> repository.Repository: ...


class SQLAlchemySessionFactory(SessionFactory):
    def __call__(self) -> sql_session.AsyncSession:
        return async_sessionmaker(
            create_async_engine(
                settings.get_mysql_url(),
                isolation_level="REPEATABLE READ",
            )
        )()


class SQLAlchemyRepositoryFactory(RepositoryFactory):
    def __call__(self, session: sql_session.AsyncSession):
        return repository.SQLAlchemyRepository(session=session)
