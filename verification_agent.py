"""Verification Agent: قبل/بعد. القرار: كل الفحوصات المتاحة نجحت => VERIFIED، أي فشل => REOPENED."""
from backend.agents.base import BaseAgent


class VerificationAgent(BaseAgent):
    name = "verification"

    def run(self, checks: dict[str, bool | None]) -> tuple[bool, list[str]]:
        """checks: اسم الفحص -> True نجح / False فشل / None مش متاح (بيتسجل ويتجاهل)."""
        notes, ok = [], True
        for name, res in checks.items():
            if res is None:
                notes.append(f"{name}: not available, skipped")
            elif res:
                notes.append(f"{name}: passed")
            else:
                notes.append(f"{name}: FAILED")
                ok = False
        if all(v is None for v in checks.values()):
            return False, notes + ["no check available: needs human review"]
        return ok, notes
