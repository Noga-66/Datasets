"""State Machine لدورة حياة الحادث. هو الوحيد المسموح له يغيّر status."""
from sqlalchemy.orm import Session
from backend.contracts.events import IncidentStatus as S
from backend.db.models import Incident, TimelineEntry

ALLOWED: dict[S, set[S]] = {
    S.DETECTED: {S.ANALYZED},
    S.ANALYZED: {S.FUSED},
    S.FUSED: {S.PRIORITIZED},
    S.PRIORITIZED: {S.ASSIGNED},
    S.ASSIGNED: {S.RESOLVED},
    S.RESOLVED: {S.VERIFIED, S.REOPENED},
    S.REOPENED: {S.ASSIGNED},
    S.VERIFIED: set(),
}


class InvalidTransition(Exception):
    pass


def can_move(current: S, new: S) -> bool:
    return new in ALLOWED[current]


def advance(session: Session, inc: Incident, new: S, actor: str, note: str = "") -> Incident:
    current = S(inc.status)
    if not can_move(current, new):
        raise InvalidTransition(f"{current.value} -> {new.value} not allowed")
    inc.status = new.value
    if new == S.REOPENED:
        inc.reopen_count += 1
    session.add(TimelineEntry(incident_id=inc.id, status=new.value, actor=actor, note=note))
    return inc


def log(session: Session, inc: Incident, actor: str, note: str) -> None:
    """سطر في الـ Timeline من غير تغيير الحالة (مثلاً: Event اندمج)."""
    session.add(TimelineEntry(incident_id=inc.id, status=inc.status, actor=actor, note=note))
