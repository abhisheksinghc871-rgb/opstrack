"""
SQLAlchemy ORM models.

Schema is intentionally kept flat and easy to understand:

    users
    tasks        -> assigned_to (users), created_by (users)
    incidents    -> assigned_to (users), created_by (users)
    comments     -> polymorphic-lite: belongs to either a task or an incident
"""
import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    blocked = "blocked"
    done = "done"


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class IncidentSeverity(str, enum.Enum):
    sev1 = "sev1"
    sev2 = "sev2"
    sev3 = "sev3"
    sev4 = "sev4"


class IncidentStatus(str, enum.Enum):
    open = "open"
    investigating = "investigating"
    mitigated = "mitigated"
    resolved = "resolved"
    closed = "closed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tasks_created = relationship(
        "Task", foreign_keys="Task.created_by_id", back_populates="created_by"
    )
    tasks_assigned = relationship(
        "Task", foreign_keys="Task.assigned_to_id", back_populates="assigned_to"
    )
    incidents_created = relationship(
        "Incident", foreign_keys="Incident.created_by_id", back_populates="created_by"
    )
    incidents_assigned = relationship(
        "Incident", foreign_keys="Incident.assigned_to_id", back_populates="assigned_to"
    )
    comments = relationship("Comment", back_populates="author")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, native_enum=False), default=TaskStatus.todo, nullable=False
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority, native_enum=False), default=TaskPriority.medium, nullable=False
    )
    created_by_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    assigned_to_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="tasks_created")
    assigned_to = relationship(
        "User", foreign_keys=[assigned_to_id], back_populates="tasks_assigned"
    )
    comments = relationship(
        "Comment",
        primaryjoin="and_(Comment.entity_type=='task', foreign(Comment.entity_id)==Task.id)",
        viewonly=True,
        order_by="Comment.created_at",
    )


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    severity: Mapped[IncidentSeverity] = mapped_column(
        Enum(IncidentSeverity, native_enum=False), default=IncidentSeverity.sev3, nullable=False
    )
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus, native_enum=False), default=IncidentStatus.open, nullable=False
    )
    created_by_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    assigned_to_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_by = relationship(
        "User", foreign_keys=[created_by_id], back_populates="incidents_created"
    )
    assigned_to = relationship(
        "User", foreign_keys=[assigned_to_id], back_populates="incidents_assigned"
    )
    comments = relationship(
        "Comment",
        primaryjoin="and_(Comment.entity_type=='incident', foreign(Comment.entity_id)==Incident.id)",
        viewonly=True,
        order_by="Comment.created_at",
    )


class Comment(Base):
    """A comment/note attached to either a Task or an Incident."""

    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    entity_type: Mapped[str] = mapped_column(String(20), nullable=False)  # "task" | "incident"
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="comments")
