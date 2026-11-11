"""Report renderers: JSON, CSV (one row per test), Markdown and a self-contained HTML report.
The HTML report loads nothing from the network."""
from __future__ import annotations

import csv
import io
from html import escape as h

from ..catalog import load_frameworks
from ..models import Assessment, RequirementResult

DISCLAIMER = (
    "This report is a governance diagnostic produced by rule-based tests, not legal advice or a certification. "
    "Article summaries are paraphrased; confirm applicability, current wording and effective dates against the "
    "official texts and with qualified counsel before relying on a finding."
)
STATUS_LABEL = {"met": "Met", "partial": "Partial", "gap": "Gap", "not_applicable": "N/A"}
BASIS_LABEL = {"verified": "Yes - evidenced", "attested": "Yes - no evidence", "partial": "Partial", "failed": "No",
               "not_applicable": "N/A", "evidence": "Unanswered - from evidence", "no_evidence": "Unanswered"}


def fw_name(key: str) -> str:
    fws = load_frameworks()
    return fws[key].name if key in fws else key


def to_json(a: Assessment) -> str:
    return a.model_dump_json(indent=2)


def to_csv(a: Assessment) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["framework", "article", "title", "article_status", "article_score", "priority", "legally_binding",
                "test_id", "test", "answer", "test_score", "basis", "note", "evidence_ref", "recommendation"])
    for r in a.results:
        rec = r.recommendations[0].action if r.recommendations else ""
        for t in r.tests or [None]:
            w.writerow([fw_name(r.framework), r.ref, r.title, r.status, round(r.score * 100), r.priority or "", r.legally_binding,
                        t.test_id if t else "", t.question if t else "", (t.answer or "") if t else "",
                        "" if not t or t.score is None else round(t.score * 100), BASIS_LABEL[t.basis] if t else "",
                        t.note if t else "", t.evidence_ref if t else "", rec])
    return buf.getvalue()


def to_markdown(a: Assessment) -> str:
    e = a.profile.entity
    out = [
        f"# AI Governance & Compliance Assessment: {e.name}", "",
        f"- **Date:** {a.created_at}", f"- **Method:** rule-based compliance tests (offline)",
        f"- **Jurisdictions:** {', '.join(e.jurisdictions) or 'not stated'}",
        f"- **Overall score:** {a.overall_score:.0f}/100 ({a.maturity})",
        f"- **Tests answered:** {a.tests_answered} of {a.tests_total}", "",
        "## Executive summary", "", a.executive_summary, "",
        "## Laws and frameworks", "",
        "| Framework | Type | Articles in library | In scope | Score | Met | Partial | Gap |", "|---|---|---|---|---|---|---|---|",
    ]
    for f in a.frameworks:
        lib = f"{f.articles_total} ({f.articles_assessable} with obligations)"
        if f.applicable and f.score is not None:
            out.append(f"| {f.name} | {'Binding law' if f.binding else 'Voluntary'} | {lib} | {f.in_scope} | {f.score:.0f} | {f.met} | {f.partial} | {f.gap} |")
        else:
            out.append(f"| {f.name} | {'Binding law' if f.binding else 'Voluntary'} | {lib} | No: {f.reason} | - | - | - | - |")
    out += ["", "## AI systems", "", "| System | Role | Risk tier | Basis |", "|---|---|---|---|"]
    out += [f"| {s.name} | {s.role} | {s.assessed_risk_tier} | {s.risk_rationale} |" for s in a.profile.systems]
    out += ["", "## Domain scores", ""] + [f"- {d}: {s:.0f}/100" for d, s in a.domains.items()]
    out += ["", "## Gaps by article", ""]
    for r in a.gaps():
        out += [f"### {fw_name(r.framework)} {r.ref} - {r.title}", "",
                f"{STATUS_LABEL[r.status]}, {r.priority} priority, score {r.score * 100:.0f}" + (" - binding law" if r.legally_binding else ""), "",
                r.rationale, ""]
        out += [f"- Gap: {g}" for g in r.gaps]
        out += [f"- **Do:** {x.action} *(owner: {x.owner or 'unassigned'}; effort: {x.effort})*" for x in r.recommendations]
        out += [f"- Evidence [{c.source}]: \"{c.quote}\"" for c in r.citations]
        out.append("")
    out += ["## Roadmap", ""]
    for p in a.roadmap:
        out.append(f"### {p['phase']} ({p['horizon']})")
        out += [f"- [{x['priority']}] {x['action']} *(owner: {x['owner'] or 'unassigned'}; closes {len(x['closes'])} article(s): {', '.join(x['closes'][:12])})*" for x in p["actions"]]
        out.append("")
    met = [r for r in a.results if r.status == "met"]
    if met:
        out += ["## Articles met", ""] + [f"- {fw_name(r.framework)} {r.ref} {r.title}" for r in met] + [""]
    if a.warnings:
        out += ["## Notes", ""] + [f"- {w}" for w in a.warnings] + [""]
    out += ["---", DISCLAIMER, ""]
    return "\n".join(out)


