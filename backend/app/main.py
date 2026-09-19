import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import auth, comments, dashboard, health, incidents, tasks, users
from app.core.config import settings
from app.core.logging import configure_logging, log_requests_middleware
from app.db.database import Base, engine

configure_logging()
logger = logging.getLogger("opstrack")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Simple schema bootstrap. A DevOps/production setup may later swap
    # this for a proper migration tool (e.g. Alembic) - kept simple here
    # on purpose so the app is easy to run locally out of the box.
    Base.metadata.create_all(bind=engine)
    logger.info("application_startup env=%s", settings.APP_ENV)
    yield
    logger.info("application_shutdown")


app = FastAPI(
    title="OpsTrack API",
    description="Task & Incident Management Platform for small engineering/operations teams.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_requests_middleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("validation_error path=%s errors=%s", request.url.path, exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(incidents.router)
app.include_router(comments.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "status": "running",
        "docs": "/api/docs",
    }
