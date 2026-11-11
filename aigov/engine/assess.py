"""The compliance test engine: scope -> test each article -> score -> prioritise -> roadmap.

Everything is computed locally from the rule library, the answers and the evidence supplied.
No network or model call is made.

Scoring of one test
    yes  + evidence (linked evidence item, or the article's evidence checks pass)  -> 1.0  verified
    yes  without evidence                                                          -> 0.6  attested
    yes  but the evidence says the control is planned / excludes AI                 -> 0.6  attested
    partial                                                                        -> 0.5
    no                                                                             -> 0.0
    na                                                                             -> excluded
    unanswered                                                                     -> evidence score x 0.8
An article's score is the mean of its tests: met >= 75, partial >= 35, gap below.
"""
from __future__ import annotations

import uuid

from .. import __version__
from ..catalog import controls_by_id, load_frameworks, load_requirements
from ..models import (Answer, Assessment, Citation, Evidence, FrameworkScore, Profile, Recommendation,
                      Requirement, RequirementResult, TestResult)
from .applicability import classify_profile, derive_flags, framework_applies, requirement_applies
from .evidence import ControlEvidence, check_groups, control_evidence, merge_signals

MET, PARTIAL = 0.75, 0.35
EVIDENCE_PASS = 0.35
ATTESTED = 0.6
UNANSWERED_FACTOR = 0.8
MATURITY = [(80, "Level 5 - Optimised"), (60, "Level 4 - Managed"), (40, "Level 3 - Defined"), (20, "Level 2 - Developing"), (0, "Level 1 - Initial")]
EFFORT_RANK = {"low": 0, "medium": 1, "high": 2}
PRIORITY_RANK = {"critical": 3, "high": 2, "medium": 1, "low": 0}


def status_for(score: float) -> str:
    return "met" if score >= MET else "partial" if score >= PARTIAL else "gap"


def priority_for(weight: int, score: float, binding: bool) -> str:
    """Severity = importance x shortfall, raised when a binding law imposes the requirement."""
    sev = weight * (1 - score) * (1.5 if binding else 1.0)
    return "critical" if sev >= 3.4 else "high" if sev >= 2.0 else "medium" if sev >= 1.0 else "low"


def _weighted(results: list[RequirementResult]) -> float | None:
    total = sum(r.weight for r in results)
    return round(100 * sum(r.weight * r.score for r in results) / total, 1) if total else None


def answer_map(answers: list[Answer], reqs: list[Requirement]) -> dict[str, Answer]:
    """Expand requirement-level answers to their tests; test-level answers win."""
    by_req = {r.id: r for r in reqs}
    out: dict[str, Answer] = {}
    for a in answers:
        r = by_req.get(a.test_id)
        if r:
            for t in r.tests:
                out.setdefault(t.id, a.model_copy(update={"test_id": t.id}))
    for a in answers:
        if a.test_id not in by_req:
            out[a.test_id] = a
    return out


def _linked_evidence(ref: str, evidence: list[Evidence]) -> Evidence | None:
    ref = ref.strip().lower()
    if not ref:
        return None
    for e in evidence:
        if ref in (e.id.lower(), e.title.lower()) or ref in e.id.lower() or (len(ref) > 3 and ref in e.title.lower()):
            return e
    return None


def requirement_evidence(r: Requirement, cev: dict[str, ControlEvidence], evidence: list[Evidence], signals: dict) -> list[ControlEvidence]:
    items = [cev[c] for c in r.controls if c in cev]
    if r.keywords:
        items.append(check_groups(r.id, [r.keywords], [], evidence, signals))
    return items


