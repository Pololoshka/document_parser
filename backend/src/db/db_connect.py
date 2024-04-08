from collections.abc import AsyncGenerator

from fastapi import Depends

from settings import DBSettings
from src.db.uow import SqlAlchemyUnitOfWork


def db_settings() -> DBSettings:
    return DBSettings()


def uow_engine(settings: DBSettings = Depends(db_settings)) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork.from_url(url=settings.db_url)


async def uow(
    uow_engine: SqlAlchemyUnitOfWork = Depends(uow_engine),
) -> AsyncGenerator[SqlAlchemyUnitOfWork, None]:
    async with uow_engine:
        yield uow_engine
