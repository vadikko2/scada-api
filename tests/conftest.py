import asyncio

import pytest

pytest_plugins = [
    "tests.integration.fixtures",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    try:
        yield loop
    finally:
        if loop.is_running():
            loop.close()
