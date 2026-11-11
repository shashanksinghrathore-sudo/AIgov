"""Test answers, keyed by test id (EUAIA.ART.9-T2) or requirement id (EUAIA.ART.9, answers all its tests).

    EUAIA.ART.9: {answer: yes, note: "RMS procedure v3", evidence_ref: model-risk-procedure.md}
    GDPR.ART.35: partial
"""
from __future__ import annotations

from pathlib import Path

import yaml

from ..models import Answer, Evidence
from .base import Connector, register


def parse_answers(data: dict) -> list[Answer]:
    out = []
    for tid, v in (data or {}).items():
        if isinstance(v, bool):  # YAML reads bare yes/no as booleans
            v = "yes" if v else "no"
        if isinstance(v, str):
            v = {"answer": v}
        v = dict(v)
        if isinstance(v.get("answer"), bool):
            v["answer"] = "yes" if v["answer"] else "no"
        if "notes" in v:
            v["note"] = v.pop("notes")
        out.append(Answer(test_id=str(tid), **v))
    return out


@register("questionnaire")
class QuestionnaireConnector(Connector):
    """Answers to compliance tests from a YAML/JSON file (path) or a dict (answers)."""

    def answers(self) -> list[Answer]:
        if "answers" in self.config:
            return parse_answers(self.config["answers"])
        p = Path(self.config["path"])
        if not p.exists():
            self.warnings.append(f"questionnaire: file not found: {p}")
            return []
        return parse_answers(yaml.safe_load(p.read_text()))

    def collect(self) -> list[Evidence]:
        return []  # answers are passed to the engine directly, not treated as documentary evidence