CSS = """
:root{--bg:#f5f6f8;--card:#fff;--ink:#18202e;--mute:#5a6474;--line:#e1e5eb;--accent:#2d5bd7;
--met:#1d7f47;--partial:#a86a0c;--gap:#c0322f;--na:#7f8898;--critical:#9b1c1c;--high:#c2410c;--medium:#93630a;--low:#47607a}
@media(prefers-color-scheme:dark){:root{--bg:#0f131a;--card:#171d28;--ink:#e5e9f1;--mute:#98a3b6;--line:#283142;--accent:#7da2ff;
--met:#4ade80;--partial:#fbbf24;--gap:#f87171;--na:#7c8799;--critical:#fca5a5;--high:#fdba74;--medium:#fde047;--low:#a5b4c8}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1080px;margin:0 auto;padding:28px 16px 60px}h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:34px 0 12px}h3{font-size:15px;margin:0}
.mute{color:var(--mute)}.small{font-size:13px}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-bottom:12px}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}.hero{display:grid;gap:12px;grid-template-columns:minmax(200px,260px) 1fr}
@media(max-width:700px){.hero{grid-template-columns:1fr}}.big{font-size:54px;font-weight:700;line-height:1}
.bar{height:8px;border-radius:4px;background:var(--line);overflow:hidden;margin-top:8px}.bar>i{display:block;height:100%;background:var(--accent)}
.pill{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;font-weight:600;border:1px solid currentColor;white-space:nowrap}
.met{color:var(--met)}.partial{color:var(--partial)}.gap{color:var(--gap)}.not_applicable{color:var(--na)}
.critical{color:var(--critical)}.high{color:var(--high)}.medium{color:var(--medium)}.low{color:var(--low)}
.wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute)}
details{background:var(--card);border:1px solid var(--line);border-radius:10px;margin-bottom:8px}
summary{cursor:pointer;padding:12px 16px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}summary b{flex:1;min-width:200px}
.body{padding:0 16px 14px;border-top:1px solid var(--line)}.body p{margin:10px 0}ul{margin:6px 0;padding-left:20px}
blockquote{margin:6px 0;padding:4px 10px;border-left:3px solid var(--line);color:var(--mute);font-size:13px}
.rec{border-left:3px solid var(--accent);padding:4px 10px;margin:6px 0}.note{border-left:3px solid var(--partial)}
p.sum{margin:0 0 10px}footer{margin-top:40px;font-size:12px;color:var(--mute)}
"""


def _pill(cls: str, text: str) -> str:
    return f'<span class="pill {h(cls)}">{h(text)}</span>'


def _article(r: RequirementResult, open_: bool = False) -> str:
    parts = [f"<p>{h(r.rationale)}</p>"]
    if r.tests:
        rows = "".join(
            f"<tr><td>{h(t.question)}</td><td>{h(BASIS_LABEL[t.basis])}</td><td>{'' if t.score is None else f'{t.score * 100:.0f}'}</td>"
            f"<td class='small'>{h(t.note)}{(' · ' + h(t.evidence_ref)) if t.evidence_ref else ''}</td></tr>" for t in r.tests)
        parts.append(f'<div class="wrap"><table><tr><th>Test</th><th>Result</th><th>Score</th><th>Note / evidence</th></tr>{rows}</table></div>')
    if r.gaps:
        parts.append("<ul>" + "".join(f"<li>{h(g)}</li>" for g in r.gaps) + "</ul>")
    for x in r.recommendations:
        parts.append(f'<div class="rec"><b>Recommended:</b> {h(x.action)}<br><span class="small mute">Owner: {h(x.owner or "unassigned")} · Effort: {h(x.effort)} · Priority: {h(x.priority)}{" · Control " + h(x.control_id) if x.control_id else ""}</span></div>')
    for c in r.citations:
        parts.append(f"<blockquote>“{h(c.quote)}”<br>— {h(c.source)}</blockquote>")
    meta = f'<span class="small mute">{r.score * 100:.0f}/100 · confidence {h(r.confidence)}</span>' if r.status != "not_applicable" else ""
    prio = _pill(r.priority, r.priority) if r.priority else ""
    law = _pill("gap", "binding law") if r.legally_binding and r.status in ("gap", "partial") else ""
    return (f'<details{" open" if open_ else ""}><summary>{_pill(r.status, STATUS_LABEL[r.status])}'
            f'<b>{h(fw_name(r.framework))} · {h(r.ref)} · {h(r.title)}</b>{prio}{law}{meta}</summary><div class="body">{"".join(parts)}</div></details>')


