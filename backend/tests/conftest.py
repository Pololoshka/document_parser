import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient

from settings import DBSettings
from src.db.uow import SqlAlchemyUnitOfWork

pytest_plugins = ["pytest_asyncio", "tests.utils_db"]

load_dotenv(".env.tests", override=True)


@pytest.fixture(scope="session")
def event_loop(
    request: type[pytest.FixtureRequest],
) -> Generator[asyncio.AbstractEventLoop, Any, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def app(event_loop: Generator[asyncio.AbstractEventLoop, Any, None]) -> AsyncClient:
    from main import app as _app

    return _app  # type: ignore


@pytest.fixture()
async def client(app: AsyncClient) -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:  # type: ignore
        yield client


@pytest.fixture(autouse=True)
def _override_dependency(
    app: AsyncClient,
    uow: SqlAlchemyUnitOfWork,
    event_loop: Generator[asyncio.AbstractEventLoop, Any, None],
) -> None:
    from src.db.db_connect import uow as uow_

    async def foo() -> AsyncGenerator:
        yield uow

    app.dependency_overrides[uow_] = foo  # type: ignore


@pytest.fixture()
def db_settings() -> DBSettings:
    return DBSettings()
