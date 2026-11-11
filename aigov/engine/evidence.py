"""Deterministic evidence checks (no network, no model).

For each best-practice control the checker looks for:
  * documents   - phrase-group coverage inside one document (the anchor group must match)
  * signals     - facts found by connectors (repository scan, inventory)
  * caveats     - sentences saying the control is planned, absent or excludes AI

Keyword coverage shows a topic is *addressed*, not that a control is *effective*;
the test engine therefore treats evidence as corroboration and leaves the verdict to answers.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..models import Control, Evidence

CAVEAT = re.compile(
    r"\b(not yet|will be|to be (developed|defined|implemented|determined)|has not been|have not been|is not covered|"
    r"are not (yet )?covered|not currently|planned for|under development|tbd|no formal|does not (yet )?(cover|include|apply))\b",
    re.I,
)
AI_WORDS = re.compile(r"\bai\b|\bmodels?\b|machine learning|algorithm", re.I)


@dataclass
class ControlEvidence:
    control_id: str
    score: float = 0.0                  # 0..1
    doc_id: str = ""
    doc_title: str = ""
    quotes: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    caveats: list[str] = field(default_factory=list)
    signals_present: list[str] = field(default_factory=list)
    signals_missing: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def merge_signals(evidence: list[Evidence]) -> dict:
    """Boolean signals are OR-ed and numeric signals summed across all evidence."""
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


def find_caveats(phrases: list[str], text: str) -> list[str]:
    out = []
    for sent in re.split(r"(?<=[.!?])\s+|\n+", text):
        if CAVEAT.search(sent):
            low = sent.lower()
            if any(ph in low for ph in phrases) or AI_WORDS.search(sent):
                out.append(sent.strip(" #*-\t")[:240])
    return out[:2]


def best_document(groups: list[list[str]], docs: list[Evidence]):
    """Return (coverage, doc, matched group indexes, quotes) for the best single document."""
    best = (0.0, None, [], [])
    if not groups:
        return best
    for d in docs:
        low = d.text.lower()
        matched, quotes = [], []
        for i, group in enumerate(groups):
            pos = min((p for p in (low.find(ph.lower()) for ph in group) if p != -1), default=-1)
            if pos == -1:
                if i == 0:
                    break
                continue
            matched.append(i)
            q = _snippet(d.text, pos)
            if q and q not in quotes:
                quotes.append(q)
        if matched and matched[0] == 0:
            cov = len(matched) / len(groups)
            if cov > best[0]:
                best = (cov, d, matched, quotes)
    return best


def check_groups(cid: str, groups: list[list[str]], wanted_signals: list[str], evidence: list[Evidence], signals: dict) -> ControlEvidence:
    docs = [e for e in evidence if e.kind in ("document", "api")]
    cov, doc, matched, quotes = best_document(groups, docs)
    ce = ControlEvidence(control_id=cid)
    base = cov
    if doc:
        ce.doc_id, ce.doc_title, ce.quotes = doc.id, doc.title, quotes[:3]
        ce.notes.append(f"'{doc.title}' addresses {len(matched)} of {len(groups)} expected elements.")
        ce.missing = [" / ".join(g[:3]) for i, g in enumerate(groups) if i not in matched]
        ce.caveats = find_caveats([p for g in groups for p in g], doc.text)
    if wanted_signals:
        ce.signals_present = [s for s in wanted_signals if signals.get(s)]
        ce.signals_missing = [s for s in wanted_signals if not signals.get(s)]
        frac = len(ce.signals_present) / len(wanted_signals)
        base = min(1.0, cov * 0.75 + frac * 0.25) if cov else frac * 0.4
        if ce.signals_present:
            ce.notes.append("Technical signals present: " + ", ".join(ce.signals_present) + ".")
    if ce.caveats:
        base = min(base, 0.6)
        ce.notes.append("The document indicates the control is incomplete or only planned.")
    ce.score = round(base, 2)
    return ce


def control_evidence(control: Control, evidence: list[Evidence], signals: dict) -> ControlEvidence:
    ce = check_groups(control.id, control.indicators, control.signals, evidence, signals)
    if control.id == "GOV-03" and signals.get("inventory_systems"):
        ratio = signals.get("inventory_complete", 0) / signals["inventory_systems"]
        ce.score = round(max(ce.score, 0.4 + 0.5 * ratio), 2)
        ce.notes.append(f"Inventory lists {signals['inventory_systems']} system(s); {int(ratio * 100)}% have owner, purpose, role and risk tier.")
        if ratio < 1:
            ce.missing.append("owner, purpose, role or risk tier for every inventory entry")
    if control.id == "DEV-04" and signals.get("hardcoded_secrets"):
        ce.score = min(ce.score, 0.3)
        ce.caveats.append("Possible hard-coded credentials found in source code.")
    return ce
