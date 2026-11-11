import base64
import io
import json
import re
import socket
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aigov.catalog import builtin_requirements, load_frameworks
from aigov.cli import main
from aigov.engine.applicability import classify_system
from aigov.engine.assess import priority_for, run_assessment
from aigov.models import AISystem, Answer, Entity, Evidence, Profile
from aigov.pipeline import collect_file
from aigov.web.app import create_app

EXAMPLE = Path(__file__).parent.parent / "examples" / "acme" / "aigov.yaml"


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Every test fails if anything tries to open a connection to a non-loopback address."""
    real = socket.socket.connect

    def guarded(self, address):
        host = address[0] if isinstance(address, tuple) else address
        if host not in ("127.0.0.1", "::1", "localhost") and not str(host).startswith("/"):
            raise AssertionError(f"outbound network call attempted to {address}")
        return real(self, address)
    monkeypatch.setattr(socket.socket, "connect", guarded)


def by_id(a):
    return {r.id: r for r in a.results}


# --------------------------------------------------------------------------- rule library
def numbers(fw, pattern):
    return {int(m.group(1)) for r in builtin_requirements() if r.framework == fw for m in [re.fullmatch(pattern, r.ref)] if m}


def test_library_lists_every_article():
    assert numbers("eu_ai_act", r"Art\. (\d+)") == set(range(1, 114))
    assert numbers("gdpr", r"Art\. (\d+)") == set(range(1, 100))
    assert numbers("india_dpdp", r"s\. (\d+)") == set(range(1, 45))
    nist = [r for r in builtin_requirements() if r.framework == "nist_ai_rmf"]
    assert len(nist) == 72
    iso = [r for r in builtin_requirements() if r.framework == "iso_42001"]
    assert sum(r.ref.startswith("A.") for r in iso) == 38 and len(iso) == 65


def test_library_rules_are_well_formed():
    reqs = builtin_requirements()
    assert len({r.id for r in reqs}) == len(reqs)
    for r in reqs:
        if r.kind == "info":
            assert not r.tests
        else:
            assert r.tests and r.summary and 1 <= r.weight <= 3, r.id
            assert r.controls, f"{r.id} has no evidence checks"


def test_risk_classification():
    assert classify_system(AISystem(id="1", name="CV screening for hiring"))[0] == "high"
    assert classify_system(AISystem(id="2", name="Social scoring of citizens"))[0] == "prohibited"
    assert classify_system(AISystem(id="3", name="FAQ chatbot", generative=True))[0] == "limited"
    assert classify_system(AISystem(id="4", name="Warehouse demand forecast"))[0] == "minimal"


# --------------------------------------------------------------------------- engine
def test_scope_follows_jurisdiction_and_flags():
    p = Profile(entity=Entity(name="X", jurisdictions=["US"]), systems=[AISystem(id="1", name="Demand forecast")])
    a = run_assessment(p, [])
    scope = {f.key: f.applicable for f in a.frameworks}
    assert scope["nist_ai_rmf"] and scope["iso_42001"] and not scope["eu_ai_act"] and not scope["gdpr"]
    assert {r.framework for r in a.results} == {"nist_ai_rmf", "iso_42001", "oecd_ai"}


def test_article_level_applicability():
    p = Profile(entity=Entity(name="X", jurisdictions=["EU"]), systems=[AISystem(id="1", name="Support chatbot", generative=True, consumer_facing=True)])
    r = by_id(run_assessment(p, []))
    assert r["EUAIA.ART.9"].status == "not_applicable"          # high-risk providers only
    assert "high-risk" in r["EUAIA.ART.9"].rationale
    assert r["EUAIA.ART.50"].status != "not_applicable"         # transparency applies to chatbots
    assert r["EUAIA.ART.4"].status != "not_applicable"
    assert "GDPR.ART.5" not in r                                # no personal data -> GDPR out of scope


def test_test_scoring_rules():
    p = Profile(entity=Entity(name="X", jurisdictions=["EU"]), systems=[AISystem(id="1", name="Chatbot", generative=True, consumer_facing=True)])
    doc = Evidence(id="doc:lit.md", connector="t", kind="document", title="lit.md",
                   text="AI literacy training programme for all staff. Completion records are kept. Role-based modules for developers.")
    answers = [Answer(test_id="EUAIA.ART.4", answer="yes"),                       # article-level answer: all tests
               Answer(test_id="EUAIA.ART.4-T2", answer="partial"),                # test-level override
               Answer(test_id="EUAIA.ART.50-T1", answer="yes"),                   # yes, no evidence
               Answer(test_id="EUAIA.ART.50-T2", answer="na"),
               Answer(test_id="EUAIA.ART.50-T3", answer="yes", evidence_ref="lit.md")]  # yes with linked evidence
    r = by_id(run_assessment(p, [doc], answers))
    t4 = {t.test_id: t for t in r["EUAIA.ART.4"].tests}
    assert t4["EUAIA.ART.4-T1"].basis == "verified" and t4["EUAIA.ART.4-T1"].score == 1.0
    assert t4["EUAIA.ART.4-T2"].basis == "partial"
    t50 = {t.test_id: t for t in r["EUAIA.ART.50"].tests}
    assert t50["EUAIA.ART.50-T1"].basis == "attested" and t50["EUAIA.ART.50-T1"].score == 0.6
    assert t50["EUAIA.ART.50-T2"].score is None
    assert t50["EUAIA.ART.50-T3"].basis == "verified"
    assert t50["EUAIA.ART.50-T4"].basis == "no_evidence" and t50["EUAIA.ART.50-T4"].score == 0.0
    assert any("without supporting evidence" in g for g in r["EUAIA.ART.50"].gaps)


def test_priority():
    assert priority_for(3, 0.0, True) == "critical"
    assert priority_for(3, 0.0, False) == "high"
    assert priority_for(1, 0.5, False) == "low"


def test_example_assessment():
    profile, evidence, answers, custom, warnings = collect_file(EXAMPLE)
    a = run_assessment(profile, evidence, answers, custom, warnings)
    r = by_id(a)
    assert all(f.applicable for f in a.frameworks)
    assert r["EUAIA.ART.27"].status == "gap" and r["EUAIA.ART.27"].priority == "critical"
    assert r["EUAIA.ART.11"].status == "met"
    assert r["EUAIA.ART.53"].status == "not_applicable"   # GPAI duties: entity provides no GPAI model
    assert any("TalentRank" in w and "high" in w for w in a.warnings)
    assert a.gaps()[0].priority == "critical"
    # one roadmap action closes several articles across frameworks
    closes = max(len(x["closes"]) for p in a.roadmap for x in p["actions"])
    assert closes >= 5
    assert 0 < a.overall_score < 100 and a.tests_answered > 50


def test_cli(tmp_path, capsys):
    assert main(["assess", "-c", str(EXAMPLE), "--out", str(tmp_path)]) == 0
    assert main(["assess", "-c", str(EXAMPLE), "--out", str(tmp_path), "--fail-on", "critical"]) == 2
    assert main(["assess", "-c", str(EXAMPLE), "--out", str(tmp_path), "--fail-under", "90"]) == 2
    for ext in ("html", "json", "md", "csv"):
        assert (tmp_path / f"assessment.{ext}").stat().st_size > 1000
    assert "<script" not in (tmp_path / "assessment.html").read_text()
    assert main(["questionnaire", "--framework", "gdpr", "--out", str(tmp_path / "q.yaml")]) == 0
    assert "GDPR.ART.35-T1" in (tmp_path / "q.yaml").read_text()


# --------------------------------------------------------------------------- web platform
@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.delenv("AIGOV_API_TOKEN", raising=False)
    return TestClient(create_app(str(tmp_path / "t.db")))


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode()


def test_web_end_to_end(client):
    c = client
    assert "AI Compliance Platform" in c.get("/").text
    assert "default-src 'self'" in c.get("/").headers["content-security-policy"]
    meta = c.get("/api/meta").json()
    assert sum(f["articles"] for f in meta["frameworks"]) == len(builtin_requirements())

    eid = c.post("/api/entities", json={"entity": {"name": "Beta Bank"}, "systems": []}).json()["id"]
    sc = c.put(f"/api/entities/{eid}", json={
        "entity": {"name": "Beta Bank", "jurisdictions": ["EU", "IN"], "attributes": ["international_transfers"]},
        "systems": [{"id": "S1", "name": "Loan scoring", "description": "creditworthiness scoring for loans", "role": "provider", "uses_personal_data": True}],
    }).json()
    assert "high_risk" in sc["flags"] and "credit_or_insurance" in sc["flags"]
    assert {f["key"] for f in sc["frameworks"] if f["applicable"]} >= {"eu_ai_act", "gdpr", "india_dpdp"}

    # evidence: a document, a zip "repository", pushed text
    up = c.post(f"/api/entities/{eid}/evidence/file", json={"filename": "ai-policy.md", "content_b64": b64(
        b"# AI policy\nApproved by the board. Version 3, next review 2027. Prohibited use is listed. Policy owner: CRO.")})
    assert up.status_code == 201
    z = io.BytesIO()
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("svc/requirements.txt", "fairlearn\nshap\nevidently\n")
        zf.writestr("svc/MODEL_CARD.md", "# Model card\nIntended use: credit. Limitations: thin files. Performance: AUC 0.8")
        zf.writestr("../evil.txt", "should not escape")
    r = c.post(f"/api/entities/{eid}/evidence/file", json={"filename": "svc.zip", "content_b64": b64(z.getvalue())})
    assert r.status_code == 201 and len(r.json()["added"]) >= 2
    assert c.post(f"/api/entities/{eid}/evidence", json={"title": "Risk register", "text": "risk register with likelihood and severity"}).status_code == 201
    ev = c.get(f"/api/entities/{eid}/evidence").json()
    repo = next(e for e in ev if e["kind"] == "repository")
    assert repo["signals"]["fairness_lib"] and repo["signals"]["model_card"]

    # tests and answers
    det = c.get(f"/api/entities/{eid}/scope?details=true").json()
    art9 = next(x for x in det["requirements"] if x["id"] == "EUAIA.ART.9")
    assert len(art9["tests"]) == 5
    gov = next(x for x in det["requirements"] if x["id"] == "NIST.GOVERN1.2")
    assert gov["evidence"]["score"] > 0 and gov["evidence"]["doc"] == "ai-policy.md"
    assert c.put(f"/api/entities/{eid}/answers", json=[{"test_id": "EUAIA.ART.9-T1", "answer": "yes", "evidence_ref": "Risk register"}]).status_code == 200
    assert c.put(f"/api/entities/{eid}/answers", json=[{"test_id": "NOPE-T1", "answer": "yes"}]).status_code == 422
    imp = c.post(f"/api/entities/{eid}/answers/import", content="GDPR.ART.35: no\nEUAIA.ART.27: {answer: no, notes: none}\nBAD.ID: yes")
    assert imp.json()["saved"] == 5 and imp.json()["unknown"] == ["BAD.ID"]

    # custom rule appears in the library and is tested
    rule = c.post("/api/rules", json={"framework": "custom", "ref": "POL-7", "title": "Model approval board sign-off",
                                      "tests": ["Does the board sign off each high-risk model?"], "keywords": ["sign-off", "approval board"],
                                      "need": ["high_risk"], "weight": 3, "action": "Introduce board sign-off."}).json()
    assert rule["id"] == "CUSTOM.CUSTOM.POL-7"
    assert c.post("/api/rules", json={"ref": "POL-7", "title": "dup"}).status_code == 409
    assert c.put("/api/rules/EUAIA.ART.9", json={"ref": "x", "title": "y"}).status_code == 404   # built-ins are read-only

    a = c.post(f"/api/entities/{eid}/assessments").json()
    res = {r["id"]: r for r in a["results"]}
    assert res["EUAIA.ART.9"]["tests"][0]["basis"] == "verified"
    assert res["EUAIA.ART.27"]["status"] == "not_applicable"   # FRIA is a deployer duty; this entity is a provider
    assert res["GDPR.ART.35"]["status"] == "gap"
    assert res["CUSTOM.CUSTOM.POL-7"]["status"] == "gap"
    assert any(f["key"] == "custom" for f in a["frameworks"])
    for fmt, needle in (("html", "<!doctype html>"), ("csv", "test_id"), ("md", "# AI Governance"), ("json", '"overall_score"')):
        rep = c.get(f"/api/assessments/{a['id']}/report?format={fmt}")
        assert rep.status_code == 200 and needle in rep.text and "attachment" in rep.headers["content-disposition"]
    assert len(c.get(f"/api/entities/{eid}/assessments").json()) == 1
    assert c.delete(f"/api/rules/{rule['id']}").status_code == 200
    assert c.delete(f"/api/entities/{eid}").status_code == 200
    assert c.get(f"/api/entities/{eid}").status_code == 404


def test_web_rejects_bad_uploads(client):
    eid = client.post("/api/entities", json={"entity": {"name": "X"}}).json()["id"]
    assert client.post(f"/api/entities/{eid}/evidence/file", json={"filename": "a.md", "content_b64": "%%%"}).status_code == 422
    assert client.post(f"/api/entities/{eid}/evidence/file", json={"filename": "a.zip", "content_b64": b64(b"not a zip")}).status_code == 422
    assert client.post(f"/api/entities/{eid}/evidence/file", json={"filename": "a.bin", "content_b64": b64(b"\x00\x01")}).status_code == 422


def test_web_token(tmp_path, monkeypatch):
    monkeypatch.setenv("AIGOV_API_TOKEN", "s3cret")
    c = TestClient(create_app(str(tmp_path / "t.db")))
    assert c.get("/").status_code == 200                       # UI shell loads, then asks for the token
    assert c.get("/api/meta").status_code == 401
    assert c.get("/api/meta", headers={"Authorization": "Bearer s3cret"}).status_code == 200


def test_ui_has_no_external_resources():
    static = Path(__file__).parent.parent / "aigov" / "web" / "static"
    for f in static.iterdir():
        text = f.read_text()
        assert not re.search(r"https?://(?!www\.w3\.org/2000/svg)", text), f"external URL in {f.name}"
