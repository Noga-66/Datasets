from backend.agents.base import BaseAgent
from backend.contracts.events import IncidentType, RoutingResult

# جدول مسؤوليات الإدارات (الأساس). RAG على اللوائح للحالات الغامضة = تحسين لاحق.
TYPE_TO_DEPT = {
    IncidentType.WATER_LEAK: "water",
    IncidentType.FIRE_SMOKE: "civil_defense",
    IncidentType.GARBAGE: "sanitation",
    IncidentType.POTHOLE: "roads",
}


class RoutingAgent(BaseAgent):
    name = "routing"

    def run(self, itype: IncidentType) -> RoutingResult:
        dept = TYPE_TO_DEPT.get(itype)
        if dept:
            return RoutingResult(department_code=dept, reason=f"{itype.value} handled by {dept}", source="table")
        return RoutingResult(department_code=None, reason="no owner found; manual routing required", source="none")
