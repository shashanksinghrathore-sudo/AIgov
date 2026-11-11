"""Data models shared by connectors, the assessment engine and reports."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

Status = Literal["met", "partial", "gap", "not_applicable"]
RiskTier = Literal["prohibited", "high", "limited", "minimal"]
Priority = Literal["critical", "high", "medium", "low"]


# --------------------------------------------------------------------------- profile
class AISystem(BaseModel):
    id: str
    name: str
    description: str = ""
    purpose: str = ""
    role: Literal["provider", "deployer", "both"] = "deployer"
    domain: str = ""                      # e.g. employment, credit, healthcare, customer service
    owner: str = ""
    vendor: str = ""
    model: str = ""
    uses_personal_data: bool = False
    generative: bool = False
    gpai_model_provider: bool = False     # the entity itself provides a general-purpose AI model
    consumer_facing: bool = False
    automated_decisions: bool = False     # decisions without meaningful human involvement
    risk_tier: Optional[RiskTier] = None  # declared tier; classified automatically when absent
    # filled in by the engine
    assessed_risk_tier: Optional[RiskTier] = None
    risk_rationale: str = ""


class Entity(BaseModel):
    name: str
    sector: str = ""
    jurisdictions: list[str] = Field(default_factory=list)  # EU, US, US-CO, US-NY, IN, UK ...
    size: str = ""


class Profile(BaseModel):
    entity: Entity
    systems: list[AISystem] = Field(default_factory=list)


# --------------------------------------------------------------------------- evidence
class Evidence(BaseModel):
    """One unit of evidence gathered by a connector."""
    id: str
    connector: str
    kind: Literal["document", "repository", "inventory", "attestation", "api"]
    title: str
    ref: str = ""                 # path / URL / record id
    text: str = ""                # content assessors can read and quote
    signals: dict[str, Any] = Field(default_factory=dict)  # machine-detected facts


class Attestation(BaseModel):
    """Self-assessment answer for one control."""
    control_id: str
    answer: Literal["yes", "partial", "no", "na"]
    notes: str = ""
    evidence_ref: str = ""


# --------------------------------------------------------------------------- catalog
class Remediation(BaseModel):
    action: str
    effort: Literal["low", "medium", "high"] = "medium"
    owner: str = ""


class Control(BaseModel):
    id: str
    domain: str
    title: str
    objective: str
    weight: int = 2
    conditions: list[str] = Field(default_factory=list)
    mappings: dict[str, list[str]] = Field(default_factory=dict)
    indicators: list[list[str]] = Field(default_factory=list)
    signals: list[str] = Field(default_factory=list)
    remediation: Remediation


class Framework(BaseModel):
    key: str
    name: str
    citation: str
    kind: str
    binding: bool
    region: str
    applies_when: dict[str, list[str]] = Field(default_factory=dict)
    note: str = ""


# --------------------------------------------------------------------------- results
class Citation(BaseModel):
    source: str            # evidence id
    quote: str
    verified: bool = True  # quote was found verbatim in the evidence text


class Recommendation(BaseModel):
    action: str
    priority: Priority = "medium"
    effort: Literal["low", "medium", "high"] = "medium"
    owner: str = ""


class ControlResult(BaseModel):
    control_id: str
    domain: str
    title: str
    status: Status
    score: float = 0.0                       # 0..1
    confidence: Literal["low", "medium", "high"] = "low"
    method: Literal["ai", "rules"] = "rules"
    rationale: str = ""
    gaps: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    recommendations: list[Recommendation] = Field(default_factory=list)
    frameworks: dict[str, list[str]] = Field(default_factory=dict)  # applicable mappings only
    legally_binding: bool = False
    priority: Optional[Priority] = None      # set for partial / gap
    weight: int = 2


class FrameworkScore(BaseModel):
    key: str
    name: str
    citation: str
    binding: bool
    applicable: bool
    reason: str = ""
    note: str = ""
    score: Optional[float] = None            # 0..100
    controls_total: int = 0
    controls_met: int = 0
    controls_partial: int = 0
    controls_gap: int = 0


class Assessment(BaseModel):
    id: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))
    tool_version: str = ""
    mode: Literal["ai", "rules"] = "rules"
    model: str = ""
    profile: Profile
    flags: list[str] = Field(default_factory=list)
    overall_score: float = 0.0               # 0..100
    maturity: str = ""
    frameworks: list[FrameworkScore] = Field(default_factory=list)
    domains: dict[str, float] = Field(default_factory=dict)
    results: list[ControlResult] = Field(default_factory=list)
    executive_summary: str = ""
    roadmap: list[dict[str, Any]] = Field(default_factory=list)
    evidence_index: list[dict[str, str]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    def gaps(self) -> list[ControlResult]:
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        items = [r for r in self.results if r.status in ("gap", "partial")]
        return sorted(items, key=lambda r: (order.get(r.priority or "low", 3), r.score, r.control_id))
