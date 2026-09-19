import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.models import Incident, IncidentSeverity, IncidentStatus, User
from app.schemas.schemas import IncidentCreate, IncidentOut, IncidentUpdate

router = APIRouter(prefix="/api/incidents", tags=["incidents"])
logger = logging.getLogger("opstrack")

_RESOLVED_STATES = {IncidentStatus.resolved, IncidentStatus.closed}


@router.post("", response_model=IncidentOut, status_code=status.HTTP_201_CREATED)
def create_incident(
    payload: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.assigned_to_id:
        assignee = db.query(User).filter(User.id == payload.assigned_to_id).first()
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="assigned_to_id does not exist"
            )

    incident = Incident(
        title=payload.title,
        description=payload.description,
        severity=payload.severity,
        assigned_to_id=payload.assigned_to_id,
        created_by_id=current_user.id,
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    logger.info(
        "incident_created incident_id=%s severity=%s created_by=%s",
        incident.id,
        incident.severity,
        current_user.id,
    )
    return incident


@router.get("", response_model=list[IncidentOut])
def list_incidents(
    status_filter: IncidentStatus | None = Query(default=None, alias="status"),
    severity: IncidentSeverity | None = Query(default=None),
    assigned_to_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Incident)
    if status_filter:
        query = query.filter(Incident.status == status_filter)
    if severity:
        query = query.filter(Incident.severity == severity)
    if assigned_to_id:
        query = query.filter(Incident.assigned_to_id == assigned_to_id)
    return query.order_by(Incident.created_at.desc()).all()


def _get_incident_or_404(incident_id: str, db: Session) -> Incident:
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return incident


@router.get("/{incident_id}", response_model=IncidentOut)
def get_incident(
    incident_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _get_incident_or_404(incident_id, db)


@router.patch("/{incident_id}", response_model=IncidentOut)
def update_incident(
    incident_id: str,
    payload: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incident = _get_incident_or_404(incident_id, db)
    update_data = payload.model_dump(exclude_unset=True)

    if "assigned_to_id" in update_data and update_data["assigned_to_id"]:
        assignee = db.query(User).filter(User.id == update_data["assigned_to_id"]).first()
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="assigned_to_id does not exist"
            )

    for field, value in update_data.items():
        setattr(incident, field, value)

    if "status" in update_data:
        if update_data["status"] in _RESOLVED_STATES and incident.resolved_at is None:
            incident.resolved_at = datetime.utcnow()
        elif update_data["status"] not in _RESOLVED_STATES:
            incident.resolved_at = None

    db.commit()
    db.refresh(incident)
    logger.info(
        "incident_updated incident_id=%s updated_by=%s fields=%s",
        incident.id,
        current_user.id,
        list(update_data.keys()),
    )
    return incident


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(
    incident_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    incident = _get_incident_or_404(incident_id, db)
    db.delete(incident)
    db.commit()
    logger.info("incident_deleted incident_id=%s deleted_by=%s", incident_id, current_user.id)
    return None
