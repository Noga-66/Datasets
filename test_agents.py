from backend.agents.fusion_agent import match_score
from backend.agents.priority_agent import PriorityAgent
from backend.agents.report_agent import ReportAgent
from backend.agents.sensor_agent import SensorAgent
from backend.contracts.events import GeoContext, IncidentStatus as S, IncidentType, Priority
from backend.services.incident_service import can_move


def test_fusion_score_close_and_recent_is_high():
    assert match_score(5, 2, 50, 30, 0.5, 0.3) > 0.8


def test_fusion_score_far_is_zero_space():
    assert match_score(60, 0, 50, 30, 0.5, 0.3) < 0.5


def test_priority_fire_override_is_critical():
    r = PriorityAgent().run(IncidentType.FIRE_SMOKE, None, 1, [0.9])
    assert r.level == Priority.CRITICAL


def test_priority_more_sources_raises_score():
    a = PriorityAgent()
    g = GeoContext()
    one = a.run(IncidentType.WATER_LEAK, g, 1, [0.7]).score
    three = a.run(IncidentType.WATER_LEAK, g, 3, [0.7]).score
    assert three > one


def test_sensor_agent_hard_threshold():
    assert SensorAgent().run("water_flow", 20.0, [])[0] == IncidentType.WATER_LEAK
    assert SensorAgent().run("water_flow", 3.0, [3.0] * 20) is None


def test_report_agent_arabic_dialect():
    r = ReportAgent().run("المية طالعة من ماسورة في الشارع")
    assert r["type"] == IncidentType.WATER_LEAK


def test_state_machine():
    assert can_move(S.ASSIGNED, S.RESOLVED)
    assert not can_move(S.DETECTED, S.VERIFIED)
    assert can_move(S.RESOLVED, S.REOPENED)
