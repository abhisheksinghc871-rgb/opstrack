"""
Application-level structured logging.

Keeps logging intentionally simple (stdout, structured key=value style
lines) so a DevOps engineer can later ship these logs to any log
aggregation stack (CloudWatch, Loki, ELK, etc.) without changing the
application. No log shipping / aggregation is implemented here.
"""
import logging
import sys
import time
from typing import Callable

from fastapi import Request

from app.core.config import settings

LOG_FORMAT = "%(asctime)s level=%(levelname)s logger=%(name)s message=%(message)s"


def configure_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format=LOG_FORMAT,
        stream=sys.stdout,
    )
    # Quiet down noisy third-party loggers a little in non-debug envs.
    if settings.LOG_LEVEL.upper() != "DEBUG":
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


logger = logging.getLogger("opstrack")


async def log_requests_middleware(request: Request, call_next: Callable):
    """Logs method, path, status code and duration for every request."""
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = round((time.time() - start_time) * 1000, 2)
        logger.exception(
            "request_failed method=%s path=%s duration_ms=%s",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = round((time.time() - start_time) * 1000, 2)
    logger.info(
        "request_handled method=%s path=%s status_code=%s duration_ms=%s client=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        request.client.host if request.client else "unknown",
    )
    return response
