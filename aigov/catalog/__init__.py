"""Loads the framework registry and the unified control catalog."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from ..models import Control, Framework

_DIR = Path(__file__).parent


@lru_cache
def load_frameworks(path: str | None = None) -> dict[str, Framework]:
    data = yaml.safe_load(Path(path or _DIR / "frameworks.yaml").read_text())
    return {k: Framework(key=k, **v) for k, v in data["frameworks"].items()}


@lru_cache
def load_controls(path: str | None = None) -> list[Control]:
    data = yaml.safe_load(Path(path or _DIR / "controls.yaml").read_text())
    controls = [Control(**c) for c in data["controls"]]
    known = set(load_frameworks())
    ids = set()
    for c in controls:
        if c.id in ids:
            raise ValueError(f"duplicate control id {c.id}")
        ids.add(c.id)
        unknown = set(c.mappings) - known
        if unknown:
            raise ValueError(f"{c.id} maps to unknown framework(s): {sorted(unknown)}")
    return controls
