"""Data models shared by the rule library, connectors, the test engine, reports and the web platform."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Status = Literal["met", "partial", "gap", "not_applicable"]
RiskTier = Literal["prohibited", "high", "limited", "minimal"]
Priority = Literal["critical", "high", "medium", "low"]
AnswerValue = Literal["yes", "partial", "no", "na"]


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
    gpai_model_provider: bool = False     # the entity provides a general-purpose AI model
    consumer_facing: bool = False
    automated_decisions: bool = False     # decisions without meaningful human involvement
    risk_tier: Optional[RiskTier] = None  # declared tier; screened automatically as well
    assessed_risk_tier: Optional[RiskTier] = None
    risk_rationale: str = ""


class Entity(BaseModel):
    name: str
    sector: str = ""
    jurisdictions: list[str] = Field(default_factory=list)  # EU, US, US-CO, US-NY, IN, UK ...
    size: str = ""
    attributes: list[str] = Field(default_factory=list)     # entity-level applicability flags


class Profile(BaseModel):
    entity: Entity
    systems: list[AISystem] = Field(default_factory=list)


# --------------------------------------------------------------------------- evidence and answers
class Evidence(BaseModel):
    id: str
    connector: str
    kind: Literal["document", "repository", "inventory", "attestation", "api"]
    title: str
    ref: str = ""
    text: str = ""
    signals: dict[str, Any] = Field(default_factory=dict)


class Answer(BaseModel):
    """Answer to one test. `test_id` may also be a requirement id, which answers all its tests."""
    test_id: str
    answer: AnswerValue
    note: str = ""
    evidence_ref: str = ""


# --------------------------------------------------------------------------- rule library
class Remediation(BaseModel):
    action: str
    effort: Literal["low", "medium", "high"] = "medium"
    owner: str = ""


class Control(BaseModel):
    """Best-practice control: evidence checks + default remediation, shared by many articles."""
    id: str
    domain: str
    title: str
    objective: str
    weight: int = 2
    conditions: list[str] = Field(default_factory=list)
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


class RuleTest(BaseModel):
    id: str
    question: str


class Requirement(BaseModel):
    """One article / section / clause of a law or standard."""
    model_config = ConfigDict(extra="forbid")  # a YAML typo must fail loudly, not vanish
    id: str
    framework: str
    ref: str
    title: str
    chapter: str = ""
    kind: Literal["obligation", "info"] = "obligation"
    summary: str = ""
    note: str = ""
    need: list[str] = Field(default_factory=list)   # all flags required
    when: list[str] = Field(default_factory=list)   # at least one flag required
    tests: list[RuleTest] = Field(default_factory=list)
    controls: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)  # extra evidence phrases (custom rules)
    weight: int = 2
    binding: Optional[bool] = None                  # overrides the framework's binding flag
    action: str = ""                                # requirement-specific remediation
    owner: str = ""
    custom: bool = False


# --------------------------------------------------------------------------- results
class Citation(BaseModel):
    source: str
    quote: str


class Recommendation(BaseModel):
    action: str
    priority: Priority = "medium"
    effort: Literal["low", "medium", "high"] = "medium"
    owner: str = ""
    control_id: str = ""


class TestResult(BaseModel):
    test_id: str
    question: str
    answer: Optional[AnswerValue] = None
    score: Optional[float] = None
    basis: Literal["verified", "attested", "partial", "failed", "not_applicable", "evidence", "no_evidence"] = "no_evidence"
    note: str = ""
    evidence_ref: str = ""


class RequirementResult(BaseModel):
    id: str
    framework: str
    ref: str
    title: str
    chapter: str = ""
    domain: str = ""
    status: Status
    score: float = 0.0
    confidence: Literal["low", "medium", "high"] = "low"
    rationale: str = ""
    tests: list[TestResult] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    recommendations: list[Recommendation] = Field(default_factory=list)
    controls: list[str] = Field(default_factory=list)
    legally_binding: bool = False
    priority: Optional[Priority] = None
    weight: int = 2


class FrameworkScore(BaseModel):
    key: str
    name: str
    citation: str
    binding: bool
    applicable: bool
    reason: str = ""
    note: str = ""
    score: Optional[float] = None
    articles_total: int = 0        # every article/section in the library
    articles_assessable: int = 0   # articles that carry obligations
    in_scope: int = 0
    met: int = 0
    partial: int = 0
    gap: int = 0


class Assessment(BaseModel):
    id: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))
    tool_version: str = ""
    method: str = "rule-based"
    profile: Profile
    flags: list[str] = Field(default_factory=list)
    overall_score: float = 0.0
    maturity: str = ""
    frameworks: list[FrameworkScore] = Field(default_factory=list)
    domains: dict[str, float] = Field(default_factory=dict)
    results: list[RequirementResult] = Field(default_factory=list)
    tests_total: int = 0
    tests_answered: int = 0
    executive_summary: str = ""
    roadmap: list[dict[str, Any]] = Field(default_factory=list)
    evidence_index: list[dict[str, str]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    def gaps(self) -> list[RequirementResult]:
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        items = [r for r in self.results if r.status in ("gap", "partial")]
        return sorted(items, key=lambda r: (order.get(r.priority or "low", 3), r.score, r.framework, r.id))
