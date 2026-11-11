"""Report renderers: JSON (machine), Markdown (tickets, wikis), HTML (self-contained dashboard)."""
from __future__ import annotations

from html import escape as h

from ..catalog import load_frameworks
from ..models import Assessment, ControlResult

DISCLAIMER = (
    "This report is a governance diagnostic, not legal advice or a certification. Framework references are mapped at "
    "clause level to help you find the source text; confirm applicability, current wording and effective dates with "
    "qualified counsel before relying on them."
)
STATUS_LABEL = {"met": "Met", "partial": "Partial", "gap": "Gap", "not_applicable": "N/A"}


def to_json(a: Assessment) -> str:
    return a.model_dump_json(indent=2)


def _refs(r: ControlResult) -> str:
    names = load_frameworks()
    return "; ".join(f"{names[k].name}: {', '.join(v)}" for k, v in r.frameworks.items())


# --------------------------------------------------------------------------- markdown
def to_markdown(a: Assessment) -> str:
    e = a.profile.entity
    out = [
        f"# AI Governance & Compliance Assessment: {e.name}",
        "",
        f"- **Date:** {a.created_at}",
        f"- **Assessment method:** {'AI-assisted (' + a.model + ')' if a.mode == 'ai' else 'Rule-based (offline)'}",
        f"- **Jurisdictions:** {', '.join(e.jurisdictions) or 'not stated'}",
        f"- **Overall score:** {a.overall_score:.0f}/100 ({a.maturity})",
        "",
        "## Executive summary",
        "",
        a.executive_summary,
        "",
        "## Frameworks",
        "",
        "| Framework | Type | In scope | Score | Met | Partial | Gap |",
        "|---|---|---|---|---|---|---|",
    ]
    for f in a.frameworks:
        out.append(
            f"| {f.name} ({f.citation}) | {'Binding law' if f.binding else 'Voluntary'} | "
            + (f"Yes | {f.score:.0f} | {f.controls_met} | {f.controls_partial} | {f.controls_gap} |" if f.applicable and f.score is not None
               else f"No: {f.reason} | - | - | - | - |")
        )
    out += ["", "## AI systems", "", "| System | Role | Risk tier | Basis |", "|---|---|---|---|"]
    for s in a.profile.systems:
        out.append(f"| {s.name} | {s.role} | {s.assessed_risk_tier} | {s.risk_rationale} |")
    out += ["", "## Domain scores", ""]
    out += [f"- {d}: {s:.0f}/100" for d, s in a.domains.items()]

    out += ["", "## Gaps and recommendations", ""]
    for r in a.gaps():
        out += [
            f"### {r.control_id} {r.title} ({STATUS_LABEL[r.status]}, {r.priority} priority, score {r.score * 100:.0f})",
            "",
            r.rationale,
            "",
            f"*Requirements:* {_refs(r)}",
            "",
        ]
        out += [f"- Gap: {g}" for g in r.gaps]
        out += [f"- **Do:** {x.action} *(owner: {x.owner or 'unassigned'}; effort: {x.effort})*" for x in r.recommendations]
        out += [f"- Evidence [{c.source}]{'' if c.verified else ' (unverified quote)'}: \"{c.quote}\"" for c in r.citations]
        out.append("")

    out += ["## Roadmap", ""]
    for p in a.roadmap:
        out.append(f"### {p['phase']} ({p['horizon']})")
        out += [f"- {x['action']} *(owner: {x['owner']}; closes {', '.join(x['control_ids'])})*" for x in p["actions"]]
        out.append("")

    met = [r for r in a.results if r.status == "met"]
    if met:
        out += ["## Controls met", ""] + [f"- {r.control_id} {r.title}" for r in met] + [""]
    if a.warnings:
        out += ["## Notes and limitations", ""] + [f"- {w}" for w in a.warnings] + [""]
    out += ["---", DISCLAIMER, ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- html
CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#1a2233;--mute:#5b6577;--line:#e2e6ec;--accent:#2f5bd8;
--met:#1f8a4c;--partial:#b7791f;--gap:#c53030;--na:#8a93a3;--critical:#9b1c1c;--high:#c2410c;--medium:#a16207;--low:#47607a}
@media(prefers-color-scheme:dark){:root{--bg:#10141c;--card:#181e2a;--ink:#e6eaf2;--mute:#9aa5b8;--line:#2a3344;--accent:#7da2ff;
--met:#4ade80;--partial:#fbbf24;--gap:#f87171;--na:#7c8799;--critical:#fca5a5;--high:#fdba74;--medium:#fde047;--low:#a5b4c8}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1080px;margin:0 auto;padding:28px 16px 60px}h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:36px 0 12px}
h3{font-size:15px;margin:0}.mute{color:var(--mute)}.small{font-size:13px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-bottom:12px}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.hero{display:grid;gap:12px;grid-template-columns:minmax(200px,260px) 1fr}@media(max-width:700px){.hero{grid-template-columns:1fr}}
.big{font-size:54px;font-weight:700;line-height:1}.bar{height:8px;border-radius:4px;background:var(--line);overflow:hidden;margin-top:8px}
.bar>i{display:block;height:100%;background:var(--accent)}
.pill{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;font-weight:600;border:1px solid currentColor;white-space:nowrap}
.met{color:var(--met)}.partial{color:var(--partial)}.gap{color:var(--gap)}.not_applicable{color:var(--na)}
.critical{color:var(--critical)}.high{color:var(--high)}.medium{color:var(--medium)}.low{color:var(--low)}
.wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute)}
details{background:var(--card);border:1px solid var(--line);border-radius:10px;margin-bottom:8px}
summary{cursor:pointer;padding:12px 16px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}summary b{flex:1;min-width:180px}
.body{padding:0 16px 14px;border-top:1px solid var(--line)}.body p{margin:10px 0}ul{margin:6px 0;padding-left:20px}
blockquote{margin:6px 0;padding:4px 10px;border-left:3px solid var(--line);color:var(--mute);font-size:13px}
.rec{border-left:3px solid var(--accent);padding:4px 10px;margin:6px 0}.note{border-left:3px solid var(--partial)}
p.sum{margin:0 0 10px}footer{margin-top:40px;font-size:12px;color:var(--mute)}
"""


def _pill(cls: str, text: str) -> str:
    return f'<span class="pill {cls}">{h(text)}</span>'


def _control(r: ControlResult, open_: bool = False) -> str:
    parts = [f"<p>{h(r.rationale)}</p>", f'<p class="small mute"><b>Requirements:</b> {h(_refs(r)) or "none in scope"}</p>']
    if r.gaps:
        parts.append("<ul>" + "".join(f"<li>{h(g)}</li>" for g in r.gaps) + "</ul>")
    for x in r.recommendations:
        parts.append(
            f'<div class="rec"><b>Recommended:</b> {h(x.action)}<br><span class="small mute">Owner: {h(x.owner or "unassigned")}'
            f" · Effort: {h(x.effort)} · Priority: {h(x.priority)}</span></div>"
        )
    for c in r.citations:
        tag = "" if c.verified else " (unverified quote)"
        parts.append(f"<blockquote>“{h(c.quote)}”<br>— {h(c.source)}{tag}</blockquote>")
    meta = f'<span class="small mute">{r.score * 100:.0f}/100 · {h(r.method)} · confidence {h(r.confidence)}</span>' if r.status != "not_applicable" else ""
    prio = _pill(r.priority, r.priority) if r.priority else ""
    law = _pill("gap", "binding law") if r.legally_binding and r.status in ("gap", "partial") else ""
    return (
        f'<details{" open" if open_ else ""}><summary>{_pill(r.status, STATUS_LABEL[r.status])}<b>{h(r.control_id)} · {h(r.title)}</b>'
        f'{prio}{law}{meta}</summary><div class="body">{"".join(parts)}</div></details>'
    )


def to_html(a: Assessment) -> str:
    e = a.profile.entity
    scored = [r for r in a.results if r.status != "not_applicable"]
    counts = {s: sum(r.status == s for r in a.results) for s in STATUS_LABEL}
    gaps = a.gaps()
    crit = sum(g.priority == "critical" for g in gaps)

    fw_rows = ""
    for f in a.frameworks:
        kind = _pill("gap" if f.binding else "low", "Binding law" if f.binding else "Voluntary")
        if f.applicable and f.score is not None:
            cells = (f'<td><b>{f.score:.0f}</b><div class="bar"><i style="width:{f.score:.0f}%"></i></div></td>'
                     f"<td>{f.controls_met}</td><td>{f.controls_partial}</td><td>{f.controls_gap}</td>")
        else:
            cells = f'<td colspan="4" class="mute small">Not in scope: {h(f.reason)}</td>'
        note = f'<div class="small mute">{h(f.note)}</div>' if f.note and f.applicable else ""
        fw_rows += f'<tr><td><b>{h(f.name)}</b><div class="small mute">{h(f.citation)}</div>{note}</td><td>{kind}</td>{cells}</tr>'

    sys_rows = "".join(
        f"<tr><td><b>{h(s.name)}</b><div class='small mute'>{h(s.purpose or s.description)}</div></td><td>{h(s.role)}</td>"
        f"<td>{_pill({'prohibited': 'critical', 'high': 'high', 'limited': 'medium', 'minimal': 'low'}[s.assessed_risk_tier or 'minimal'], s.assessed_risk_tier or '')}</td>"
        f"<td class='small'>{h(s.risk_rationale)}</td></tr>" for s in a.profile.systems
    ) or '<tr><td colspan="4" class="mute">No AI systems declared.</td></tr>'

    domains = "".join(
        f'<div class="card"><h3>{h(d)}</h3><div class="small mute">{s:.0f}/100</div><div class="bar"><i style="width:{s:.0f}%"></i></div></div>'
        for d, s in a.domains.items()
    )
    roadmap = "".join(
        f'<div class="card"><h3>{h(p["phase"])}</h3><div class="small mute">{h(p["horizon"])}</div><ul>'
        + "".join(f'<li>{h(x["action"])}<div class="small mute">Owner: {h(x["owner"])} · Closes {h(", ".join(x["control_ids"]))}</div></li>' for x in p["actions"])
        + "</ul></div>" for p in a.roadmap
    )
    warnings = "".join(f'<div class="card note small">{h(w)}</div>' for w in a.warnings)
    method = f"AI-assisted review ({h(a.model)})" if a.mode == "ai" else "Rule-based review (offline)"
    summary = "".join(f'<p class="sum">{h(p)}</p>' for p in a.executive_summary.split("\n\n"))
    others = [r for r in a.results if r.status in ("met", "not_applicable")]

    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Governance Assessment - {h(e.name)}</title><style>{CSS}</style></head><body><main>
<h1>AI Governance &amp; Compliance Assessment</h1>
<div class="mute">{h(e.name)}{' · ' + h(e.sector) if e.sector else ''} · {h(', '.join(e.jurisdictions))} · {h(a.created_at)} · {method}</div>

<h2>Position</h2>
<div class="hero">
 <div class="card"><div class="small mute">Overall score</div><div class="big">{a.overall_score:.0f}</div><div class="small mute">out of 100 · {h(a.maturity)}</div>
  <div class="bar"><i style="width:{a.overall_score:.0f}%"></i></div>
  <p class="small">{_pill('met', f"{counts['met']} met")} {_pill('partial', f"{counts['partial']} partial")} {_pill('gap', f"{counts['gap']} gap")}<br>
  <span class="mute">{len(scored)} controls in scope · {counts['not_applicable']} not applicable · {crit} critical</span></p></div>
 <div class="card">{summary}</div>
</div>

<h2>Laws and frameworks</h2>
<div class="card wrap"><table><tr><th>Framework</th><th>Type</th><th>Score</th><th>Met</th><th>Partial</th><th>Gap</th></tr>{fw_rows}</table></div>

<h2>AI systems and risk tiers</h2>
<div class="card wrap"><table><tr><th>System</th><th>Role</th><th>Risk tier</th><th>Basis</th></tr>{sys_rows}</table></div>

<h2>Domains</h2><div class="grid">{domains}</div>

<h2>Gaps and recommendations ({len(gaps)})</h2>
{''.join(_control(r, i < 3) for i, r in enumerate(gaps)) or '<div class="card">No gaps identified.</div>'}

<h2>Roadmap</h2><div class="grid">{roadmap or '<div class="card">Nothing to remediate.</div>'}</div>

<h2>Controls met or not applicable ({len(others)})</h2>
{''.join(_control(r) for r in others)}

{'<h2>Notes and limitations</h2>' + warnings if warnings else ''}
<footer>{h(DISCLAIMER)}<br>Evidence items reviewed: {len(a.evidence_index)} · Assessment id {h(a.id)} · aigov {h(a.tool_version)}</footer>
</main></body></html>"""


RENDERERS = {"json": to_json, "md": to_markdown, "html": to_html}
