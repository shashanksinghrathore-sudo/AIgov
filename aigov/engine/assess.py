"""Orchestrates one assessment: scope -> evaluate -> score -> prioritise -> summarise."""
from __future__ import annotations

import uuid

from .. import __version__
from ..catalog import load_controls, load_frameworks
from ..models import Assessment, Attestation, ControlResult, Evidence, FrameworkScore, Profile
from . import ai, rules
from .applicability import classify_profile, control_applies, derive_flags, framework_applies

MATURITY = [(80, "Level 5 - Optimised"), (60, "Level 4 - Managed"), (40, "Level 3 - Defined"), (20, "Level 2 - Developing"), (0, "Level 1 - Initial")]
EFFORT_RANK = {"low": 0, "medium": 1, "high": 2}


def priority_for(weight: int, score: float, binding: bool) -> str:
    """Severity = importance x shortfall, raised when a binding law requires the control."""
    sev = weight * (1 - score) * (1.5 if binding else 1.0)
    return "critical" if sev >= 3.4 else "high" if sev >= 2.0 else "medium" if sev >= 1.0 else "low"


def _weighted(results: list[ControlResult]) -> float | None:
    total = sum(r.weight for r in results)
    return round(100 * sum(r.weight * r.score for r in results) / total, 1) if total else None


def _rules_roadmap(gaps: list[ControlResult]) -> list[dict]:
    phases = [("Stabilise", "0-30 days", []), ("Build", "31-90 days", []), ("Embed", "91-180 days", [])]
    for r in gaps:
        if not r.recommendations:
            continue
        rec = r.recommendations[0]
        quick = EFFORT_RANK[rec.effort] == 0
        idx = 0 if r.priority == "critical" or (r.priority == "high" and quick) else 1 if r.priority in ("high", "medium") else 2
        phases[idx][2].append({"action": rec.action, "owner": rec.owner, "control_ids": [r.control_id]})
    return [{"phase": p, "horizon": h, "actions": a} for p, h, a in phases if a]


def _rules_summary(a: Assessment) -> str:
    gaps = a.gaps()
    crit = [g for g in gaps if g.priority == "critical"]
    binding = [f for f in a.frameworks if f.applicable and f.binding]
    weakest = sorted(a.domains.items(), key=lambda kv: kv[1])[:2]
    high = [s.name for s in a.profile.systems if s.assessed_risk_tier in ("high", "prohibited")]
    paras = [
        f"{a.profile.entity.name} scores {a.overall_score:.0f} out of 100 against the unified AI governance control catalog "
        f"({a.maturity}). {sum(r.status == 'met' for r in a.results)} of {sum(r.status != 'not_applicable' for r in a.results)} "
        f"applicable controls are met, {sum(r.status == 'partial' for r in a.results)} are partly met and "
        f"{sum(r.status == 'gap' for r in a.results)} are gaps.",
    ]
    if binding:
        paras.append(
            "Binding law in scope: " + "; ".join(f"{f.name} ({f.score:.0f}/100)" for f in binding if f.score is not None) + ". "
            + (f"{len(crit)} critical gap(s) carry direct legal exposure: " + ", ".join(f"{g.control_id} {g.title}" for g in crit[:5]) + "." if crit else "No critical gaps were identified.")
            + (f" Systems screened as high-risk: {', '.join(high)}." if high else "")
        )
    if weakest:
        paras.append("Weakest areas: " + " and ".join(f"{d} ({s:.0f}/100)" for d, s in weakest) + ".")
    paras.append(
        "This summary was produced by the rule-based evaluator, which checks whether evidence addresses each control, "
        "not whether the control is effective. Run with AI mode enabled for a substantive review and tailored recommendations."
    )
    return "\n\n".join(paras)


