"""Loads the framework registry, the best-practice control library and the article-level rule library."""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import yaml

from ..models import Control, Framework, Requirement, RuleTest

_DIR = Path(__file__).parent


@lru_cache
def load_frameworks() -> dict[str, Framework]:
    data = yaml.safe_load((_DIR / "frameworks.yaml").read_text())
    return {k: Framework(key=k, **v) for k, v in data["frameworks"].items()}


@lru_cache
def load_controls() -> list[Control]:
    data = yaml.safe_load((_DIR / "controls.yaml").read_text())
    controls = [Control(**c) for c in data["controls"]]
    if len({c.id for c in controls}) != len(controls):
        raise ValueError("duplicate control id")
    return controls


def controls_by_id() -> dict[str, Control]:
    return {c.id: c for c in load_controls()}


def ref_slug(ref: str) -> str:
    s = ref.upper().replace("ARTICLE", "ART").replace("SECTION", "S")
    s = re.sub(r"[^A-Z0-9.()-]+", "", s).replace("(", ".").replace(")", "")
    return s.strip(".")


def build_requirement(framework: str, prefix: str, item: dict, chapter: str = "", custom: bool = False) -> Requirement:
    item = dict(item)
    rid = item.pop("id", None) or f"{prefix}.{ref_slug(item['ref'])}"
    tests = item.pop("tests", None) or []
    kind = item.get("kind", "obligation")
    if kind != "info" and not tests:
        tests = [item.get("summary") or item["title"]]
    item.setdefault("chapter", chapter)
    return Requirement(
        id=rid, framework=framework, custom=custom,
        tests=[RuleTest(id=f"{rid}-T{i}", question=q) for i, q in enumerate(tests, 1)],
        **item,
    )


@lru_cache
def builtin_requirements() -> tuple[Requirement, ...]:
    out: list[Requirement] = []
    for path in sorted((_DIR / "requirements").glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        blocks = data["frameworks"] if "frameworks" in data else [data]
        for b in blocks:
            for sec in b["sections"]:
                for item in sec["items"]:
                    out.append(build_requirement(b["framework"], b["prefix"], item, sec["chapter"]))
    validate(out)
    return tuple(out)


def validate(reqs: list[Requirement]) -> None:
    fws, ctl = load_frameworks(), controls_by_id()
    seen: set[str] = set()
    for r in reqs:
        if r.id in seen:
            raise ValueError(f"duplicate requirement id {r.id}")
        seen.add(r.id)
        if r.framework not in fws:
            raise ValueError(f"{r.id}: unknown framework {r.framework}")
        bad = [c for c in r.controls if c not in ctl]
        if bad:
            raise ValueError(f"{r.id}: unknown control(s) {bad}")


def load_requirements(custom: list[Requirement] | None = None) -> list[Requirement]:
    reqs = list(builtin_requirements()) + list(custom or [])
    validate(reqs)
    return reqs
