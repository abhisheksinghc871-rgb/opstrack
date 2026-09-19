from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.models import Incident, IncidentStatus, Task, TaskStatus, User
from app.schemas.schemas import DashboardStats

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

_OVERDUE_THRESHOLD_DAYS = 7


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_tasks = db.query(func.count(Task.id)).scalar() or 0
    total_incidents = db.query(func.count(Incident.id)).scalar() or 0

    tasks_by_status = dict(
        db.query(Task.status, func.count(Task.id)).group_by(Task.status).all()
    )
    tasks_by_priority = dict(
        db.query(Task.priority, func.count(Task.id)).group_by(Task.priority).all()
    )
    incidents_by_status = dict(
        db.query(Incident.status, func.count(Incident.id)).group_by(Incident.status).all()
    )
    incidents_by_severity = dict(
        db.query(Incident.severity, func.count(Incident.id)).group_by(Incident.severity).all()
    )

    open_incidents = (
        db.query(func.count(Incident.id))
        .filter(Incident.status.notin_([IncidentStatus.resolved, IncidentStatus.closed]))
        .scalar()
        or 0
    )

    overdue_cutoff = datetime.utcnow() - timedelta(days=_OVERDUE_THRESHOLD_DAYS)
    overdue_looking_tasks = (
        db.query(func.count(Task.id))
        .filter(Task.status != TaskStatus.done, Task.created_at < overdue_cutoff)
        .scalar()
        or 0
    )

    def _stringify_keys(d: dict) -> dict[str, int]:
        return {(k.value if hasattr(k, "value") else str(k)): v for k, v in d.items()}

    return DashboardStats(
        total_tasks=total_tasks,
        tasks_by_status=_stringify_keys(tasks_by_status),
        tasks_by_priority=_stringify_keys(tasks_by_priority),
        total_incidents=total_incidents,
        incidents_by_status=_stringify_keys(incidents_by_status),
        incidents_by_severity=_stringify_keys(incidents_by_severity),
        open_incidents=open_incidents,
        overdue_looking_tasks=overdue_looking_tasks,
    )
