"""Config-driven evidence collection.

    entity: {name: Acme, jurisdictions: [EU, US-CO]}
    systems: [...]                 # or `inventory: systems.csv`
    connectors:
      - {type: documents, path: ./policies}
      - {type: repo, path: ../ml-service}
      - {type: questionnaire, path: answers.yaml}
      - {type: mlflow, url: https://mlflow.internal, token_env: MLFLOW_TOKEN}

Relative paths are resolved against the config file's folder.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from .connectors.base import build
from .connectors.inventory import load_systems
from .connectors.questionnaire import QuestionnaireConnector
from .models import AISystem, Attestation, Entity, Evidence, Profile


def collect(config: dict, base: Path | None = None) -> tuple[Profile, list[Evidence], list[Attestation], list[str]]:
    base = base or Path.cwd()
    systems = [AISystem(**s) for s in config.get("systems", [])]
    if config.get("inventory"):
        systems += load_systems(base / config["inventory"])
    profile = Profile(entity=Entity(**config["entity"]), systems=systems)

    evidence: list[Evidence] = []
    attestations: list[Attestation] = []
    warnings: list[str] = []
    specs = [{"type": "inventory", "systems": systems}] + list(config.get("connectors", []))
    for spec in specs:
        spec = dict(spec)
        kind = spec.pop("type")
        if "path" in spec:
            spec["path"] = str(base / spec["path"])
        conn = build(kind, **spec)
        if isinstance(conn, QuestionnaireConnector):
            attestations += conn.attestations()
        evidence += conn.collect()
        warnings += conn.warnings

    seen: set[str] = set()
    unique = []
    for e in evidence:  # two connectors may read the same file
        if e.id not in seen:
            seen.add(e.id)
            unique.append(e)
    if not any(e.kind in ("document", "api", "repository") for e in unique):
        warnings.append("No documents, repositories or system exports were collected; results rest on attestations only.")
    return profile, unique, attestations, warnings


def collect_file(path: str | Path):
    p = Path(path)
    return collect(yaml.safe_load(p.read_text()), p.parent)
