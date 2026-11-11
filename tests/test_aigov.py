import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from aigov.catalog import load_controls, load_frameworks
from aigov.cli import main
from aigov.engine import ai
from aigov.engine.applicability import classify_system
from aigov.engine.assess import priority_for, run_assessment
from aigov.models import AISystem, Entity, Evidence, Profile
from aigov.pipeline import collect_file

EXAMPLE = Path(__file__).parent.parent / "examples" / "acme" / "aigov.yaml"


def by_id(a):
    return {r.control_id: r for r in a.results}


def test_catalog_is_consistent():
    controls, frameworks = load_controls(), load_frameworks()
    assert len(controls) >= 30
    for c in controls:
        assert c.mappings and c.indicators and 1 <= c.weight <= 3
    for key in frameworks:  # every framework is used by at least one control
        assert any(key in c.mappings for c in controls)


def test_risk_classification():
    assert classify_system(AISystem(id="1", name="CV screening for hiring"))[0] == "high"
    assert classify_system(AISystem(id="2", name="Social scoring of citizens"))[0] == "prohibited"
    assert classify_system(AISystem(id="3", name="FAQ chatbot", generative=True))[0] == "limited"
    assert classify_system(AISystem(id="4", name="Warehouse demand forecast"))[0] == "minimal"


def test_scope_follows_jurisdiction_and_flags():
    p = Profile(entity=Entity(name="X", jurisdictions=["US"]), systems=[AISystem(id="1", name="Demand forecast")])
    a = run_assessment(p, [], mode="rules")
    scope = {f.key: f.applicable for f in a.frameworks}
    assert scope["nist_ai_rmf"] and scope["iso_42001"]
    assert not scope["eu_ai_act"] and not scope["gdpr"] and not scope["colorado_ai_act"] and not scope["nyc_ll144"]
    r = by_id(a)
    assert r["RSK-04"].status == "not_applicable"      # high-risk only
    assert r["DAT-03"].status == "not_applicable"      # personal data only
    assert r["GOV-01"].status == "gap" and not r["GOV-01"].legally_binding


def test_example_rules_assessment():
    profile, evidence, att, warnings = collect_file(EXAMPLE)
    a = run_assessment(profile, evidence, att, mode="rules", warnings=warnings)
    r = by_id(a)
    assert all(f.applicable for f in a.frameworks)
    assert r["GOV-01"].status == "met" and r["GOV-01"].citations
    assert r["DAT-03"].status == "partial"             # attested "yes" with no evidence is not "met"
    assert r["DEV-03"].status == "gap" and r["DEV-03"].priority == "critical"
    assert r["OPS-03"].status == "partial"             # plan says AI failures are not yet covered
    assert r["GPA-01"].status == "not_applicable"
    assert any("TalentRank" in w and "high" in w for w in a.warnings)
    assert a.gaps()[0].priority == "critical"
    assert a.roadmap and a.executive_summary
    assert 0 < a.overall_score < 100


def test_priority():
    assert priority_for(3, 0.0, True) == "critical"
    assert priority_for(3, 0.0, False) == "high"
    assert priority_for(1, 0.5, False) == "low"


def test_cli_gate_and_reports(tmp_path):
    assert main(["assess", "-c", str(EXAMPLE), "--mode", "rules", "--out", str(tmp_path)]) == 0
    assert main(["assess", "-c", str(EXAMPLE), "--mode", "rules", "--out", str(tmp_path), "--fail-on", "critical"]) == 2
    assert main(["assess", "-c", str(EXAMPLE), "--mode", "rules", "--out", str(tmp_path), "--fail-under", "90"]) == 2
    assert json.loads((tmp_path / "assessment.json").read_text())["results"]
    assert "<html" in (tmp_path / "assessment.html").read_text()
    assert "## Gaps and recommendations" in (tmp_path / "assessment.md").read_text()


# --------------------------------------------------------------------------- AI path (model call stubbed)
class FakeStream:
    def __init__(self, payload, stop="end_turn"):
        self.payload, self.stop = payload, stop

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def get_final_message(self):
        return SimpleNamespace(stop_reason=self.stop, content=[SimpleNamespace(type="text", text=json.dumps(self.payload))])


