from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

import asyncpg
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from structlog.stdlib import BoundLogger

from diecastor.settings.config import DatabaseSettings


class DatabaseError(Exception): ...


class Database:
    def __init__(
        self, db_settings: DatabaseSettings, logger: BoundLogger
    ) -> None:
        self._settings = db_settings
        self._logger = logger

        self._engine = self._create_engine()
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine
        )

    def _create_engine(self) -> AsyncEngine:
        """Create and configure the SQLAlchemy async engine.

        Returns:
            AsyncEngine: A configured SQLAlchemy async engine instance.

        Raises:
            DatabaseError: If the engine creation fails for any reason.
        """
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
        """Create a new asyncpg database connection."""
        return await asyncpg.connect(
            host=self._settings.host,
            port=self._settings.port,
            user=self._settings.user,
            password=self._settings.password,
            database=self._settings.database
        )

    @asynccontextmanager
    async def session(self, commit=False) -> AsyncIterator[AsyncSession]:
        """Provide a database session from the connection pool.

        The session is automatically closed when the context exits.

        Args:
            commit: If True, automatically commit the transaction after the
                session is used. If False, the caller is responsible for
                committing or rolling back.

        Yields:
            AsyncSession: A SQLAlchemy async database session.

        Raises:
            DatabaseError: If the database is not properly initialized.

        Note:
            If an exception occurs during session usage, the transaction will
            be automatically rolled back. The session is always closed in the
            finally block, regardless of success or failure.
        """
        if not self._sessionmaker:
            self._logger.error("database_not_initialized")
            raise DatabaseError()

        self._logger.info("providing session from a connection pool...")
        session = self._sessionmaker()
        try:
            yield session
            if commit:
                await session.commit()
        except Exception as e:
            self._logger.exception("session.error", error=str(e))
            await session.rollback()
        finally:
            await session.aclose()
            self._logger.info("Session closed.")

    async def close(self) -> None:
        """Close the database engine and dispose of all connections.

        This method should be called during application shutdown to properly
        clean up database resources.
        """
        await self._engine.dispose()
        self._logger.info("Engine disposed and all connections closed.")


def get_db(request: Request) -> Database:
    """Return database object from the app's state,
    injected within the lifespan init.
    """
    return request.app.state.database


DatabaseDependency = Annotated[
    Database, Depends(get_db)
]
