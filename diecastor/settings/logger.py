from typing import Annotated

from fastapi import Depends
import structlog.stdlib as logger
from structlog.stdlib import BoundLogger


def get_logger() -> BoundLogger:
    return logger.get_logger()


LoggerDependency = Annotated[BoundLogger, Depends(get_logger)]
