# AI Compliance Platform (aigov)

A self-hosted web platform that tests an organisation's AI governance against AI laws and recognised best practice, article by article, finds the gaps, and recommends what to fix first.

All testing is done by rules defined inside the platform. The server makes no outbound network calls and calls no AI or third-party API. The browser UI is locked to its own server by a Content-Security-Policy. Your data stays in a local SQLite file.

> This is a governance diagnostic, not legal advice or a certification. Article summaries and test questions are paraphrased, not the official text. Confirm applicability, current wording and effective dates against the official sources and with qualified counsel.

## Quick start

```bash
pip install -e ".[docs]"
```

```bash
aigov demo
```

```bash
aigov serve
```

Open http://127.0.0.1:8080. `aigov demo` loads a fictional lender with three AI systems, policy documents, a scanned code repository and some answers, so every page has data on it.

## Put it online for your team

The app is one container with one SQLite file. Anyone with the URL and the access token can use it.
On a public address the server will not start without `AIGOV_API_TOKEN`; visitors enter the token once in the browser.

### Option A: Render (one click, from this GitHub repo)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/shashanksinghrathore-sudo/aigov)

1. Click the button, or go to Render Dashboard > New > Blueprint and pick this repository. Render reads `render.yaml`.
2. Approve the plan. The Blueprint asks for a paid "starter" instance because it attaches a 1 GB persistent disk for the database.
   To try it for free, change `plan: starter` to `plan: free` and delete the `disk:` block, but data is then lost on every restart or redeploy, and free services sleep when idle.
3. When the deploy finishes, open the service's **Environment** tab and copy the generated `AIGOV_API_TOKEN`.
4. Share the `https://aigov-xxxx.onrender.com` URL and the token with your team. Optionally run `aigov demo` from the service's Shell tab to load the example company.

### Option B: any server or cloud with Docker

```bash
docker build -t aigov .
```

```bash
docker run -d -p 8080:8080 -v aigov-data:/data -e AIGOV_API_TOKEN="$(openssl rand -hex 24)" --name aigov aigov
```

Put it behind HTTPS (a reverse proxy such as Caddy or nginx, or your cloud's load balancer) before sharing the address. The token is sent with every request and must not travel over plain HTTP.
The same image runs on Railway, Fly.io, Google Cloud Run, Azure Container Apps or AWS App Runner. The container listens on `$PORT` (default 8080) and keeps its data in `/data`, so mount persistent storage there.

**Sharing model:** everyone with the token sees and edits the same entities. Give each team its own deployment, or keep the token to the people who should see the data. Rotate it by changing `AIGOV_API_TOKEN` and restarting.

## The rule library

Every article or section of each regime is listed. Articles that create obligations for an organisation carry compliance tests. The rest (definitions, duties of authorities, amendments, penalties) are listed as reference only.

| Framework | Type | Articles listed | With tests | Tests |
|---|---|---|---|---|
| EU AI Act, Regulation (EU) 2024/1689 (Art. 1-113 + Annexes I-XIII) | Binding law | 126 | 43 | 90 |
| GDPR, Regulation (EU) 2016/679 (Art. 1-99) | Binding law | 99 | 38 | 51 |
| India DPDP Act 2023 (s. 1-44) | Binding law | 44 | 12 | 21 |
| Colorado AI Act, SB 24-205 (6-1-1701 to 1707) | Binding law | 7 | 4 | 13 |
| NYC Local Law 144 + 6 RCNY 5-300 to 5-304 | Binding law | 11 | 6 | 7 |
| NIST AI RMF 1.0 (all 72 subcategories) | Voluntary | 72 | 72 | 72 |
| ISO/IEC 42001:2023 (clauses 4-10 + Annex A) | Voluntary | 65 | 65 | 65 |
| OECD AI Principles | Voluntary | 10 | 5 | 5 |
| **Total** | | **434** | **245** | **324** |

Each article that carries tests also links to a best-practice control in `aigov/catalog/controls.yaml` (33 controls such as AI inventory, risk management, bias testing and incident response). The control supplies the evidence checks and the default fix. One fix can close many articles: an incident-response procedure, for example, closes EU AI Act Art. 73, GDPR Art. 33-34, DPDP s. 8, NIST MANAGE 4.3 and ISO 42001 A.8.4.

You can add your own rules on the **Rule library** page: national laws, sector rules, internal policies or contract terms. Each custom rule has its own tests, applicability conditions, evidence keywords and remediation. Built-in rules are read-only. To change one permanently, edit the YAML under `aigov/catalog/requirements/`.

## How a test run works

1. **Profile and scope.** Record jurisdictions, entity characteristics and AI systems. Each system is screened for prohibited and high-risk use. Frameworks and articles apply only when their conditions hold. For example, EU AI Act Art. 9 applies to providers of high-risk systems, and Art. 27 applies to deployers that are public bodies or score credit or insurance.
2. **Evidence.** Upload policies and records (md, txt, pdf, docx, json, yaml, csv), paste text, or upload a `.zip` of a code repository. Repositories are scanned statically and never executed. The scan looks for ML and LLM libraries, model cards, datasheets, tests, CI, fairness, explainability, monitoring and guardrail tooling, and hard-coded secrets.
3. **Compliance tests.** Answer each test Yes, Partial, No or N/A, with an optional note and linked evidence. Each article shows what the evidence checks found, including quotes and any caveats such as "not yet covered".
4. **Results.** You get scores per framework, domain and article; gaps ranked critical to low; a 30/90/180-day roadmap; and downloadable reports (HTML, CSV test log, JSON, Markdown). Every run is kept so you can compare over time.

**Scoring rules**

| Test outcome | Score |
|---|---|
| Yes, with linked evidence or evidence the checks found | 100 (verified) |
| Yes, with no evidence, or evidence says it is only planned | 60 (attested) |
| Partial | 50 |
| No | 0 |
| N/A | excluded (keep the justification) |
| Unanswered | evidence-check score x 0.8 |

An article's score is the mean of its tests: met is 75 or more, partial is 35 to 74, and gap is below 35. Gap priority is the article weight x shortfall, raised by 1.5x when a binding law imposes it.

## Plugging into other systems

- **REST API** (interactive docs at `/api/docs`). Systems can create entities, push evidence (`POST /api/entities/{id}/evidence`), bulk-import answers (`POST /api/entities/{id}/answers/import`), run tests (`POST /api/entities/{id}/assessments`) and pull reports. Set `AIGOV_API_TOKEN` to require a bearer token.
- **CLI and CI gate.** `aigov assess -c config.yaml --fail-on critical` exits with code 2 on a breach. Example workflow: `examples/ci/github-action.yml`.
- **Local connectors** (`aigov connectors`): documents folder, repository, inventory CSV/JSON/YAML, and questionnaire. Write your own by subclassing `Connector`. See `aigov/connectors/base.py`.

```bash
aigov questionnaire --framework eu_ai_act --out answers.yaml
```

## Limits to know

- The platform judges your answers and the evidence you give it. Keyword evidence checks show that a topic is addressed, not that a control works, so they only corroborate answers.
- Risk-tier screening is keyword-based and is meant to prompt a human decision.
- Several of these laws are being phased in or amended (EU AI Act dates, Colorado's effective date, DPDP Rules commencement). Check the current position before relying on a finding.
- ISO/IEC 42001 is copyrighted. Its entries are short paraphrases; use a licensed copy for the actual requirements.

## Development

```bash
python -m pytest
```

The suite includes a guard that fails any test that opens a non-local network connection.
