"""Config-driven evidence collection (used by the CLI and CI).

    entity: {name: Acme, jurisdictions: [EU, US-CO], attributes: [international_transfers]}
    systems: [...]                 # or `inventory: systems.csv`
    connectors:
      - {type: documents, path: ./policies}
      - {type: repo, path: ../ml-service}
      - {type: questionnaire, path: answers.yaml}
    custom_rules: rules.yaml       # optional, same format as the built-in rule library

Relative paths are resolved against the config file's folder. All connectors read local files only.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from .catalog import build_requirement
from .connectors.base import build
from .connectors.inventory import load_systems
from .connectors.questionnaire import QuestionnaireConnector
from .models import AISystem, Answer, Entity, Evidence, Profile, Requirement


def load_custom_rules(path: Path) -> list[Requirement]:
    data = yaml.safe_load(path.read_text())
    out = []
    for item in data.get("rules", []):
        item = dict(item)
        fw = item.pop("framework", "custom")
        out.append(build_requirement(fw, "CUSTOM", item, item.pop("chapter", "Custom rules"), custom=True))
    return out


def collect(config: dict, base: Path | None = None):
    """Returns (profile, evidence, answers, custom_rules, warnings)."""
    base = base or Path.cwd()
    systems = [AISystem(**s) for s in config.get("systems", [])]
    if config.get("inventory"):
        systems += load_systems(base / config["inventory"])
    profile = Profile(entity=Entity(**config["entity"]), systems=systems)

    evidence: list[Evidence] = []
    answers: list[Answer] = []
    warnings: list[str] = []
    for spec in [{"type": "inventory", "systems": systems}] + list(config.get("connectors", [])):
        spec = dict(spec)
        kind = spec.pop("type")
        if "path" in spec:
            spec["path"] = str(base / spec["path"])
        conn = build(kind, **spec)
        if isinstance(conn, QuestionnaireConnector):
            answers += conn.answers()
        evidence += conn.collect()
        warnings += conn.warnings

    seen: set[str] = set()
    unique = [e for e in evidence if not (e.id in seen or seen.add(e.id))]
    custom = load_custom_rules(base / config["custom_rules"]) if config.get("custom_rules") else []
    return profile, unique, answers, custom, warnings


def collect_file(path: str | Path):
    p = Path(path)
    return collect(yaml.safe_load(p.read_text()), p.parent)
