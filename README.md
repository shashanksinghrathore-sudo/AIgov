# aigov

Measures an organisation's AI governance against laws and recognised standards, finds the gaps, and recommends what to fix first.

It plugs into systems you already run (policy folders, code repositories, model registries, GRC tools), gathers evidence, and assesses it against one control catalog that is mapped to every framework, so a single piece of evidence counts everywhere it is required.

> This is a governance diagnostic, not legal advice or a certification. Clause references help you find the source text; confirm applicability, current wording and effective dates with qualified counsel.

## Quick start

```bash
pip install -e ".[all]"
```

```bash
aigov assess -c examples/acme/aigov.yaml --out examples/acme/out
```

Open `examples/acme/out/assessment.html`. The same run also writes `assessment.json` and `assessment.md`.

With Anthropic credentials (`ANTHROPIC_API_KEY`), Claude reads the evidence and judges each control on substance. Without them the tool falls back to an offline rule-based check and says so in the report.

## What it covers

| Framework | Type | In scope when |
|---|---|---|
| EU AI Act (Regulation (EU) 2024/1689) | Binding law | Entity operates in the EU |
| GDPR | Binding law | EU and personal data |
| Colorado AI Act (SB 24-205) | Binding law | Colorado and consequential decisions |
| NYC Local Law 144 | Binding law | New York and employment decisions |
| India DPDP Act 2023 | Binding law | India and personal data |
| NIST AI RMF 1.0 + Generative AI Profile | Voluntary | Always |
| ISO/IEC 42001:2023 | Voluntary | Always |
| OECD AI Principles | Voluntary | Always |

33 controls across nine domains: governance, risk management, data governance, development and documentation, transparency, human oversight, operations and monitoring, third parties, and generative AI safeguards. List them with `aigov controls` or `aigov controls --framework eu_ai_act`.

## How an assessment works

1. **Scope.** Each AI system is screened into a risk tier (prohibited, high, limited, minimal). Jurisdictions and system traits decide which frameworks and controls apply. A declared tier lower than the screening result is flagged.
2. **Collect.** Connectors pull evidence.
3. **Evaluate.** Each control is rated met, partial or gap, with a 0-100 score, the quoted evidence relied on, and specific gaps.
4. **Prioritise.** Priority = control weight x shortfall, raised when binding law requires the control.
5. **Recommend.** Each gap gets actions with an owner and effort, sequenced into a 30/90/180-day roadmap.

### Two evaluators

| | AI-assisted (`--mode ai`) | Rule-based (`--mode rules`) |
|---|---|---|
| Method | Claude reads all evidence as an auditor would | Phrase coverage in documents, technical signals, attestations |
| Judges | Whether the control is designed and operating | Whether the topic is addressed |
| Recommendations | Tailored to the entity and its systems | Catalog defaults |
| Needs | Anthropic credentials | Nothing; runs offline |

Safeguards in AI mode: quotes are re-checked against the source text and marked unverified if not found; evidence that exceeds the size budget is reported as unread, never silently cut; evidence is treated as data, not instructions; a failed batch falls back to rules for those controls and is noted. The model defaults to `claude-opus-5-5` (override with `AIGOV_MODEL`).

In rule-based mode an unsupported "yes" in the questionnaire scores as partial, and documents that describe a control as planned or not yet covering AI cannot score as met.

## Plugging it in

**Config file** (paths are relative to the file):

```yaml
entity: {name: Acme, sector: Finance, jurisdictions: [EU, US-CO, IN]}
inventory: systems.csv            # or list `systems:` inline
connectors:
  - {type: documents, path: ./policies}                  # md, txt, pdf, docx, yaml, json
  - {type: repo, path: ../ml-service}                    # static scan, never runs code
  - {type: questionnaire, path: answers.yaml}            # template: aigov questionnaire
  - {type: mlflow, url: https://mlflow.internal, token_env: MLFLOW_TOKEN}
  - {type: http, url: https://grc.internal/api/risks, title: Risk register, token_env: GRC_TOKEN}
```

| Connector | Pulls |
|---|---|
| `documents` | Policies, procedures, assessments from a folder |
| `repo` | ML/LLM libraries, model cards, datasheets, tests, CI, fairness, explainability, monitoring and guardrail tooling, hard-coded secrets |
| `inventory` | The AI system register and its completeness |
| `questionnaire` | Management self-assessment per control |
| `mlflow` | Registered models and whether each has an owner, description and risk tier |
| `http` | Any JSON or text endpoint (GRC, ticketing, wiki) |

Tokens are read from environment variables named in the config, never stored in it.

**Your own connector:** subclass `Connector`, decorate with `@register("name")`, return `Evidence` items. Packages can also publish connectors through the `aigov.connectors` entry-point group. See `aigov/connectors/base.py`.

**CI gate:** exit code 2 when a threshold is breached. Example workflow in `examples/ci/github-action.yml`.

```bash
aigov assess -c aigov.yaml --fail-on critical --fail-under 60
```

**Webhook:** `--webhook URL` posts a JSON list of prioritised gaps, ready to turn into tickets.

**REST API** for portals and GRC platforms:

```bash
AIGOV_API_TOKEN=change-me aigov serve --port 8080
```

`POST /assessments` with entity, systems, documents and answers; then `GET /assessments/{id}`, `/gaps` or `/report?format=html`. Interactive docs at `/docs`.

## Extending the catalog

Frameworks live in `aigov/catalog/frameworks.yaml` and controls in `aigov/catalog/controls.yaml`. To add a law, add a framework entry with its `applies_when` rule, then add its clause references under `mappings` on the relevant controls. The loader rejects unknown framework keys and duplicate ids.

## Limits to know

- Risk-tier screening is keyword-based and meant to prompt a human decision, not replace one.
- Clause mappings are at article or section level and were written from the published texts; several of these laws are being phased in or amended, so check them before relying on a finding.
- The tool assesses the evidence it is given. Controls that exist but were not supplied as evidence show up as gaps.

## Tests

```bash
python -m pytest
```
