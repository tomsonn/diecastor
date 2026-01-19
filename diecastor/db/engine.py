from typing import Annotated, AsyncIterator

import asyncpg
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from diecastor.settings.config import DatabaseSettings
from diecastor.settings.logger import LoggerDependency


class DatabaseError(Exception):
    ...


class Database:
    def __init__(
        self, db_settings: DatabaseSettings, logger: LoggerDependency
    ) -> None:
        self._settings = db_settings
        self._logger = logger

        self._engine = self._create_engine()
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine
        )

    def _create_engine(self) -> AsyncEngine:
        self._logger.info("Establishing database connection...")
        try:
            return create_async_engine(
                self._settings.driver,
                async_creator=self._get_connection,
                **self._settings.pool_config.model_dump()
            )
        except Exception as e:
            self._logger.exception("create_engine.error", error=str(e))
            raise DatabaseError

    async def _get_connection(self) -> asyncpg.Connection:
        return await asyncpg.connect(
            host=self._settings.host,
            port=self._settings.port,
            user=self._settings.user,
            password=self._settings.password,
            database=self._settings.database
        )

    async def session(self, commit=False) -> AsyncIterator[AsyncSession]:
        if not self._sessionmaker:
            self._logger.error("database_not_initialized")
            raise DatabaseError()

        self._logger.info("providing session from a connection pool...")
        session = self._sessionmaker()
        try:
            if commit:
                yield session
                await session.commit()
        except Exception as e:
            self._logger.exception("session.error", error=str(e))
            await session.rollback()
        finally:
            await session.aclose()
            self._logger.info("Session closed.")

    async def close(self) -> None:
        await self._engine.dispose()
        self._logger.info("Engine disposed and all connections closed.")


async def get_db_session(
    db_settings: DatabaseSettings,
    logger: LoggerDependency
) -> AsyncIterator[AsyncSession]:
    database = Database(db_settings, logger)
    async with database.session() as session:
        yield session


DatabaseSessionDependency = Annotated[
    AsyncIterator[AsyncSession], Depends(get_db_session)
]
