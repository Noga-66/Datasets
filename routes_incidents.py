from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.contracts.events import IncidentStatus as S
from backend.contracts.topics import INCIDENTS_UPDATES, VERIFICATION_REQUESTS
from backend.core.deps import current_user, require_role
from backend.core.kafka import publish
from backend.db.models import Incident
from backend.db.session import get_db
from backend.services import incident_service as svc

router = APIRouter(prefix="/incidents", tags=["incidents"])


def _out(i: Incident, with_timeline: bool = False) -> dict:
    d = {"id": i.id, "type": i.type, "lat": i.lat, "lon": i.lon, "status": i.status,
         "priority": i.priority, "score": i.priority_score, "department": i.department_code,
         "reopen_count": i.reopen_count, "sources": sorted({e.source for e in i.events}),
         "created_at": i.created_at}
    if with_timeline:
        d["timeline"] = [{"status": t.status, "actor": t.actor, "note": t.note, "ts": t.ts} for t in i.timeline]
    return d


def _visible(q, user: dict):
    """الصلاحيات في الـ backend: المواطن بلاغاته بس، الإدارة حوادثها بس."""
    if user["role"] == "citizen":
        return q.where(Incident.reporter_id == user["sub"])
    if user["role"] == "department":
        return q.where(Incident.department_code == user.get("dept"))
    return q


@router.get("")
def list_incidents(db: Session = Depends(get_db), user: dict = Depends(current_user)):
    return [_out(i) for i in db.scalars(_visible(select(Incident).order_by(Incident.created_at.desc()), user))]


@router.get("/{incident_id}")
def get_incident(incident_id: str, db: Session = Depends(get_db), user: dict = Depends(current_user)):
    i = db.scalar(_visible(select(Incident).where(Incident.id == incident_id), user))
    if not i:
        raise HTTPException(404, "not found")
    return _out(i, with_timeline=True)


class StatusChange(BaseModel):
    status: S
    note: str = ""


@router.patch("/{incident_id}/status")
def change_status(incident_id: str, body: StatusChange, db: Session = Depends(get_db),
                  user: dict = Depends(require_role("department", "operator", "admin"))):
    i = db.get(Incident, incident_id)
    if not i:
        raise HTTPException(404, "not found")
    if body.status not in (S.RESOLVED,):   # يدويًا: RESOLVED فقط؛ الباقي بتعمله الـ Agents
        raise HTTPException(400, "only RESOLVED can be set manually")
    try:
        svc.advance(db, i, body.status, f"user:{user['sub']}", body.note)
    except svc.InvalidTransition as e:
        raise HTTPException(409, str(e))
    db.flush()
    publish(INCIDENTS_UPDATES, {"incident_id": i.id, "type": i.type, "status": i.status,
                                "priority": i.priority, "department": i.department_code,
                                "lat": i.lat, "lon": i.lon}, key=i.id)
    publish(VERIFICATION_REQUESTS, {"incident_id": i.id, "requested_by": user["sub"]}, key=i.id)
    return _out(i)