def evaluate_requirement(r: Requirement, ctl_ev: list[ControlEvidence], answers: dict[str, Answer], evidence: list[Evidence]) -> RequirementResult:
    ev_score = round(sum(c.score for c in ctl_ev) / len(ctl_ev), 2) if ctl_ev else 0.0
    caveats = [c for ce in ctl_ev for c in ce.caveats]
    tests: list[TestResult] = []
    gaps: list[str] = []
    for t in r.tests:
        a = answers.get(t.id)
        tr = TestResult(test_id=t.id, question=t.question)
        if a:
            tr.answer, tr.note, tr.evidence_ref = a.answer, a.note, a.evidence_ref
        if a is None:
            tr.score = round(ev_score * UNANSWERED_FACTOR, 2)
            tr.basis = "evidence" if ev_score > 0 else "no_evidence"
            if tr.score < MET:
                gaps.append(("Not answered; evidence is incomplete for: " if ev_score else "Not answered and no evidence found for: ") + t.question)
        elif a.answer == "na":
            tr.basis = "not_applicable"
        elif a.answer == "yes":
            linked = _linked_evidence(a.evidence_ref, evidence)
            if caveats and not linked:
                tr.score, tr.basis = ATTESTED, "attested"
                gaps.append("Answered yes, but the evidence describes this as planned or incomplete: " + t.question)
            elif linked or ev_score >= EVIDENCE_PASS:
                tr.score, tr.basis = 1.0, "verified"
            else:
                tr.score, tr.basis = ATTESTED, "attested"
                gaps.append("Answered yes without supporting evidence - attach or reference the record for: " + t.question)
        elif a.answer == "partial":
            tr.score, tr.basis = 0.5, "partial"
            gaps.append("Partly in place: " + t.question + (f" ({a.note})" if a.note else ""))
        else:
            tr.score, tr.basis = 0.0, "failed"
            gaps.append("Not in place: " + t.question + (f" ({a.note})" if a.note else ""))
        tests.append(tr)

    scored = [t for t in tests if t.score is not None]
    if not scored:
        return RequirementResult(
            id=r.id, framework=r.framework, ref=r.ref, title=r.title, chapter=r.chapter, status="not_applicable",
            tests=tests, controls=r.controls, weight=r.weight,
            rationale="All tests were declared not applicable by the entity. Keep the justification on file.",
        )
    score = round(sum(t.score for t in scored) / len(scored), 2)
    answered = sum(t.answer is not None for t in tests)
    verified = sum(t.basis == "verified" for t in tests)
    confidence = "high" if answered == len(tests) and verified == len(scored) else "medium" if answered else "low"
    notes = [f"{answered} of {len(tests)} test(s) answered, {verified} verified by evidence."]
    best = max(ctl_ev, key=lambda c: c.score, default=None)
    if best and best.score:
        notes.append("Evidence check " + f"{int(ev_score * 100)}/100" + (f": {best.notes[0]}" if best.notes else "."))
    elif ctl_ev:
        notes.append("No supporting evidence found by the evidence checks.")
    for c in caveats[:2]:
        gaps.append(f'Evidence states: "{c}"')
    cites = [Citation(source=ce.doc_id, quote=q) for ce in sorted(ctl_ev, key=lambda c: -c.score) if ce.doc_id for q in ce.quotes[:2]][:3]
    return RequirementResult(
        id=r.id, framework=r.framework, ref=r.ref, title=r.title, chapter=r.chapter, status=status_for(score), score=score,
        confidence=confidence, rationale=" ".join(notes), tests=tests, gaps=[] if score >= MET else gaps[:8],
        citations=cites, controls=r.controls, weight=r.weight,
    )