def run_assessment(
    profile: Profile,
    evidence: list[Evidence],
    attestations: list[Attestation] | None = None,
    mode: str = "auto",
    warnings: list[str] | None = None,
    evidence_budget: int = ai.DEFAULT_EVIDENCE_BUDGET,
) -> Assessment:
    """mode: 'ai' (Claude), 'rules' (offline), or 'auto' (AI when credentials are present)."""
    warnings = list(warnings or [])
    frameworks, controls = load_frameworks(), load_controls()
    att = {a.control_id: a for a in (attestations or [])}
    unknown = set(att) - {c.id for c in controls}
    if unknown:
        warnings.append("Questionnaire answers for unknown control ids were ignored: " + ", ".join(sorted(unknown)))

    # 1. Scope
    warnings += classify_profile(profile)
    flags = derive_flags(profile)
    fw_scope = {k: framework_applies(fw, profile, flags) for k, fw in frameworks.items()}
    applicable_fw = {k for k, (ok, _) in fw_scope.items() if ok}
    in_scope = [c for c in controls if control_applies(c, flags, applicable_fw)]
    binding = {c.id: any(frameworks[k].binding for k in c.mappings if k in applicable_fw) for c in controls}

    # 2. Evaluate
    use_ai = mode == "ai" or (mode == "auto" and ai.credentials_present())
    if mode == "auto" and not use_ai:
        warnings.append("No Anthropic credentials found: used the rule-based evaluator. Set ANTHROPIC_API_KEY for AI assessment.")
    signals = rules.merge_signals(evidence)
    results: dict[str, ControlResult] = {}
    assessor = None
    todo = [c for c in in_scope if not (att.get(c.id) and att[c.id].answer == "na")]
    if use_ai and todo:
        try:
            assessor = ai.Assessor(profile, sorted(flags), evidence, evidence_budget)
        except Exception as e:  # SDK missing or client misconfigured
            if mode == "ai":
                raise
            warnings.append(f"AI assessment unavailable ({e}); used the rule-based evaluator.")
        if assessor:
            if assessor.omitted:
                warnings.append(
                    f"{len(assessor.omitted)} evidence item(s) exceeded the evidence budget and were NOT read by the AI assessor: "
                    + ", ".join(assessor.omitted[:20]) + ". Raise --evidence-budget or split the assessment."
                )
            res, errors = assessor.assess(todo, binding)
            results.update({r.control_id: r for r in res})
            for group, err in errors:
                if mode == "ai" and not res:
                    raise ai.AIError(err)
                warnings.append(f"AI assessment failed for {', '.join(c.id for c in group)} ({err}); rule-based result used instead.")
    for c in in_scope:
        if c.id not in results:
            results[c.id] = rules.evaluate_control(c, evidence, signals, att.get(c.id))
    for c in controls:
        if c.id not in results:
            results[c.id] = ControlResult(
                control_id=c.id, domain=c.domain, title=c.title, status="not_applicable", weight=c.weight,
                rationale="Out of scope: no applicable framework requires this control for the declared systems and jurisdictions.",
            )

    # 3. Score and prioritise
    ordered = []
    for c in controls:
        r = results[c.id]
        r.frameworks = {k: v for k, v in c.mappings.items() if k in applicable_fw}
        r.legally_binding = binding[c.id] and r.status != "not_applicable"
        if r.status in ("gap", "partial"):
            r.priority = priority_for(c.weight, r.score, binding[c.id])  # type: ignore[assignment]
            if not r.recommendations:
                from ..models import Recommendation
                r.recommendations = [Recommendation(action=c.remediation.action, effort=c.remediation.effort, owner=c.remediation.owner)]
            for rec in r.recommendations:
                if r.method == "rules":
                    rec.priority = r.priority  # type: ignore[assignment]
        ordered.append(r)
    scored = [r for r in ordered if r.status != "not_applicable"]

    fw_scores = []
    for k, fw in frameworks.items():
        ok, reason = fw_scope[k]
        mine = [r for r in scored if k in r.frameworks]
        fw_scores.append(FrameworkScore(
            key=k, name=fw.name, citation=fw.citation, binding=fw.binding, applicable=ok, reason=reason, note=fw.note,
            score=_weighted(mine) if ok else None, controls_total=len(mine) if ok else 0,
            controls_met=sum(r.status == "met" for r in mine) if ok else 0,
            controls_partial=sum(r.status == "partial" for r in mine) if ok else 0,
            controls_gap=sum(r.status == "gap" for r in mine) if ok else 0,
        ))
    domains: dict[str, float] = {}
    for d in dict.fromkeys(c.domain for c in controls):
        s = _weighted([r for r in scored if r.domain == d])
        if s is not None:
            domains[d] = s
    overall = _weighted(scored) or 0.0
    any_ai = any(r.method == "ai" for r in scored)

    a = Assessment(
        id=uuid.uuid4().hex[:12], tool_version=__version__, mode="ai" if any_ai else "rules",
        model=assessor.model if (assessor and any_ai) else "", profile=profile, flags=sorted(flags),
        overall_score=overall, maturity=next(label for floor, label in MATURITY if overall >= floor),
        frameworks=fw_scores, domains=domains, results=ordered,
        evidence_index=[{"id": e.id, "connector": e.connector, "kind": e.kind, "title": e.title, "ref": e.ref} for e in evidence],
        warnings=warnings,
    )
    unverified = sum(1 for r in ordered for c in r.citations if not c.verified)
    if unverified:
        a.warnings.append(f"{unverified} AI citation(s) could not be matched to the evidence text and are marked unverified.")

    # 4. Summarise
    if any_ai and assessor:
        try:
            findings = [{
                "control_id": r.control_id, "title": r.title, "status": r.status, "score": round(r.score * 100),
                "priority": r.priority, "legally_binding": r.legally_binding, "frameworks": r.frameworks,
                "gaps": r.gaps, "recommendations": [x.action for x in r.recommendations],
            } for r in scored]
            scores = {
                "overall": overall, "maturity": a.maturity, "domains": domains,
                "frameworks": {f.name: f.score for f in fw_scores if f.applicable},
            }
            s = assessor.summarise(findings, scores)
            a.executive_summary, a.roadmap = s["executive_summary"], s["roadmap"]
        except Exception as e:
            a.warnings.append(f"AI summary failed ({e}); generated summary used instead.")
    if not a.executive_summary:
        a.executive_summary, a.roadmap = _rules_summary(a), _rules_roadmap(a.gaps())
    return a
