import structlog.stdlib as logger
from structlog.stdlib import BoundLogger


def get_logger() -> BoundLogger:
    return logger.get_logger("diecastor")
