"""Web platform: rule library, entity profiles, evidence intake, compliance tests and reports.

Runs entirely on your own infrastructure. The server makes no outbound network calls, and the
browser UI is locked to this origin by a Content-Security-Policy, so nothing is sent to any
external service or AI API.

Environment:
    AIGOV_DB         SQLite file (default ./aigov-data/aigov.db)
    AIGOV_API_TOKEN  if set, every /api call needs "Authorization: Bearer <token>"
"""
from __future__ import annotations

import base64
import binascii
import hmac
import io
import os
import re
import tempfile
import zipfile
from pathlib import Path
from typing import Literal, Optional

import yaml
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .. import __version__
from ..catalog import build_requirement, controls_by_id, load_controls, load_frameworks, load_requirements, ref_slug
from ..connectors.documents import DocumentsConnector, _read
from ..connectors.inventory import InventoryConnector
from ..connectors.questionnaire import parse_answers
from ..connectors.repo import RepoConnector
from ..engine.applicability import (ENTITY_FLAGS, FLAG_LABELS, JURISDICTIONS, classify_profile, derive_flags,
                                    framework_applies, requirement_applies)
from ..engine.assess import requirement_evidence, run_assessment
from ..engine.evidence import control_evidence, merge_signals
from ..models import AISystem, Answer, Assessment, Entity, Evidence, Profile, Requirement
from ..report.render import RENDERERS
from .db import DB

STATIC = Path(__file__).parent / "static"
MAX_UPLOAD = 25 * 1024 * 1024          # per file, decoded
MAX_ZIP_TOTAL = 200 * 1024 * 1024      # uncompressed
MAX_ZIP_FILES = 5000
CSP = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
       "connect-src 'self'; font-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")


class RuleIn(BaseModel):
    framework: str = "custom"
    ref: str = Field(min_length=1, max_length=80)
    title: str = Field(min_length=1, max_length=300)
    chapter: str = "Custom rules"
    summary: str = ""
    note: str = ""
    tests: list[str] = Field(default_factory=list)
    controls: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    need: list[str] = Field(default_factory=list)
    when: list[str] = Field(default_factory=list)
    weight: int = Field(default=2, ge=1, le=3)
    binding: Optional[bool] = None
    action: str = ""
    owner: str = ""


class EntityIn(BaseModel):
    entity: Entity
    systems: list[AISystem] = Field(default_factory=list)


