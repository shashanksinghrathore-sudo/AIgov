"""REST API so other systems (GRC platforms, CI, internal portals) can push evidence and pull findings.

    POST /assessments            run an assessment on a pushed profile + evidence
    GET  /assessments/{id}       full result (JSON)
    GET  /assessments/{id}/report?format=html|md|json
    GET  /assessments/{id}/gaps  prioritised gaps, ready to turn into tickets
    GET  /frameworks, /controls  the catalog

Set AIGOV_API_TOKEN to require `Authorization: Bearer <token>` on every call.
Results are kept in memory and, when AIGOV_STORE is set, written to that folder as JSON.
The API accepts pushed content only; it does not read server-side paths or fetch URLs on a caller's behalf.
"""
from __future__ import annotations

import hmac
import os
import re
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel, Field

from . import __version__
from .catalog import load_controls, load_frameworks
from .cli import webhook_payload
from .connectors.inventory import InventoryConnector
from .connectors.questionnaire import QuestionnaireConnector
from .engine import ai
from .engine.assess import run_assessment
from .models import AISystem, Assessment, Entity, Evidence, Profile
from .report.render import RENDERERS


def auth(authorization: str | None = Header(default=None)) -> None:
    token = os.environ.get("AIGOV_API_TOKEN")
    if token and not hmac.compare_digest(authorization or "", f"Bearer {token}"):
        raise HTTPException(401, "invalid or missing bearer token")


app = FastAPI(title="aigov", version=__version__, description=__doc__, dependencies=[Depends(auth)])
_STORE: dict[str, Assessment] = {}


class DocumentIn(BaseModel):
    title: str
    text: str
    kind: Literal["document", "api", "repository"] = "document"
    signals: dict = Field(default_factory=dict)


class AssessmentIn(BaseModel):
    entity: Entity
    systems: list[AISystem] = Field(default_factory=list)
    documents: list[DocumentIn] = Field(default_factory=list)
    answers: dict = Field(default_factory=dict, description="questionnaire answers keyed by control id")
    mode: Literal["auto", "ai", "rules"] = "auto"


def _get(aid: str) -> Assessment:
    if aid not in _STORE:
        store = os.environ.get("AIGOV_STORE")
        path = Path(store) / f"{aid}.json" if store and re.fullmatch(r"[0-9a-f]{12}", aid) else None
        if path and path.exists():
            _STORE[aid] = Assessment.model_validate_json(path.read_text())
        else:
            raise HTTPException(404, "assessment not found")
    return _STORE[aid]


@app.get("/health")
def health():
    return {"status": "ok", "version": __version__, "ai_credentials": ai.credentials_present()}


@app.get("/frameworks")
def frameworks():
    return list(load_frameworks().values())


@app.get("/controls")
def controls():
    return load_controls()


@app.post("/assessments", status_code=201)
def create(body: AssessmentIn):
    profile = Profile(entity=body.entity, systems=body.systems)
    q = QuestionnaireConnector(answers=body.answers)
    try:
        attestations = q.attestations()
    except Exception as e:
        raise HTTPException(422, f"invalid answers: {e}")
    evidence = InventoryConnector(systems=body.systems).collect() + q.collect()
    seen = set()
    for i, d in enumerate(body.documents):
        eid = f"{'doc' if d.kind == 'document' else d.kind}:{d.title}"
        if eid in seen:
            eid += f"#{i}"
        seen.add(eid)
        evidence.append(Evidence(id=eid, connector="api", kind=d.kind, title=d.title, text=d.text, signals=d.signals))
    try:
        a = run_assessment(profile, evidence, attestations, mode=body.mode)
    except ai.AIError as e:
        raise HTTPException(502, f"AI assessment failed: {e}")
    _STORE[a.id] = a
    store = os.environ.get("AIGOV_STORE")
    if store:
        Path(store).mkdir(parents=True, exist_ok=True)
        (Path(store) / f"{a.id}.json").write_text(a.model_dump_json())
    return a


@app.get("/assessments/{aid}")
def read(aid: str):
    return _get(aid)


@app.get("/assessments/{aid}/gaps")
def gaps(aid: str):
    return webhook_payload(_get(aid))


@app.get("/assessments/{aid}/report")
def report(aid: str, format: Literal["html", "md", "json"] = "html"):
    body = RENDERERS[format](_get(aid))
    if format == "html":
        return HTMLResponse(body)
    return PlainTextResponse(body, media_type="application/json" if format == "json" else "text/markdown")