def to_html(a: Assessment) -> str:
    e = a.profile.entity
    counts = {s: sum(r.status == s for r in a.results) for s in STATUS_LABEL}
    gaps = a.gaps()
    crit = sum(g.priority == "critical" for g in gaps)
    fw_rows = ""
    for f in a.frameworks:
        kind = _pill("gap" if f.binding else "low", "Binding law" if f.binding else "Voluntary")
        lib = f'<div class="small mute">{f.articles_total} articles in library · {f.articles_assessable} with obligations</div>'
        if f.applicable and f.score is not None:
            cells = (f'<td><b>{f.score:.0f}</b><div class="bar"><i style="width:{f.score:.0f}%"></i></div></td>'
                     f"<td>{f.in_scope}</td><td>{f.met}</td><td>{f.partial}</td><td>{f.gap}</td>")
        else:
            cells = f'<td colspan="5" class="mute small">Not in scope: {h(f.reason)}</td>'
        note = f'<div class="small mute">{h(f.note)}</div>' if f.note and f.applicable else ""
        fw_rows += f'<tr><td><b>{h(f.name)}</b><div class="small mute">{h(f.citation)}</div>{lib}{note}</td><td>{kind}</td>{cells}</tr>'
    tier_cls = {"prohibited": "critical", "high": "high", "limited": "medium", "minimal": "low"}
    sys_rows = "".join(
        f"<tr><td><b>{h(s.name)}</b><div class='small mute'>{h(s.purpose or s.description)}</div></td><td>{h(s.role)}</td>"
        f"<td>{_pill(tier_cls.get(s.assessed_risk_tier or 'minimal', 'low'), s.assessed_risk_tier or '')}</td><td class='small'>{h(s.risk_rationale)}</td></tr>"
        for s in a.profile.systems) or '<tr><td colspan="4" class="mute">No AI systems declared.</td></tr>'
    domains = "".join(f'<div class="card"><h3>{h(d)}</h3><div class="small mute">{s:.0f}/100</div><div class="bar"><i style="width:{s:.0f}%"></i></div></div>' for d, s in a.domains.items())
    roadmap = "".join(
        f'<div class="card"><h3>{h(p["phase"])}</h3><div class="small mute">{h(p["horizon"])}</div><ul>'
        + "".join(f'<li>{_pill(x["priority"], x["priority"])} {h(x["action"])}<div class="small mute">Owner: {h(x["owner"] or "unassigned")} · closes {len(x["closes"])} article(s)</div></li>' for x in p["actions"])
        + "</ul></div>" for p in a.roadmap)
    summary = "".join(f'<p class="sum">{h(p)}</p>' for p in a.executive_summary.split("\n\n"))
    met = [r for r in a.results if r.status == "met"]
    na = [r for r in a.results if r.status == "not_applicable"]
    warnings = "".join(f'<div class="card note small">{h(w)}</div>' for w in a.warnings)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Compliance Report - {h(e.name)}</title><style>{CSS}</style></head><body><main>
<h1>AI Governance &amp; Compliance Report</h1>
<div class="mute">{h(e.name)}{' · ' + h(e.sector) if e.sector else ''} · {h(', '.join(e.jurisdictions))} · {h(a.created_at)} · Rule-based compliance tests</div>
<h2>Position</h2><div class="hero">
 <div class="card"><div class="small mute">Overall score</div><div class="big">{a.overall_score:.0f}</div><div class="small mute">out of 100 · {h(a.maturity)}</div>
 <div class="bar"><i style="width:{a.overall_score:.0f}%"></i></div>
 <p class="small">{_pill('met', f"{counts['met']} met")} {_pill('partial', f"{counts['partial']} partial")} {_pill('gap', f"{counts['gap']} gap")}<br>
 <span class="mute">{counts['met'] + counts['partial'] + counts['gap']} articles in scope · {crit} critical · {a.tests_answered}/{a.tests_total} tests answered</span></p></div>
 <div class="card">{summary}</div></div>
<h2>Laws and frameworks</h2>
<div class="card wrap"><table><tr><th>Framework</th><th>Type</th><th>Score</th><th>In scope</th><th>Met</th><th>Partial</th><th>Gap</th></tr>{fw_rows}</table></div>
<h2>AI systems and risk tiers</h2>
<div class="card wrap"><table><tr><th>System</th><th>Role</th><th>Risk tier</th><th>Basis</th></tr>{sys_rows}</table></div>
<h2>Domains</h2><div class="grid">{domains}</div>
<h2>Roadmap</h2><div class="grid">{roadmap or '<div class="card">Nothing to remediate.</div>'}</div>
<h2>Gaps by article ({len(gaps)})</h2>
{''.join(_article(r, i < 3) for i, r in enumerate(gaps)) or '<div class="card">No gaps identified.</div>'}
<h2>Articles met ({len(met)})</h2>{''.join(_article(r) for r in met) or '<div class="card mute">None yet.</div>'}
<h2>In-scope frameworks, articles not applicable ({len(na)})</h2>{''.join(_article(r) for r in na)}
{'<h2>Notes</h2>' + warnings if warnings else ''}
<footer>{h(DISCLAIMER)}<br>Evidence items reviewed: {len(a.evidence_index)} · Assessment {h(a.id)} · aigov {h(a.tool_version)}</footer>
</main></body></html>"""


RENDERERS = {"json": to_json, "md": to_markdown, "html": to_html, "csv": to_csv}
