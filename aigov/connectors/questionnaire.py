"""Self-assessment answers keyed by control id.

    GOV-01: {answer: yes, notes: "Policy v2 approved March 2026", evidence_ref: "policies/ai-policy.md"}
    OPS-02: no
"""
from __future__ import annotations

from pathlib import Path

import yaml

from ..models import Attestation, Evidence
from .base import Connector, register


def parse_answers(data: dict) -> list[Attestation]:
    out = []
    for cid, v in (data or {}).items():
        if isinstance(v, bool):  # YAML parses bare yes/no as booleans
            v = "yes" if v else "no"
        if isinstance(v, str):
            v = {"answer": v}
        v = dict(v)
        if isinstance(v.get("answer"), bool):
            v["answer"] = "yes" if v["answer"] else "no"
        out.append(Attestation(control_id=cid, **v))
    return out


@register("questionnaire")
class QuestionnaireConnector(Connector):
    """config: path (YAML/JSON file) or answers (dict)"""

    def attestations(self) -> list[Attestation]:
        if "answers" in self.config:
            return parse_answers(self.config["answers"])
        p = Path(self.config["path"])
        if not p.exists():
            self.warnings.append(f"questionnaire: file not found: {p}")
            return []
        return parse_answers(yaml.safe_load(p.read_text()))

    def collect(self) -> list[Evidence]:
        items = self.attestations()
        if not items:
            return []
        lines = ["Self-assessment answers (management attestations, not independently verified):"]
        for a in items:
            extra = "; ".join(x for x in (a.notes, f"evidence: {a.evidence_ref}" if a.evidence_ref else "") if x)
            lines.append(f"- {a.control_id}: {a.answer}" + (f" ({extra})" if extra else ""))
        return [Evidence(
            id="attestations", connector="questionnaire", kind="attestation", title="Self-assessment questionnaire",
            text="\n".join(lines), signals={"attestations": {a.control_id: a.model_dump() for a in items}},
        )]