class TextEvidenceIn(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    text: str = Field(min_length=1)
    kind: Literal["document", "api", "repository"] = "document"
    signals: dict = Field(default_factory=dict)


class FileIn(BaseModel):
    filename: str = Field(min_length=1, max_length=300)
    content_b64: str


class AnswerIn(BaseModel):
    test_id: str
    answer: Optional[Literal["yes", "partial", "no", "na"]] = None   # null clears the answer
    note: str = ""
    evidence_ref: str = ""


def auth(authorization: Optional[str] = Header(default=None)) -> None:
    token = os.environ.get("AIGOV_API_TOKEN")
    if token and not hmac.compare_digest(authorization or "", f"Bearer {token}"):
        raise HTTPException(401, "invalid or missing bearer token")


def create_app(db_path: str | None = None) -> FastAPI:
    db = DB(db_path or os.environ.get("AIGOV_DB", "aigov-data/aigov.db"))
    app = FastAPI(title="aigov", version=__version__, docs_url="/api/docs", openapi_url="/api/openapi.json")
    app.state.db = db
    api = Depends(auth)

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        resp = await call_next(request)
        if not request.url.path.startswith("/api/docs"):
            resp.headers["Content-Security-Policy"] = CSP
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Referrer-Policy"] = "no-referrer"
        return resp

    # ------------------------------------------------------------------ helpers
    def custom_rules() -> list[Requirement]:
        return [Requirement(**r) for r in db.list_rules()]

    def all_requirements() -> list[Requirement]:
        return load_requirements(custom_rules())

    def entity_or_404(eid: str) -> Profile:
        d = db.get_entity(eid)
        if d is None:
            raise HTTPException(404, "entity not found")
        return Profile(**d)

    def evidence_for(eid: str, profile: Profile) -> list[Evidence]:
        ev = InventoryConnector(systems=profile.systems).collect()
        for r in db.list_evidence(eid, with_text=True):
            ev.append(Evidence(id=r["ev_id"], connector=r["connector"], kind=r["kind"], title=r["title"], text=r["text"] or "", signals=r["signals"]))
        return ev

    def answers_for(eid: str) -> list[Answer]:
        return [Answer(test_id=a["test_id"], answer=a["answer"], note=a["note"] or "", evidence_ref=a["evidence_ref"] or "") for a in db.get_answers(eid)]

    def req_json(r: Requirement) -> dict:
        d = r.model_dump()
        d["need_labels"] = [FLAG_LABELS.get(f, f) for f in r.need]
        d["when_labels"] = [FLAG_LABELS.get(f, f) for f in r.when]
        d["binding_effective"] = load_frameworks()[r.framework].binding if r.binding is None else r.binding
        return d

    # ------------------------------------------------------------------ meta and library
    @app.get("/api/meta", dependencies=[api])
    def meta():
        reqs = all_requirements()
        fws = []
        for k, f in load_frameworks().items():
            mine = [r for r in reqs if r.framework == k]
            fws.append({**f.model_dump(), "articles": len(mine), "assessable": sum(r.kind != "info" for r in mine),
                        "tests": sum(len(r.tests) for r in mine)})
        return {
            "version": __version__, "frameworks": fws, "flags": FLAG_LABELS, "entity_flags": ENTITY_FLAGS,
            "jurisdictions": JURISDICTIONS,
            "controls": [{"id": c.id, "title": c.title, "domain": c.domain} for c in load_controls()],
        }

    @app.get("/api/library", dependencies=[api])
    def library(framework: str = "", q: str = "", kind: Literal["all", "obligation", "info"] = "all"):
        out = []
        ql = q.lower().strip()
        for r in all_requirements():
            if framework and r.framework != framework:
                continue
            if kind != "all" and r.kind != kind:
                continue
            if ql and ql not in " ".join([r.id, r.ref, r.title, r.summary, r.note, r.chapter, *[t.question for t in r.tests]]).lower():
                continue
            out.append(req_json(r))
        return out


    def build_rule(body: RuleIn, rid: str | None = None) -> Requirement:
        if body.framework not in load_frameworks():
            raise HTTPException(422, f"unknown framework {body.framework}")
        bad = [c for c in body.controls if c not in controls_by_id()]
        bad += [f for f in body.need + body.when if f not in FLAG_LABELS]
        if bad:
            raise HTTPException(422, f"unknown control or flag: {bad}")
        tests = [t.strip() for t in body.tests if t.strip()]
        item = body.model_dump(exclude={"framework", "tests", "chapter"})
        item.update(id=rid or f"CUSTOM.{body.framework.upper()}.{ref_slug(body.ref)}", tests=tests,
                    keywords=[k.strip() for k in body.keywords if k.strip()])
        return build_requirement(body.framework, "CUSTOM", item, body.chapter or "Custom rules", custom=True)

    @app.post("/api/rules", status_code=201, dependencies=[api])
    def create_rule(body: RuleIn):
        r = build_rule(body)
        if any(x.id == r.id for x in all_requirements()):
            raise HTTPException(409, f"a rule with id {r.id} already exists; use a different reference")
        db.save_rule(r.id, r.model_dump())
        return req_json(r)

    @app.put("/api/rules/{rid}", dependencies=[api])
    def update_rule(rid: str, body: RuleIn):
        if not any(x["id"] == rid for x in db.list_rules()):
            raise HTTPException(404, "custom rule not found (built-in rules are read-only)")
        r = build_rule(body, rid)
        db.save_rule(rid, r.model_dump())
        return req_json(r)

    @app.delete("/api/rules/{rid}", dependencies=[api])
    def delete_rule(rid: str):
        if not db.delete_rule(rid):
            raise HTTPException(404, "custom rule not found (built-in rules are read-only)")
        return {"deleted": rid}

    # ------------------------------------------------------------------ entities

    @app.get("/api/entities", dependencies=[api])
    def list_entities():
        return db.list_entities()

    @app.post("/api/entities", status_code=201, dependencies=[api])
    def create_entity(body: EntityIn):
        eid = db.save_entity(Profile(**body.model_dump()).model_dump())
        return {"id": eid}

    @app.get("/api/entities/{eid}", dependencies=[api])
    def get_entity(eid: str):
        return {"id": eid, "profile": entity_or_404(eid)}

    @app.put("/api/entities/{eid}", dependencies=[api])
    def update_entity(eid: str, body: EntityIn):
        entity_or_404(eid)
        ids = [s.id for s in body.systems]
        if len(ids) != len(set(ids)):
            raise HTTPException(422, "system ids must be unique")
        db.save_entity(Profile(**body.model_dump()).model_dump(), eid)
        return scope(eid)

    @app.delete("/api/entities/{eid}", dependencies=[api])
    def delete_entity(eid: str):
        entity_or_404(eid)
        db.delete_entity(eid)
        return {"deleted": eid}

    @app.get("/api/entities/{eid}/scope", dependencies=[api])
    def scope(eid: str, details: bool = False):
        """What applies to this entity; with details=true, every in-scope article with its tests, answers and evidence check."""
        profile = entity_or_404(eid)
        warnings = classify_profile(profile)
        flags = derive_flags(profile)
        fws = load_frameworks()
        fw_scope = {k: framework_applies(f, profile, flags) for k, f in fws.items()}
        reqs = all_requirements()
        in_scope = [r for r in reqs if r.kind != "info" and fw_scope[r.framework][0] and requirement_applies(r, flags)[0]]
        out = {
            "flags": sorted(flags), "warnings": warnings,
            "systems": [s.model_dump() for s in profile.systems],
            "frameworks": [{"key": k, "name": f.name, "binding": f.binding, "applicable": fw_scope[k][0], "reason": fw_scope[k][1],
                            "in_scope": sum(r.framework == k for r in in_scope), "articles": sum(r.framework == k for r in reqs)}
                           for k, f in fws.items() if k != "custom" or any(r.framework == "custom" for r in reqs)],
            "articles_in_scope": len(in_scope), "tests_in_scope": sum(len(r.tests) for r in in_scope),
        }
        if details:
            evidence = evidence_for(eid, profile)
            signals = merge_signals(evidence)
            cev = {c.id: control_evidence(c, evidence, signals) for c in load_controls()}
            answers = {a["test_id"]: a for a in db.get_answers(eid)}
            items = []
            for r in in_scope:
                ce = requirement_evidence(r, cev, evidence, signals)
                best = max(ce, key=lambda c: c.score, default=None)
                d = req_json(r)
                d["evidence"] = {
                    "score": round(sum(c.score for c in ce) / len(ce), 2) if ce else 0,
                    "doc": best.doc_title if best else "", "quotes": best.quotes[:2] if best else [],
                    "caveats": [c for x in ce for c in x.caveats][:2],
                    "notes": best.notes[:2] if best else [],
                }
                d["answers"] = {t.id: answers[t.id] for t in r.tests if t.id in answers}
                items.append(d)
            out["requirements"] = items
            out["evidence_items"] = [{"id": e.id, "title": e.title} for e in evidence if e.kind != "inventory"]
        return out

    # ------------------------------------------------------------------ evidence


    @app.get("/api/entities/{eid}/evidence", dependencies=[api])
    def list_evidence(eid: str):
        entity_or_404(eid)
        return db.list_evidence(eid)

    @app.post("/api/entities/{eid}/evidence", status_code=201, dependencies=[api])
    def add_text_evidence(eid: str, body: TextEvidenceIn):
        """Push evidence from another system (GRC tool, ticketing, CI) or paste text."""
        entity_or_404(eid)
        prefix = {"document": "doc", "api": "api", "repository": "repo"}[body.kind]
        return db.add_evidence(eid, {"id": f"{prefix}:{body.title}", "title": body.title, "kind": body.kind,
                                     "connector": "api", "text": body.text, "signals": body.signals})

    @app.post("/api/entities/{eid}/evidence/file", status_code=201, dependencies=[api])
    def add_file_evidence(eid: str, body: FileIn):
        """Upload a document (md, txt, pdf, docx, json, yaml, csv) or a .zip of a repository / policy folder."""
        entity_or_404(eid)
        try:
            raw = base64.b64decode(body.content_b64, validate=True)
        except (binascii.Error, ValueError):
            raise HTTPException(422, "content_b64 is not valid base64")
        if len(raw) > MAX_UPLOAD:
            raise HTTPException(413, "file too large (25 MB limit)")
        name = Path(body.filename).name
        with tempfile.TemporaryDirectory() as tmp:
            if name.lower().endswith(".zip"):
                root = Path(tmp) / Path(name).stem
                _safe_extract(raw, root)
                items: list[Evidence] = []
                repo = RepoConnector(path=str(root))
                items += [e for e in repo.collect() if e.kind == "repository"]
                docs = DocumentsConnector(path=str(root))
                items += [e.model_copy(update={"id": f"doc:{name}/{e.title}", "title": f"{name}/{e.title}"})
                          for e in docs.collect() if Path(e.ref).suffix.lower() in {".md", ".txt", ".pdf", ".docx", ".rst", ".html"}]
                added = [db.add_evidence(eid, e.model_dump()) for e in items]
                return {"added": added, "warnings": repo.warnings + docs.warnings}
            p = Path(tmp) / name
            p.write_bytes(raw)
            try:
                text = _read(p)
            except Exception as e:
                raise HTTPException(422, f"could not read {name}: {e}")
            if not text or not text.strip():
                raise HTTPException(422, f"no readable text in {name} (supported: md, txt, pdf, docx, json, yaml, csv, zip)")
        return {"added": [db.add_evidence(eid, {"id": f"doc:{name}", "title": name, "kind": "document", "connector": "upload", "text": text})], "warnings": []}

    @app.delete("/api/entities/{eid}/evidence/{rid}", dependencies=[api])
    def delete_evidence(eid: str, rid: str):
        if not db.delete_evidence(eid, rid):
            raise HTTPException(404, "evidence not found")
        return {"deleted": rid}

    # ------------------------------------------------------------------ answers

    @app.get("/api/entities/{eid}/answers", dependencies=[api])
    def get_answers(eid: str):
        entity_or_404(eid)
        return db.get_answers(eid)

    @app.put("/api/entities/{eid}/answers", dependencies=[api])
    def put_answers(eid: str, body: list[AnswerIn]):
        entity_or_404(eid)
        valid = {t.id for r in all_requirements() for t in r.tests}
        bad = [a.test_id for a in body if a.test_id not in valid]
        if bad:
            raise HTTPException(422, f"unknown test id(s): {bad[:10]}")
        for a in body:
            db.put_answer(eid, a.test_id, a.answer, a.note, a.evidence_ref)
        db.touch(eid)
        return {"saved": len(body)}

    @app.post("/api/entities/{eid}/answers/import", dependencies=[api])
    async def import_answers(eid: str, request: Request):
        """Body: YAML or JSON mapping of test id or article id -> answer (same format as the CLI questionnaire)."""
        entity_or_404(eid)
        try:
            parsed = parse_answers(yaml.safe_load(await request.body()))
        except Exception as e:
            raise HTTPException(422, f"could not parse answers: {e}")
        reqs = {r.id: r for r in all_requirements()}
        tests = {t.id for r in reqs.values() for t in r.tests}
        saved, unknown = 0, []
        for a in parsed:
            targets = [t.id for t in reqs[a.test_id].tests] if a.test_id in reqs else [a.test_id] if a.test_id in tests else []
            if not targets:
                unknown.append(a.test_id)
            for t in targets:
                db.put_answer(eid, t, a.answer, a.note, a.evidence_ref)
                saved += 1
        return {"saved": saved, "unknown": unknown}

    # ------------------------------------------------------------------ assessments
    @app.post("/api/entities/{eid}/assessments", status_code=201, dependencies=[api])
    def run(eid: str):
        profile = entity_or_404(eid)
        a = run_assessment(profile, evidence_for(eid, profile), answers_for(eid), custom_rules())
        db.save_assessment(eid, a.id, a.overall_score, a.model_dump_json())
        return a

    @app.get("/api/entities/{eid}/assessments", dependencies=[api])
    def history(eid: str):
        entity_or_404(eid)
        return db.list_assessments(eid)

    def assessment_or_404(aid: str) -> Assessment:
        data = db.get_assessment(aid)
        if data is None:
            raise HTTPException(404, "assessment not found")
        return Assessment.model_validate_json(data)

    @app.get("/api/assessments/{aid}", dependencies=[api])
    def get_assessment(aid: str):
        return assessment_or_404(aid)

    @app.get("/api/assessments/{aid}/report", dependencies=[api])
    def report(aid: str, format: Literal["html", "md", "json", "csv"] = "html"):
        a = assessment_or_404(aid)
        body = RENDERERS[format](a)
        slug = re.sub(r"[^A-Za-z0-9]+", "-", a.profile.entity.name).strip("-").lower() or "entity"
        media = {"html": "text/html", "md": "text/markdown", "json": "application/json", "csv": "text/csv"}[format]
        return Response(body, media_type=media + "; charset=utf-8",
                        headers={"Content-Disposition": f'attachment; filename="aigov-{slug}-{a.created_at[:10]}.{format}"'})

    # ------------------------------------------------------------------ UI
    app.mount("/static", StaticFiles(directory=STATIC), name="static")

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(STATIC / "index.html")

    @app.get("/health", include_in_schema=False)
    def health():
        return PlainTextResponse("ok")

    return app


def _safe_extract(raw: bytes, dest: Path) -> None:
    """Extract a zip without path traversal, symlinks or zip bombs."""
    try:
        zf = zipfile.ZipFile(io.BytesIO(raw))
    except zipfile.BadZipFile:
        raise HTTPException(422, "not a valid zip file")
    members = [m for m in zf.infolist() if not m.is_dir()]
    if len(members) > MAX_ZIP_FILES:
        raise HTTPException(413, f"zip has more than {MAX_ZIP_FILES} files")
    if sum(m.file_size for m in members) > MAX_ZIP_TOTAL:
        raise HTTPException(413, "zip expands beyond 200 MB")
    root = dest.resolve()
    for m in members:
        if (m.external_attr >> 16) & 0o170000 == 0o120000:  # symlink
            continue
        target = (root / m.filename).resolve()
        if not str(target).startswith(str(root) + os.sep):
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with zf.open(m) as src, open(target, "wb") as out:
            out.write(src.read())

