"""Command line interface.

    aigov assess -c aigov.yaml --out reports/           run an assessment
    aigov assess -c aigov.yaml --fail-on critical       CI gate (exit code 2 on breach)
    aigov questionnaire --out answers.yaml              self-assessment template
    aigov frameworks | controls | connectors            inspect the catalog
    aigov serve --port 8080                             REST API
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

from .catalog import load_controls, load_frameworks
from .connectors.base import available
from .engine import ai
from .engine.assess import run_assessment
from .pipeline import collect_file
from .report.render import RENDERERS

PRIORITIES = ["low", "medium", "high", "critical"]


def _post(url: str, payload: dict) -> None:
    if not url.lower().startswith(("https://", "http://")):
        raise ValueError("webhook must be an http(s) URL")
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=30).close()  # noqa: S310


def webhook_payload(a) -> dict:
    return {
        "assessment_id": a.id, "entity": a.profile.entity.name, "overall_score": a.overall_score, "maturity": a.maturity,
        "frameworks": {f.key: f.score for f in a.frameworks if f.applicable},
        "gaps": [{
            "control_id": g.control_id, "title": g.title, "status": g.status, "priority": g.priority,
            "legally_binding": g.legally_binding, "recommendation": g.recommendations[0].action if g.recommendations else "",
            "owner": g.recommendations[0].owner if g.recommendations else "",
        } for g in a.gaps()],
    }


def cmd_assess(args) -> int:
    profile, evidence, attestations, warnings = collect_file(args.config)
    print(f"Collected {len(evidence)} evidence item(s) for {profile.entity.name}; assessing ({args.mode} mode)...", file=sys.stderr)
    try:
        a = run_assessment(profile, evidence, attestations, mode=args.mode, warnings=warnings, evidence_budget=args.evidence_budget)
    except ai.AIError as e:
        print(f"AI assessment failed: {e}", file=sys.stderr)
        return 1

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for fmt in args.format.split(","):
        path = out / f"assessment.{fmt.strip()}"
        path.write_text(RENDERERS[fmt.strip()](a))
        print(f"Wrote {path}", file=sys.stderr)

    gaps = a.gaps()
    print(f"\n{profile.entity.name}: {a.overall_score:.0f}/100 ({a.maturity}) - {'AI-assisted' if a.mode == 'ai' else 'rule-based'}")
    for f in a.frameworks:
        if f.applicable and f.score is not None:
            print(f"  {f.name:<48} {f.score:>5.0f}  {'binding' if f.binding else 'voluntary'}")
    print(f"  {len(gaps)} open finding(s): " + ", ".join(f"{sum(g.priority == p for g in gaps)} {p}" for p in reversed(PRIORITIES)))
    for g in gaps[:8]:
        print(f"  [{g.priority:<8}] {g.control_id} {g.title}")
    for w in a.warnings:
        print(f"  note: {w}", file=sys.stderr)

    if args.webhook:
        try:
            _post(args.webhook, webhook_payload(a))
        except Exception as e:
            print(f"webhook failed: {e}", file=sys.stderr)

    breached = []
    if args.fail_under is not None and a.overall_score < args.fail_under:
        breached.append(f"overall score {a.overall_score:.0f} is below {args.fail_under:.0f}")
    if args.fail_on:
        floor = PRIORITIES.index(args.fail_on)
        n = sum(PRIORITIES.index(g.priority) >= floor for g in gaps if g.priority)
        if n:
            breached.append(f"{n} gap(s) at {args.fail_on} priority or above")
    if breached:
        print("GATE FAILED: " + "; ".join(breached), file=sys.stderr)
        return 2
    return 0


def cmd_questionnaire(args) -> int:
    lines = ["# Answer each control: yes | partial | no | na. Add notes and a pointer to the evidence."]
    domain = None
    for c in load_controls():
        if c.domain != domain:
            domain = c.domain
            lines += ["", f"# --- {domain}"]
        lines += [f"# {c.title}: {' '.join(c.objective.split())}", f"{c.id}: {{answer: no, notes: \"\", evidence_ref: \"\"}}"]
    text = "\n".join(lines) + "\n"
    if args.out:
        Path(args.out).write_text(text)
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


def cmd_frameworks(_) -> int:
    for f in load_frameworks().values():
        n = sum(f.key in c.mappings for c in load_controls())
        print(f"{f.key:<16} {'binding' if f.binding else 'voluntary':<10} {n:>2} controls  {f.name} ({f.citation})")
    return 0


def cmd_controls(args) -> int:
    for c in load_controls():
        if args.framework and args.framework not in c.mappings:
            continue
        refs = ", ".join(c.mappings[args.framework]) if args.framework else ", ".join(c.mappings)
        print(f"{c.id:<7} w{c.weight}  {c.title:<62} {refs}")
    return 0


def cmd_connectors(_) -> int:
    for name, cls in sorted(available().items()):
        print(f"{name:<14} {(cls.__doc__ or '').strip().splitlines()[0] if cls.__doc__ else ''}")
    return 0


def cmd_serve(args) -> int:
    import uvicorn
    uvicorn.run("aigov.api:app", host=args.host, port=args.port)
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="aigov", description="AI governance and compliance assessment")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("assess", help="collect evidence and assess")
    a.add_argument("-c", "--config", required=True)
    a.add_argument("--mode", choices=["auto", "ai", "rules"], default="auto")
    a.add_argument("--out", default="aigov-report")
    a.add_argument("--format", default="html,json,md")
    a.add_argument("--fail-under", type=float, help="exit 2 if the overall score is below this")
    a.add_argument("--fail-on", choices=PRIORITIES, help="exit 2 if any gap has this priority or higher")
    a.add_argument("--webhook", help="POST a JSON summary of gaps to this URL")
    a.add_argument("--evidence-budget", type=int, default=ai.DEFAULT_EVIDENCE_BUDGET, help="max evidence characters sent to the model")
    a.set_defaults(fn=cmd_assess)

    q = sub.add_parser("questionnaire", help="write a self-assessment template")
    q.add_argument("--out")
    q.set_defaults(fn=cmd_questionnaire)
    sub.add_parser("frameworks", help="list frameworks").set_defaults(fn=cmd_frameworks)
    c = sub.add_parser("controls", help="list controls")
    c.add_argument("--framework")
    c.set_defaults(fn=cmd_controls)
    sub.add_parser("connectors", help="list connectors").set_defaults(fn=cmd_connectors)
    s = sub.add_parser("serve", help="run the REST API")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8080)
    s.set_defaults(fn=cmd_serve)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
