"""Deterministic evaluator: works offline, with no model call.

It combines three kinds of evidence for each control:
  * documents   - phrase-group coverage inside a single document (anchor group must match)
  * signals     - facts detected by connectors (repo scan, registries, inventory)
  * attestation - management's questionnaire answer

Keyword coverage shows that a topic is *addressed*, not that the control is *effective*,
so results carry low confidence and an uncorroborated "yes" is capped at partial.
"""
from __future__ import annotations

import re

from ..models import Attestation, Citation, Control, ControlResult, Evidence, Recommendation

MET, PARTIAL = 0.75, 0.35
CAVEAT_CAP = 0.6
# Wording that signals intent or absence rather than an operating control.
CAVEAT = re.compile(
    r"\b(not yet|will be|to be (developed|defined|implemented|determined)|has not been|have not been|is not covered|"
    r"are not (yet )?covered|not currently|planned for|under development|tbd|no formal|does not (yet )?(cover|include|apply))\b", re.I)
AI_WORDS = re.compile(r"\bai\b|\bmodels?\b|machine learning|algorithm", re.I)


def find_caveats(control: Control, text: str) -> list[str]:
    """Sentences in a matched document saying the control (or its AI coverage) is absent or only planned."""
    phrases = [ph for g in control.indicators for ph in g]
    out = []
    for sent in re.split(r"(?<=[.!?])\s+|\n+", text):
        if CAVEAT.search(sent):
            low = sent.lower()
            if any(ph in low for ph in phrases) or AI_WORDS.search(sent):
                out.append(sent.strip(" #*-\t")[:240])
    return out[:2]


def status_for(score: float) -> str:
    return "met" if score >= MET else "partial" if score >= PARTIAL else "gap"


def merge_signals(evidence: list[Evidence]) -> dict:
    """Boolean signals are OR-ed, numeric signals summed, across all evidence."""
    out: dict = {}
    for e in evidence:
        for k, v in e.signals.items():
            if isinstance(v, bool):
                out[k] = out.get(k, False) or v
            elif isinstance(v, (int, float)):
                out[k] = out.get(k, 0) + v
    return out


def _snippet(text: str, pos: int) -> str:
    start = max(text.rfind("\n", 0, pos), text.rfind(". ", 0, pos)) + 1
    ends = [i for i in (text.find("\n", pos), text.find(". ", pos)) if i != -1]
    end = min(ends) if ends else len(text)
    return text[start:end].strip(" #*-\t")[:240]


def _doc_match(control: Control, docs: list[Evidence]) -> tuple[float, Evidence | None, list[int], list[str]]:
    """Best single-document coverage. Returns (coverage, doc, matched group indexes, quotes)."""
    best: tuple[float, Evidence | None, list[int], list[str]] = (0.0, None, [], [])
    if not control.indicators:
        return best
    for d in docs:
        low = d.text.lower()
        matched, quotes = [], []
        for i, group in enumerate(control.indicators):
            pos = min((p for p in (low.find(ph) for ph in group) if p != -1), default=-1)
            if pos == -1:
                if i == 0:
                    break  # anchor missing: this document is not about the control
                continue
            matched.append(i)
            q = _snippet(d.text, pos)
            if q and q not in quotes:
                quotes.append(q)
        if matched and matched[0] == 0:
            cov = len(matched) / len(control.indicators)
            if cov > best[0]:
                best = (cov, d, matched, quotes)
    return best


def evaluate_control(control: Control, evidence: list[Evidence], signals: dict, att: Attestation | None) -> ControlResult:
    docs = [e for e in evidence if e.kind in ("document", "api")]
    cov, doc, matched, quotes = _doc_match(control, docs)
    gaps: list[str] = []
    notes: list[str] = []

    base = cov
    if doc:
        notes.append(f"'{doc.title}' addresses {len(matched)} of {len(control.indicators)} expected elements.")
        for i, group in enumerate(control.indicators):
            if i not in matched:
                gaps.append("No evidence of: " + " / ".join(group[:3]))
        caveats = find_caveats(control, doc.text)
        if caveats:
            base = min(base, CAVEAT_CAP)
            notes.append("The document itself indicates the control is incomplete or only planned.")
            gaps += [f'Stated as absent or planned: "{c}"' for c in caveats]
    else:
        gaps.append("No document found that addresses this control.")

    if control.signals:
        present = [s for s in control.signals if signals.get(s)]
        frac = len(present) / len(control.signals)
        base = min(base if cov else 1.0, cov * 0.75 + frac * 0.25) if cov else frac * 0.4
        if present:
            notes.append("Technical signals present: " + ", ".join(present) + ".")
        missing = [s for s in control.signals if s not in present]
        if missing:
            gaps.append("Technical signals not detected: " + ", ".join(missing))

    # A populated inventory is direct evidence for the inventory control.
    if control.id == "GOV-03" and signals.get("inventory_systems"):
        ratio = signals.get("inventory_complete", 0) / signals["inventory_systems"]
        base = max(base, 0.4 + 0.5 * ratio)
        notes.append(f"Inventory lists {signals['inventory_systems']} system(s); {int(ratio * 100)}% have owner, purpose, role and risk tier.")
        if ratio < 1:
            gaps.append("Some inventory entries lack owner, purpose, role or risk tier.")
    if control.id == "DEV-04" and signals.get("hardcoded_secrets"):
        base = min(base, 0.3)
        gaps.append("Possible hard-coded credentials found in source code.")

    confidence = "low"
    score = base
    if att:
        if att.answer == "na":
            return ControlResult(
                control_id=control.id, domain=control.domain, title=control.title, status="not_applicable",
                rationale="Declared not applicable by management" + (f": {att.notes}" if att.notes else "") + ". Confirm the scoping decision.",
                weight=control.weight,
            )
        if att.answer == "yes":
            if base > 0:
                capped = doc is not None and base <= CAVEAT_CAP and bool(find_caveats(control, doc.text))
                score, confidence = (min(base + 0.1, 0.7) if capped else min(1.0, max(base, 0.5) + 0.15)), "medium"
                notes.append("Management attests the control is in place, and evidence corroborates it.")
            else:
                score = 0.5
                notes.append("Management attests the control is in place, but no corroborating evidence was found.")
                gaps.insert(0, "Attested but unverified: provide the document or record that demonstrates this control.")
        elif att.answer == "partial":
            score = min(0.7, max(base, 0.35))
            notes.append("Management reports the control is partly in place.")
        else:  # "no"
            score = min(base, 0.3)
            notes.append("Management reports the control is not in place.")
            if base > 0.3:
                notes.append("Documents mention the topic, so they may be drafts or not operational.")
        if att.notes:
            notes.append(f"Management note: {att.notes}")

    status = status_for(score)
    if status == "met":
        gaps = []
    recs = [] if status == "met" else [Recommendation(
        action=control.remediation.action, effort=control.remediation.effort, owner=control.remediation.owner,
    )]
    return ControlResult(
        control_id=control.id, domain=control.domain, title=control.title, status=status, score=round(score, 2),
        confidence=confidence, method="rules", rationale=" ".join(notes) or "No evidence found.",
        gaps=gaps[:6], citations=[Citation(source=doc.id, quote=q) for q in quotes[:3]] if doc else [],
        recommendations=recs, weight=control.weight,
    )


def normalise(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()