def _roadmap(gaps: list[RequirementResult], reqs: dict[str, Requirement]) -> list[dict]:
    """One action per control closes every article linked to it; custom rules without controls get their own action."""
    ctl = controls_by_id()
    actions: dict[str, dict] = {}
    for g in gaps:
        req = reqs[g.id]
        key = req.controls[0] if req.controls and not req.action else f"REQ:{g.id}"
        if key not in actions:
            if key.startswith("REQ:"):
                actions[key] = {"action": req.action or f"Implement {req.ref} {req.title}.", "owner": req.owner, "effort": "medium",
                                "control_ids": [], "closes": [], "priority": "low"}
            else:
                c = ctl[key]
                actions[key] = {"action": c.remediation.action, "owner": c.remediation.owner, "effort": c.remediation.effort,
                                "control_ids": [key], "closes": [], "priority": "low"}
        a = actions[key]
        a["closes"].append(g.id)
        if PRIORITY_RANK[g.priority or "low"] > PRIORITY_RANK[a["priority"]]:
            a["priority"] = g.priority
    phases = [("Stabilise", "0-30 days", []), ("Build", "31-90 days", []), ("Embed", "91-180 days", [])]
    for a in sorted(actions.values(), key=lambda x: (-PRIORITY_RANK[x["priority"]], -len(x["closes"]))):
        quick = EFFORT_RANK[a["effort"]] == 0
        idx = 0 if a["priority"] == "critical" or (a["priority"] == "high" and quick) else 1 if a["priority"] in ("high", "medium") else 2
        phases[idx][2].append(a)
    return [{"phase": p, "horizon": h, "actions": acts} for p, h, acts in phases if acts]


def _summary(a: Assessment) -> str:
    fws = load_frameworks()
    gaps = a.gaps()
    crit = [g for g in gaps if g.priority == "critical"]
    binding = [f for f in a.frameworks if f.applicable and f.binding and f.score is not None]
    weakest = sorted(a.domains.items(), key=lambda kv: kv[1])[:2]
    high = [s.name for s in a.profile.systems if s.assessed_risk_tier in ("high", "prohibited")]
    n = {s: sum(r.status == s for r in a.results) for s in ("met", "partial", "gap")}
    paras = [
        f"{a.profile.entity.name} scores {a.overall_score:.0f} out of 100 ({a.maturity}) across "
        f"{n['met'] + n['partial'] + n['gap']} in-scope articles and clauses: {n['met']} met, {n['partial']} partly met, "
        f"{n['gap']} gaps. {a.tests_answered} of {a.tests_total} compliance tests were answered."
    ]
    if binding:
        txt = "Binding law in scope: " + "; ".join(f"{f.name} {f.score:.0f}/100" for f in binding) + ". "
        if crit:
            txt += f"{len(crit)} critical gap(s) carry direct legal exposure, led by " + ", ".join(
                f"{fws[g.framework].name} {g.ref} ({g.title})" for g in crit[:4]) + "."
        else:
            txt += "No critical gaps were found."
        if high:
            txt += f" Systems screened as high-risk: {', '.join(high)}."
        paras.append(txt)
    if weakest:
        paras.append("Weakest areas: " + " and ".join(f"{d} ({s:.0f}/100)" for d, s in weakest) + ". "
                     "The roadmap groups fixes by control, so a single action closes every article that depends on it.")
    unanswered = a.tests_total - a.tests_answered
    if unanswered:
        paras.append(f"{unanswered} test(s) were not answered and were scored from documentary evidence alone, capped below full marks. "
                     "Answer them on the Tests page to firm up the result.")
    return "\n\n".join(paras)