def fake_client(calls, fail_domain=None):
    def stream(**kw):
        calls.append(kw)
        task = kw["messages"][0]["content"][1]["text"]
        if "<controls>" not in task:
            return FakeStream({"executive_summary": "Summary.", "roadmap": [{"phase": "Stabilise", "horizon": "0-30 days", "actions": [{"action": "Do X", "owner": "CRO", "control_ids": ["GOV-04"]}]}]})
        specs = json.loads(task.split("<controls>")[1].split("</controls>")[0])
        if fail_domain and any(s["control_id"].startswith(fail_domain) for s in specs):
            return FakeStream({}, stop="refusal")
        return FakeStream({"results": [{
            "control_id": s["control_id"], "status": "partial", "score": 50, "confidence": "medium", "rationale": "Partly evidenced.",
            "gaps": ["Missing record"],
            "citations": [{"source": "doc:ai-policy.md", "quote": "Approved by the Executive   Committee on 14 March 2026"},
                          {"source": "doc:ai-policy.md", "quote": "this sentence is not in the evidence"}],
            "recommendations": [{"action": "Tailored action", "priority": "high", "effort": "low", "owner": "CRO"}],
        } for s in specs]})
    return SimpleNamespace(beta=SimpleNamespace(messages=SimpleNamespace(stream=stream)))


def run_ai(monkeypatch, **kw):
    calls = []
    import anthropic
    monkeypatch.setattr(anthropic, "Anthropic", lambda: fake_client(calls, **kw))
    profile, evidence, att, warnings = collect_file(EXAMPLE)
    return run_assessment(profile, evidence, att, mode="ai", warnings=warnings), calls


def test_ai_assessment(monkeypatch):
    a, calls = run_ai(monkeypatch)
    assert a.mode == "ai" and a.model == ai.DEFAULT_MODEL
    r = by_id(a)["GOV-01"]
    assert r.method == "ai" and r.status == "partial" and r.recommendations[0].action == "Tailored action"
    assert [c.verified for c in r.citations] == [True, False]     # quotes are checked against the evidence
    assert any("could not be matched" in w for w in a.warnings)
    assert a.executive_summary == "Summary." and a.roadmap[0]["phase"] == "Stabilise"
    # request shape: identical cached evidence prefix on every call, schema-constrained output, refusal fallback
    first = calls[0]
    assert first["model"] == "claude-opus-5-5" and first["fallbacks"] == "default"
    assert first["output_config"]["format"]["type"] == "json_schema"
    prefixes = {c["messages"][0]["content"][0]["text"] for c in calls}
    assert len(prefixes) == 1 and "doc:ai-policy.md" in prefixes.pop()
    assert first["messages"][0]["content"][0]["cache_control"] == {"type": "ephemeral"}


def test_ai_batch_failure_falls_back_to_rules(monkeypatch):
    a, _ = run_ai(monkeypatch, fail_domain="OPS")
    r = by_id(a)
    assert r["OPS-01"].method == "rules" and r["GOV-01"].method == "ai"
    assert any("OPS-01" in w and "rule-based result used" in w for w in a.warnings)


def test_evidence_over_budget_is_reported_not_truncated():
    p = Profile(entity=Entity(name="X"))
    ev = [Evidence(id="doc:big", connector="t", kind="document", title="big", text="x" * 5000),
          Evidence(id="doc:small", connector="t", kind="document", title="small", text="ok")]
    bundle, omitted = ai.build_bundle(p, [], ev, budget=1000)
    assert omitted == ["doc:big"] and "doc:small" in bundle and "xxxx" not in bundle


# --------------------------------------------------------------------------- REST API
def test_api(monkeypatch):
    from fastapi.testclient import TestClient

    from aigov.api import app
    monkeypatch.setenv("AIGOV_API_TOKEN", "s3cret")
    c = TestClient(app)
    assert c.get("/frameworks").status_code == 401
    hdr = {"Authorization": "Bearer s3cret"}
    body = {
        "entity": {"name": "Beta", "jurisdictions": ["EU"]},
        "systems": [{"id": "S1", "name": "Resume screening", "uses_personal_data": True}],
        "documents": [{"title": "policy.md", "text": "Our AI policy was approved by the board. Version 1, next review 2027. Prohibited use is listed."}],
        "answers": {"GOV-01": "yes", "GOV-06": False},
        "mode": "rules",
    }
    res = c.post("/assessments", json=body, headers=hdr)
    assert res.status_code == 201
    aid = res.json()["id"]
    gaps = c.get(f"/assessments/{aid}/gaps", headers=hdr).json()
    assert gaps["frameworks"]["eu_ai_act"] is not None and gaps["gaps"]
    assert "<html" in c.get(f"/assessments/{aid}/report", headers=hdr).text
    assert c.get("/assessments/000000000000", headers=hdr).status_code == 404


def test_repo_connector_detects_signals():
    _, evidence, _, _ = collect_file(EXAMPLE)
    sig = next(e for e in evidence if e.kind == "repository").signals
    assert sig["ml_deps"] and sig["explainability_lib"] and sig["experiment_tracking"] and sig["model_card"] and sig["ci"]
    assert not sig["fairness_lib"] and not sig["monitoring_lib"] and sig["hardcoded_secrets"] == 0
