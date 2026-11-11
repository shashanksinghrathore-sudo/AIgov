"""AI system inventory as evidence (from the profile, or a CSV/JSON/YAML export of a register)."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml

from ..models import AISystem, Evidence
from .base import Connector, register

_TRUE = {"1", "true", "yes", "y"}
_BOOLS = ("uses_personal_data", "generative", "gpai_model_provider", "consumer_facing", "automated_decisions")


def load_systems(path: str | Path) -> list[AISystem]:
    """Read systems from .csv, .json or .yaml (a list, or a mapping with a `systems` key)."""
    p = Path(path)
    if p.suffix.lower() == ".csv":
        rows = list(csv.DictReader(p.open(newline="")))
        for r in rows:
            for b in _BOOLS:
                if b in r:
                    r[b] = str(r[b]).strip().lower() in _TRUE
            if not r.get("risk_tier"):
                r.pop("risk_tier", None)
    else:
        data = json.loads(p.read_text()) if p.suffix.lower() == ".json" else yaml.safe_load(p.read_text())
        rows = data["systems"] if isinstance(data, dict) else data
    return [AISystem(**r) for r in rows]


@register("inventory")
class InventoryConnector(Connector):
    """config: systems (list[AISystem])"""

    def collect(self) -> list[Evidence]:
        systems: list[AISystem] = self.config.get("systems", [])
        if not systems:
            self.warnings.append("inventory: no AI systems declared; applicability is based on jurisdictions only")
            return []
        fields = ("owner", "purpose", "role", "risk_tier")
        complete = sum(all(getattr(s, f) for f in fields) for s in systems)
        lines = [f"AI system inventory: {len(systems)} system(s); {complete} with owner, purpose, role and declared risk tier."]
        for s in systems:
            lines.append(
                f"- {s.id} | {s.name} | role={s.role} | owner={s.owner or 'MISSING'} | declared_tier={s.risk_tier or 'MISSING'} "
                f"| purpose={s.purpose or 'MISSING'} | vendor={s.vendor or '-'} | model={s.model or '-'} "
                f"| personal_data={s.uses_personal_data} | generative={s.generative} | automated_decisions={s.automated_decisions}"
            )
        return [Evidence(
            id="inventory", connector="inventory", kind="inventory", title="AI system inventory", text="\n".join(lines),
            signals={"inventory_present": True, "inventory_systems": len(systems), "inventory_complete": complete},
        )]
