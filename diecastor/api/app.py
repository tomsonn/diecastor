from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
import sqlalchemy
from starlette.responses import JSONResponse

from diecastor.db.engine import Database, DatabaseDependency
from diecastor.settings.config import DatabaseSettings
from diecastor.settings.logger import get_logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    db_settings = DatabaseSettings()
    logger = get_logger()
    database = Database(db_settings, logger)

    app.state.database = database
    try:
        yield
    except Exception as e:
        logger.exception("Application init error", error=str(e))
    finally:
        await database.close()


app = FastAPI(
    title="Diecastor application",
    description="""This application serves as a collector """
                """of the top diecast brands.""",
    lifespan=lifespan
)


@app.get("/ping")
async def ping(database_dependency: DatabaseDependency) -> JSONResponse:
    return JSONResponse({"response": "pong"})
