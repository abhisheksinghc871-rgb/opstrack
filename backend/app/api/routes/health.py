"""
Health endpoints.

These are consumed by container orchestrators (Docker healthcheck,
Kubernetes liveness/readiness probes) and load balancers, so keep them
fast, dependency-light, and honest about status codes.
"""
import logging

from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.core.config import settings
from app.db.database import SessionLocal

router = APIRouter(tags=["health"])
logger = logging.getLogger("opstrack")


@router.get("/health")
def health():
    """Liveness check: is the application process up and serving requests?"""
    return {"status": "ok", "service": settings.APP_NAME, "env": settings.APP_ENV}


@router.get("/health/db")
def health_db(response: Response):
    """Readiness check: can the application reach the database?"""
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "reachable"}
    except Exception as exc:  # noqa: BLE001 - we want to report any DB failure as unhealthy
        logger.error("health_db_check_failed error=%s", str(exc))
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "database": "unreachable"}
    finally:
        db.close()
