"""الـ Orchestrator: Fusion -> Geo -> Priority -> Routing -> حفظ -> نشر تحديث.
(دالة عادية؛ ممكن تتحول لـ LangGraph بعدين من غير ما الـ Agents تتغير.)"""
from sqlalchemy.orm import Session
from backend.agents.fusion_agent import FusionAgent
from backend.agents.geo_agent import GeoAgent
from backend.agents.priority_agent import PriorityAgent
from backend.agents.routing_agent import RoutingAgent
from backend.contracts.events import Event, IncidentStatus as S, IncidentType
from backend.contracts.topics import INCIDENTS_UPDATES
from backend.core.kafka import publish
from backend.db.models import EventRow, Incident
from backend.services import incident_service as svc

fusion, geo, priority, routing = FusionAgent(), GeoAgent(), PriorityAgent(), RoutingAgent()


def process_event(s: Session, ev: Event) -> Incident:
    if s.get(EventRow, ev.id):  # idempotency: نفس الرسالة اتعالجت قبل كده
        return s.get(Incident, s.get(EventRow, ev.id).incident_id)

    fr = fusion.run(s, ev)
    if fr.action == "merge":
        inc = s.get(Incident, fr.incident_id)
        svc.log(s, inc, "agent:fusion", f"merged {ev.source} event (score {fr.match_score}): " + "; ".join(fr.reasons))
    else:
        inc = Incident(type=ev.type.value, lat=ev.lat, lon=ev.lon, reporter_id=ev.payload.get("user_id"))
        s.add(inc); s.flush()
        svc.log(s, inc, f"agent:{ev.source}", f"detected {ev.type.value} (conf {ev.confidence})")
        svc.advance(s, inc, S.ANALYZED, f"agent:{ev.source}", "event understood")
        svc.advance(s, inc, S.FUSED, "agent:fusion", "; ".join(fr.reasons))

    s.add(EventRow(id=ev.id, incident_id=inc.id, source=ev.source, type=ev.type.value,
                   confidence=ev.confidence, lat=ev.lat, lon=ev.lon, ts=ev.timestamp,
                   device_id=ev.device_id, object_key=ev.object_key, payload=ev.payload))
    s.flush(); s.refresh(inc)

    g = geo.run(s, inc.lat, inc.lon)
    evs = inc.events
    pr = priority.run(IncidentType(inc.type), g, len({e.source for e in evs}), [e.confidence for e in evs])
    inc.priority, inc.priority_score = pr.level.value, pr.score
    note = f"{pr.level.value} (score {pr.score}) breakdown={pr.breakdown}"

    if inc.status == S.FUSED.value:
        svc.advance(s, inc, S.PRIORITIZED, "agent:priority", note)
        rt = routing.run(IncidentType(inc.type))
        if rt.department_code:
            inc.department_code = rt.department_code
            svc.advance(s, inc, S.ASSIGNED, "agent:routing", rt.reason)
        else:
            svc.log(s, inc, "agent:routing", rt.reason)  # يفضل PRIORITIZED = طابور يدوي للمشغّل
    else:
        svc.log(s, inc, "agent:priority", "re-evaluated: " + note)

    s.flush()
    publish(INCIDENTS_UPDATES, {"incident_id": inc.id, "type": inc.type, "status": inc.status,
                                "priority": inc.priority, "department": inc.department_code,
                                "lat": inc.lat, "lon": inc.lon}, key=inc.id)
    return inc
