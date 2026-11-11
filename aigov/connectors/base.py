"""Connector plug-in interface and registry.

A connector pulls evidence out of a system the entity already runs. To add one:

    from aigov.connectors.base import Connector, register

    @register("jira")
    class JiraConnector(Connector):
        def collect(self):
            return [Evidence(id="jira:RISK-1", connector="jira", kind="api", title=..., text=...)]

Third-party packages can also expose connectors through the ``aigov.connectors``
entry-point group; they are discovered automatically.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from importlib.metadata import entry_points
from typing import Any

from ..models import Evidence

_REGISTRY: dict[str, type["Connector"]] = {}


class Connector(ABC):
    name = "base"

    def __init__(self, **config: Any):
        self.config = config
        self.warnings: list[str] = []

    @abstractmethod
    def collect(self) -> list[Evidence]:
        """Return evidence. Must not raise for a missing optional source; add a warning instead."""


def register(name: str):
    def deco(cls: type[Connector]) -> type[Connector]:
        cls.name = name
        _REGISTRY[name] = cls
        return cls
    return deco


def available() -> dict[str, type[Connector]]:
    from . import documents, http, inventory, mlflow, questionnaire, repo  # noqa: F401  (register built-ins)
    for ep in entry_points(group="aigov.connectors"):
        if ep.name not in _REGISTRY:
            _REGISTRY[ep.name] = ep.load()
    return dict(_REGISTRY)


def build(name: str, **config: Any) -> Connector:
    reg = available()
    if name not in reg:
        raise KeyError(f"unknown connector '{name}'. Available: {', '.join(sorted(reg))}")
    return reg[name](**config)
