import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from infrastructire import orm, settings


@pytest.fixture(scope="session")
async def init_orm():
    engine = create_async_engine(settings.get_mysql_url(), pool_pre_ping=True, pool_size=10, max_overflow=30)
    async with engine.begin() as connect:
        await connect.run_sync(orm.Base.metadata.drop_all)
        await connect.run_sync(orm.Base.metadata.create_all)
