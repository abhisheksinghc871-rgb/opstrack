"""
SQLAlchemy engine and session management.

The database connection is fully driven by the DATABASE_URL environment
variable so the same code works locally, in Docker, and in whatever
production environment the DevOps engineer provisions.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# `connect_args` here is only applied for SQLite (used in the automated
# test suite); PostgreSQL ignores it because we branch on the URL scheme.
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency that yields a database session per-request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
