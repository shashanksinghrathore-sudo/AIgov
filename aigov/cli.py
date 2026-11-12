"""Command line interface.

    aigov serve --port 8080                             start the web platform
    aigov assess -c aigov.yaml --out reports/           run the compliance tests from a config file
    aigov assess -c aigov.yaml --fail-on critical       CI gate (exit code 2 on breach)
    aigov questionnaire --framework eu_ai_act           answer template for the tests
    aigov frameworks | requirements | connectors        inspect the rule library
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .catalog import builtin_requirements, load_frameworks
from .connectors.base import available
from .engine.assess import run_assessment
from .pipeline import collect_file
from .report.render import RENDERERS

PRIORITIES = ["low", "medium", "high", "critical"]


def cmd_assess(args) -> int:
    profile, evidence, answers, custom, warnings = collect_file(args.config)
    print(f"Collected {len(evidence)} evidence item(s) and {len(answers)} answer(s) for {profile.entity.name}; testing...", file=sys.stderr)
    a = run_assessment(profile, evidence, answers, custom, warnings)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for fmt in [f.strip() for f in args.format.split(",") if f.strip()]:
        path = out / f"assessment.{fmt}"
        path.write_text(RENDERERS[fmt](a))
        print(f"Wrote {path}", file=sys.stderr)

    gaps = a.gaps()
    print(f"\n{profile.entity.name}: {a.overall_score:.0f}/100 ({a.maturity}); {a.tests_answered}/{a.tests_total} tests answered")
    for f in a.frameworks:
        if f.applicable and f.score is not None:
            print(f"  {f.name:<48} {f.score:>5.0f}  {f.in_scope:>3} articles  {'binding' if f.binding else 'voluntary'}")
    print(f"  {len(gaps)} article(s) with gaps: " + ", ".join(f"{sum(g.priority == p for g in gaps)} {p}" for p in reversed(PRIORITIES)))
    fws = load_frameworks()
    for g in gaps[:10]:
        print(f"  [{g.priority:<8}] {fws[g.framework].name} {g.ref} {g.title}")
    for w in a.warnings:
        print(f"  note: {w}", file=sys.stderr)

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
    lines = ["# Answer each test: yes | partial | no | na. Delete lines you do not want to answer.",
             "# A key without '-T<n>' answers every test of that article.", ""]
    chapter = None
    for r in builtin_requirements():
        if r.kind == "info" or (args.framework and r.framework != args.framework):
            continue
        if r.chapter != chapter:
            chapter = r.chapter
            lines += ["", f"# ===== {load_frameworks()[r.framework].name} - {chapter}"]
        lines.append(f"# {r.ref} {r.title}")
        for t in r.tests:
            lines += [f"#   {' '.join(t.question.split())}", f'{t.id}: {{answer: no, note: "", evidence_ref: ""}}']
    text = "\n".join(lines) + "\n"
    if args.out:
        Path(args.out).write_text(text)
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


def cmd_frameworks(_) -> int:
    reqs = builtin_requirements()
    for f in load_frameworks().values():
        mine = [r for r in reqs if r.framework == f.key]
        if not mine:
            continue
        print(f"{f.key:<16} {'binding' if f.binding else 'voluntary':<10} {len(mine):>4} articles {sum(r.kind != 'info' for r in mine):>4} tested "
              f"{sum(len(r.tests) for r in mine):>4} tests  {f.name}")
    return 0


def cmd_requirements(args) -> int:
    for r in builtin_requirements():
        if args.framework and r.framework != args.framework:
            continue
        if args.tested and r.kind == "info":
            continue
        print(f"{r.id:<24} {'test' if r.kind != 'info' else 'ref ':<4} {len(r.tests):>2}  {r.ref} {r.title}")
    return 0


def cmd_connectors(_) -> int:
    for name, cls in sorted(available().items()):
        print(f"{name:<14} {(cls.__doc__ or '').strip().splitlines()[0] if cls.__doc__ else ''}")
    return 0


def cmd_demo(args) -> int:
    """Load the bundled example entity (profile, documents, repository scan, answers) into the platform database."""
    import os

    from .web.db import DB
    db = DB(args.db or os.environ.get("AIGOV_DB", "aigov-data/aigov.db"))
    profile, evidence, answers, _, _ = collect_file(Path(__file__).parent.parent / "examples" / "acme" / "aigov.yaml"
                                                    if not args.config else args.config)
    eid = db.save_entity(profile.model_dump())
    for e in evidence:
        if e.kind != "inventory":
            db.add_evidence(eid, e.model_dump())
    tests = {t.id: r for r in builtin_requirements() for t in r.tests}
    reqs = {r.id: r for r in builtin_requirements()}
    n = 0
    for a in answers:
        targets = [t.id for t in reqs[a.test_id].tests] if a.test_id in reqs else [a.test_id] if a.test_id in tests else []
        for t in targets:
            db.put_answer(eid, t, a.answer, a.note, a.evidence_ref)
            n += 1
    print(f"Loaded '{profile.entity.name}' as entity {eid}: {len(evidence)} evidence item(s), {n} answer(s).")
    return 0


def cmd_serve(args) -> int:
    import os

    import uvicorn
    if args.db:
        os.environ["AIGOV_DB"] = args.db
    local = args.host in ("127.0.0.1", "localhost", "::1")
    if not local and not os.environ.get("AIGOV_API_TOKEN") and not args.allow_no_auth:
        print("Refusing to listen on a public address without AIGOV_API_TOKEN set: anyone could read and change the data.\n"
              "Set AIGOV_API_TOKEN to a long random value, or pass --allow-no-auth if access is controlled elsewhere.", file=sys.stderr)
        return 1
    print(f"AI Compliance Platform on http://{args.host}:{args.port}  (data: {os.environ.get('AIGOV_DB', 'aigov-data/aigov.db')})", file=sys.stderr)
    uvicorn.run("aigov.web.app:create_app", factory=True, host=args.host, port=args.port,
                proxy_headers=True, forwarded_allow_ips="*" if not local else "127.0.0.1")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="aigov", description="AI governance and compliance testing platform (rule-based, offline)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("serve", help="start the web platform")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=int(__import__("os").environ.get("PORT", "8080")),
                   help="port (default: $PORT, else 8080)")
    s.add_argument("--allow-no-auth", action="store_true", help="allow a public bind without AIGOV_API_TOKEN")
    s.add_argument("--db", help="SQLite database file (default aigov-data/aigov.db)")
    s.set_defaults(fn=cmd_serve)

    d = sub.add_parser("demo", help="load the example entity into the platform database")
    d.add_argument("--db")
    d.add_argument("-c", "--config", help="config file to load instead of the bundled example")
    d.set_defaults(fn=cmd_demo)

    a = sub.add_parser("assess", help="run the compliance tests from a config file")
    a.add_argument("-c", "--config", required=True)
    a.add_argument("--out", default="aigov-report")
    a.add_argument("--format", default="html,json,md,csv")
    a.add_argument("--fail-under", type=float, help="exit 2 if the overall score is below this")
    a.add_argument("--fail-on", choices=PRIORITIES, help="exit 2 if any gap has this priority or higher")
    a.set_defaults(fn=cmd_assess)

    q = sub.add_parser("questionnaire", help="write an answer template for the tests")
    q.add_argument("--framework")
    q.add_argument("--out")
    q.set_defaults(fn=cmd_questionnaire)
    sub.add_parser("frameworks", help="list frameworks").set_defaults(fn=cmd_frameworks)
    r = sub.add_parser("requirements", help="list articles and clauses")
    r.add_argument("--framework")
    r.add_argument("--tested", action="store_true", help="only articles that carry tests")
    r.set_defaults(fn=cmd_requirements)
    sub.add_parser("connectors", help="list evidence connectors").set_defaults(fn=cmd_connectors)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