def run_assessment(
    profile: Profile,
    evidence: list[Evidence],
    answers: list[Answer] | None = None,
    custom_rules: list[Requirement] | None = None,
    warnings: list[str] | None = None,
) -> Assessment:
    warnings = list(warnings or [])
    profile = profile.model_copy(deep=True)
    frameworks = load_frameworks()
    reqs = load_requirements(custom_rules)
    req_by_id = {r.id: r for r in reqs}
    amap = answer_map(answers or [], reqs)
    known = {t.id for r in reqs for t in r.tests}
    unknown = sorted(k for k in amap if k not in known)
    if unknown:
        warnings.append("Answers for unknown test ids were ignored: " + ", ".join(unknown[:15]))

    # 1. Scope
    warnings += classify_profile(profile)
    flags = derive_flags(profile)
    fw_scope = {k: framework_applies(fw, profile, flags) for k, fw in frameworks.items()}

    # 2. Evidence (computed once per control, shared by every linked article)
    signals = merge_signals(evidence)
    cev = {c.id: control_evidence(c, evidence, signals) for c in controls_by_id().values()}

    # 3. Test each article
    results: list[RequirementResult] = []
    for r in reqs:
        if r.kind == "info" or not fw_scope[r.framework][0]:
            continue
        ok, why = requirement_applies(r, flags)
        fw = frameworks[r.framework]
        binding = fw.binding if r.binding is None else r.binding
        domain = controls_by_id()[r.controls[0]].domain if r.controls else "Custom rules"
        if not ok:
            results.append(RequirementResult(
                id=r.id, framework=r.framework, ref=r.ref, title=r.title, chapter=r.chapter, domain=domain,
                status="not_applicable", rationale=why, controls=r.controls, weight=r.weight,
                tests=[TestResult(test_id=t.id, question=t.question, basis="not_applicable") for t in r.tests],
            ))
            continue
        res = evaluate_requirement(r, requirement_evidence(r, cev, evidence, signals), amap, evidence)
        res.domain = domain
        res.legally_binding = binding and res.status != "not_applicable"
        if res.status in ("gap", "partial"):
            res.priority = priority_for(r.weight, res.score, binding)  # type: ignore[assignment]
            if r.action:
                res.recommendations.append(Recommendation(action=r.action, priority=res.priority, owner=r.owner))
            for cid in r.controls[:2]:
                c = controls_by_id()[cid]
                if cev[cid].score < MET or not r.action:
                    res.recommendations.append(Recommendation(
                        action=c.remediation.action, priority=res.priority, effort=c.remediation.effort,
                        owner=c.remediation.owner, control_id=cid))
            if not res.recommendations:
                res.recommendations.append(Recommendation(action=f"Implement and evidence {r.ref} {r.title}.", priority=res.priority))
        results.append(res)

    # 4. Scores
    scored = [r for r in results if r.status != "not_applicable"]
    fw_scores = []
    for k, fw in frameworks.items():
        ok, reason = fw_scope[k]
        mine = [r for r in scored if r.framework == k]
        lib = [r for r in reqs if r.framework == k]
        if k == "custom" and not lib:
            continue
        fw_scores.append(FrameworkScore(
            key=k, name=fw.name, citation=fw.citation, binding=fw.binding, applicable=ok, reason=reason, note=fw.note,
            score=_weighted(mine) if ok else None, articles_total=len(lib),
            articles_assessable=sum(x.kind != "info" for x in lib), in_scope=len(mine),
            met=sum(r.status == "met" for r in mine), partial=sum(r.status == "partial" for r in mine),
            gap=sum(r.status == "gap" for r in mine),
        ))
    domains: dict[str, float] = {}
    for d in dict.fromkeys(r.domain for r in scored):
        s = _weighted([r for r in scored if r.domain == d])
        if s is not None:
            domains[d] = s
    overall = _weighted(scored) or 0.0
    in_scope_tests = [t for r in scored for t in r.tests]

    a = Assessment(
        id=uuid.uuid4().hex[:12], tool_version=__version__, profile=profile, flags=sorted(flags),
        overall_score=overall, maturity=next(label for floor, label in MATURITY if overall >= floor),
        frameworks=fw_scores, domains=dict(sorted(domains.items())), results=results,
        tests_total=len(in_scope_tests), tests_answered=sum(t.answer is not None for t in in_scope_tests),
        evidence_index=[{"id": e.id, "connector": e.connector, "kind": e.kind, "title": e.title, "ref": e.ref} for e in evidence],
        warnings=warnings,
    )
    if not scored:
        a.warnings.append("No article is in scope: add jurisdictions and AI systems to the profile.")
    a.roadmap = _roadmap(a.gaps(), req_by_id)
    a.executive_summary = _summary(a)
    return a
