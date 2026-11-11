# AI Governance & Compliance Assessment: Acme Lending (example)

- **Date:** 2026-11-11T18:49:23+00:00
- **Method:** rule-based compliance tests (offline)
- **Jurisdictions:** EU, US-CO, US-NY, IN
- **Overall score:** 38/100 (Level 2 - Developing)
- **Tests answered:** 75 of 286

## Executive summary

Acme Lending (example) scores 38 out of 100 (Level 2 - Developing) across 220 in-scope articles and clauses: 48 met, 70 partly met, 102 gaps. 75 of 286 compliance tests were answered.

Binding law in scope: EU Artificial Intelligence Act 44/100; General Data Protection Regulation 30/100; Colorado Artificial Intelligence Act 32/100; NYC Automated Employment Decision Tools Law 0/100; India Digital Personal Data Protection Act 10/100. 10 critical gap(s) carry direct legal exposure, led by EU Artificial Intelligence Act Art. 27 (Fundamental rights impact assessment for high-risk AI systems), EU Artificial Intelligence Act Art. 43 (Conformity assessment), EU Artificial Intelligence Act Art. 73 (Reporting of serious incidents), General Data Protection Regulation Art. 28 (Processor). Systems screened as high-risk: CreditScore v4, TalentRank.

Weakest areas: Data Governance (14/100) and Transparency & Explainability (16/100). The roadmap groups fixes by control, so a single action closes every article that depends on it.

211 test(s) were not answered and were scored from documentary evidence alone, capped below full marks. Answer them on the Tests page to firm up the result.

## Laws and frameworks

| Framework | Type | Articles in library | In scope | Score | Met | Partial | Gap |
|---|---|---|---|---|---|---|---|
| EU Artificial Intelligence Act | Binding law | 126 (43 with obligations) | 32 | 44 | 6 | 15 | 11 |
| General Data Protection Regulation | Binding law | 99 (38 with obligations) | 27 | 30 | 2 | 10 | 15 |
| Colorado Artificial Intelligence Act | Binding law | 7 (4 with obligations) | 4 | 32 | 0 | 2 | 2 |
| NYC Automated Employment Decision Tools Law | Binding law | 11 (6 with obligations) | 6 | 0 | 0 | 0 | 6 |
| India Digital Personal Data Protection Act | Binding law | 44 (12 with obligations) | 9 | 10 | 0 | 1 | 8 |
| NIST AI Risk Management Framework | Voluntary | 72 (72 with obligations) | 72 | 46 | 22 | 26 | 24 |
| ISO/IEC 42001 AI Management System | Voluntary | 65 (65 with obligations) | 65 | 39 | 18 | 14 | 33 |
| OECD AI Principles | Voluntary | 10 (5 with obligations) | 5 | 30 | 0 | 2 | 3 |

## AI systems

| System | Role | Risk tier | Basis |
|---|---|---|---|
| CreditScore v4 | provider | high | Declared in profile. Screening result: high. Matches high-risk area(s): essential services. |
| TalentRank | deployer | high | Matches high-risk area(s): employment. |
| Ava support assistant | deployer | limited | Declared in profile. Screening result: limited. Interacts with people or generates content; transparency obligations apply. |

## Domain scores

- Data Governance: 14/100
- Development & Technical Documentation: 45/100
- Governance & Accountability: 52/100
- Human Oversight: 29/100
- Operations & Monitoring: 47/100
- Risk Management: 44/100
- Third-Party & Supply Chain: 22/100
- Transparency & Explainability: 16/100

## Gaps by article

### EU Artificial Intelligence Act Art. 27 - Fundamental rights impact assessment for high-risk AI systems

Gap, critical priority, score 0 - binding law

2 of 2 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not in place: Was a FRIA completed before first use, describing the deployer's processes, period and frequency of use, categories of persons affected, specific risks of harm, human oversight measures, and measures if risks materialise (including governance and complaints)? (No FRIA performed for CreditScore)
- Gap: Not in place: Has the market surveillance authority been notified of the results, and is the FRIA updated when relevant elements change? (No FRIA performed for CreditScore)
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### EU Artificial Intelligence Act Art. 43 - Conformity assessment

Gap, critical priority, score 0 - binding law

2 of 2 test(s) answered, 0 verified by evidence. Evidence check 44/100: 'model-risk-procedure.md' addresses 3 of 3 expected elements.

- Gap: Not in place: Has the applicable conformity assessment route been determined and completed for each high-risk system before market placement?
- Gap: Not in place: Does change management trigger a new conformity assessment on substantial modification?
- **Do:** Plan the conformity assessment route for each high-risk system, prepare the declaration of conformity and register the system before placing it on the market. *(owner: Regulatory Affairs / Product Compliance; effort: high)*
- **Do:** Version models and datasets alongside code, require reviewed and approved changes, and define what counts as a substantial modification that re-triggers assessment. *(owner: Engineering Lead / MLOps; effort: low)*
- Evidence [doc:model-risk-procedure.md]: "Change management"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### EU Artificial Intelligence Act Art. 73 - Reporting of serious incidents

Gap, critical priority, score 0 - binding law

2 of 2 test(s) answered, 0 verified by evidence. Evidence check 60/100: 'incident-response.md' addresses 4 of 4 expected elements.

- Gap: Not in place: Does the incident procedure define "serious incident" and the 15-day, 10-day and 2-day reporting deadlines?
- Gap: Not in place: Does it require investigation, risk assessment and corrective action while preserving evidence?
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Extend the incident process to AI harms and malfunctions, with severity criteria, regulator notification deadlines and post-incident review. *(owner: CISO / AI Governance Lead; effort: medium)*
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"
- Evidence [doc:incident-response.md]: "Personal data breaches are reported to the supervisory authority within 72 hours"

### General Data Protection Regulation Art. 28 - Processor

Gap, critical priority, score 0 - binding law

2 of 2 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'ai-policy.md' addresses 2 of 4 expected elements.

- Gap: Not in place: Are AI and cloud vendors processing personal data covered by contracts with the Art. 28(3) terms?
- Gap: Not in place: Do contracts restrict the vendor from using the entity's data to train or improve its own models unless agreed?
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; effort: medium)*
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"

### General Data Protection Regulation Art. 32 - Security of processing

Gap, critical priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Security measures appropriate to the risk protect AI processing - pseudonymisation and encryption, confidentiality, integrity, availability and resilience, restoration, and regular testing - including against AI-specific threats such as model inversion, membership inference and data leakage.
- **Do:** Threat-model each AI system, run adversarial/red-team testing before release, and harden model, data and pipeline access. *(owner: Chief Information Security Officer; effort: medium)*

### India Digital Personal Data Protection Act s. 4 - Grounds for processing personal data

Gap, critical priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Personal data is processed only for a lawful purpose, with the Data Principal's consent or for a legitimate use under section 7.
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*

### NYC Automated Employment Decision Tools Law 20-871(a) - Bias audit before use and published summary

Gap, critical priority, score 0 - binding law

2 of 2 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not in place: Has each AEDT been bias-audited by an independent auditor within the past year? (No bias audit of TalentRank has been commissioned)
- Gap: Not in place: Is a summary of the most recent audit and the distribution date publicly available on the website before use? (No bias audit of TalentRank has been commissioned)
- **Do:** Add group fairness metrics to the evaluation suite, set tolerances, and commission an independent bias audit where the law requires one. *(owner: Head of Data Science; effort: medium)*
- **Do:** Issue advance notices to people subject to AI-assisted decisions and publish the required summaries (for example bias audit results) on your website. *(owner: Legal / HR / Product; effort: low)*

### NYC Automated Employment Decision Tools Law 20-871(b) - Notices to employees and candidates

Gap, critical priority, score 0 - binding law

1 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not in place: Candidates and employees who reside in New York City are notified at least 10 business days before use that an AEDT will be used, of the job qualifications and characteristics it assesses, and that they may request an alternative selection process or accommodation; information on data type, source and retention is made available.
- **Do:** Issue advance notices to people subject to AI-assisted decisions and publish the required summaries (for example bias audit results) on your website. *(owner: Legal / HR / Product; effort: low)*
- **Do:** Provide an appeal channel with human review and a correction route for every consequential AI-assisted decision. *(owner: Customer Operations / HR; effort: low)*

### NYC Automated Employment Decision Tools Law 6 RCNY 5-301 - Bias audit

Gap, critical priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: The bias audit calculates selection rates (or scoring rates) and impact ratios for sex, race/ethnicity and intersectional categories, and reports the number of individuals in unknown categories.
- **Do:** Add group fairness metrics to the evaluation suite, set tolerances, and commission an independent bias audit where the law requires one. *(owner: Head of Data Science; effort: medium)*

### India Digital Personal Data Protection Act s. 8 - General obligations of Data Fiduciary

Gap, critical priority, score 18 - binding law

0 of 5 test(s) answered, 0 verified by evidence. Evidence check 22/100: 'incident-response.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Are Data Processors engaged only under a valid contract, with the Data Fiduciary remaining responsible for their processing?
- Gap: Not answered; evidence is incomplete for: Is personal data used to make decisions affecting a Data Principal complete, accurate and consistent?
- Gap: Not answered; evidence is incomplete for: Are reasonable security safeguards in place to prevent personal data breaches, and are breaches intimated to the Board and each affected Data Principal as prescribed?
- Gap: Not answered; evidence is incomplete for: Is personal data erased (and processors made to erase it) once the purpose is served or consent is withdrawn, unless retention is required by law?
- Gap: Not answered; evidence is incomplete for: Are the business contact details of a DPO or person able to answer questions published, and is an effective grievance redressal mechanism in place?
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*
- **Do:** Threat-model each AI system, run adversarial/red-team testing before release, and harden model, data and pipeline access. *(owner: Chief Information Security Officer; effort: medium)*
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"
- Evidence [doc:incident-response.md]: "Personal data breaches are reported to the supervisory authority within 72 hours"
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."

### Colorado Artificial Intelligence Act 6-1-1704 - Disclosure of an artificial intelligence system to consumer

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: An AI system intended to interact with consumers discloses to each consumer that they are interacting with an AI system, unless it would be obvious to a reasonable person.
- **Do:** Add clear AI-interaction notices at the point of use and label or watermark AI-generated content. *(owner: Product Lead; effort: low)*

### EU Artificial Intelligence Act Art. 47 - EU declaration of conformity

Gap, high priority, score 0 - binding law

1 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not in place: Providers draw up a written, machine-readable, signed EU declaration of conformity for each high-risk system containing the Annex V information, keep it for ten years and keep it up to date.
- **Do:** Plan the conformity assessment route for each high-risk system, prepare the declaration of conformity and register the system before placing it on the market. *(owner: Regulatory Affairs / Product Compliance; effort: high)*

### EU Artificial Intelligence Act Art. 48 - CE marking

Gap, high priority, score 0 - binding law

1 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not in place: CE marking is affixed visibly, legibly and indelibly (digitally for digital-only systems), followed by the notified body's identification number where applicable.
- **Do:** Plan the conformity assessment route for each high-risk system, prepare the declaration of conformity and register the system before placing it on the market. *(owner: Regulatory Affairs / Product Compliance; effort: high)*

### EU Artificial Intelligence Act Art. 50 - Transparency obligations for providers and deployers of certain AI systems

Gap, high priority, score 0 - binding law

0 of 5 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Are people informed that they are interacting with an AI system, unless obvious from context?
- Gap: Not answered and no evidence found for: Are synthetic audio, image, video or text outputs marked in a machine-readable format and detectable as artificially generated?
- Gap: Not answered and no evidence found for: Are deep fakes, and AI-generated text published to inform the public on matters of public interest, disclosed as artificially generated or manipulated (unless under human editorial responsibility)?
- Gap: Not answered and no evidence found for: Are persons exposed to emotion recognition or biometric categorisation informed of its operation?
- Gap: Not answered and no evidence found for: Is the information given clearly and distinguishably at the latest at the first interaction or exposure, meeting accessibility requirements?
- **Do:** Add clear AI-interaction notices at the point of use and label or watermark AI-generated content. *(owner: Product Lead; effort: low)*

### General Data Protection Regulation Art. 12 - Transparent information, communication and modalities for the exercise of the rights of the data subject

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Information and communications are concise, transparent, intelligible and in plain language; rights requests are answered without undue delay and within one month (extendable by two months), free of charge, with identity verified.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*
- **Do:** Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; effort: low)*

### General Data Protection Regulation Art. 14 - Information to be provided where personal data have not been obtained from the data subject

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Where personal data is obtained indirectly (for example third-party or publicly scraped training data), people are informed within a reasonable period (at most one month), including the source; or the disproportionate-effort exemption is assessed and documented with protective measures such as public information.
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*

### General Data Protection Regulation Art. 15 - Right of access by the data subject

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: People can obtain confirmation of processing, a copy of their data, and information on purposes, recipients, retention, source, and the existence and logic of automated decision-making.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*

### General Data Protection Regulation Art. 16 - Right to rectification

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Inaccurate personal data, including in AI-derived profiles and outputs, can be rectified without undue delay and incomplete data completed.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*

### General Data Protection Regulation Art. 17 - Right to erasure ('right to be forgotten')

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Erasure requests are handled where grounds apply, with a documented approach for personal data in training data sets and derived models.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*

### General Data Protection Regulation Art. 21 - Right to object

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: People can object to processing based on legitimate interests or public task (including profiling), processing stops unless compelling grounds are shown, objection to direct marketing is absolute, and the right is presented at the first communication.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*

### General Data Protection Regulation Art. 36 - Prior consultation

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Where a DPIA shows high residual risk that cannot be mitigated, the supervisory authority is consulted before processing.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*
- **Do:** Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; effort: low)*

### General Data Protection Regulation Art. 7 - Conditions for consent

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Where consent is relied on, the controller can demonstrate it, the request is distinguishable and plain, consent is freely given, and withdrawal is as easy as giving it.
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*

### General Data Protection Regulation Art. 88 - Processing in the context of employment

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: AI processing of employee and candidate data complies with national employment data protection rules and collective agreements, including safeguards for human dignity and monitoring at work.
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*
- **Do:** Issue advance notices to people subject to AI-assisted decisions and publish the required summaries (for example bias audit results) on your website. *(owner: Legal / HR / Product; effort: low)*

### India Digital Personal Data Protection Act s. 11 - Right to access information about personal data

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: On request, Data Principals receive a summary of their personal data and processing activities and the identities of other Data Fiduciaries and Processors it was shared with.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*

### India Digital Personal Data Protection Act s. 12 - Right to correction and erasure of personal data

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Data Principals can have personal data corrected, completed, updated and erased.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*

### India Digital Personal Data Protection Act s. 13 - Right of grievance redressal

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Data Principals have a readily available means of grievance redressal, and grievances are answered within the prescribed period before they approach the Board.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*
- **Do:** Provide an appeal channel with human review and a correction route for every consequential AI-assisted decision. *(owner: Customer Operations / HR; effort: low)*

### India Digital Personal Data Protection Act s. 5 - Notice

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Every request for consent is accompanied or preceded by a notice describing the personal data and purpose, how to exercise rights and withdraw consent, and how to complain to the Board, available in English or a language of the Eighth Schedule; notice is also given for data collected before commencement.
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*
- **Do:** Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; effort: low)*

### India Digital Personal Data Protection Act s. 7 - Certain legitimate uses

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Where personal data is processed without consent, the processing falls within a legitimate use listed in section 7 (for example data voluntarily provided for a specified purpose, legal obligations, medical emergencies, employment purposes) and this is documented.
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*

### ISO/IEC 42001 AI Management System 4.1 - Understanding the organization and its context

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: External and internal issues relevant to the organisation's purpose and its AI roles (provider, producer, customer, user) are determined, including climate change where relevant.
- **Do:** Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; effort: low)*

### ISO/IEC 42001 AI Management System 4.2 - Understanding the needs and expectations of interested parties

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Interested parties relevant to the AI management system and their requirements (including legal requirements) are determined.
- **Do:** Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; effort: low)*

### ISO/IEC 42001 AI Management System 6.1.4 - AI system impact assessment

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: A process assesses the potential consequences of AI systems for individuals, groups and societies, and results are documented and considered in risk assessment.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### ISO/IEC 42001 AI Management System 7.2 - Competence

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Necessary competence for people affecting AI performance is determined, ensured through education, training or experience, and evidenced.
- **Do:** Roll out role-based AI literacy training (all staff, operators, developers, leadership) and track completion. *(owner: HR / Learning & Development; effort: low)*

### ISO/IEC 42001 AI Management System 8.4 - AI system impact assessment (operation)

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: AI system impact assessments are performed at planned intervals or when significant changes occur, and results retained.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### ISO/IEC 42001 AI Management System 9.2 - Internal audit

Gap, high priority, score 0

1 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not in place: Internal audits are conducted at planned intervals against an audit programme, by objective auditors, with results reported to management.
- **Do:** Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; effort: medium)*

### ISO/IEC 42001 AI Management System 9.3 - Management review

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Top management reviews the AIMS at planned intervals, considering changes, performance, audit results and improvement opportunities.
- **Do:** Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; effort: medium)*

### ISO/IEC 42001 AI Management System A.4.3 - Data resources

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Information about the data resources used for each AI system is documented.
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*

### ISO/IEC 42001 AI Management System A.5.2 - AI system impact assessment process

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: A process exists to assess potential consequences of AI systems for individuals, groups and societies across the lifecycle.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### ISO/IEC 42001 AI Management System A.5.3 - Documentation of AI system impact assessments

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Impact assessment results are documented and retained for a defined period.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### ISO/IEC 42001 AI Management System A.5.4 - Assessing AI system impact on individuals or groups of individuals

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Impacts on individuals and groups (fairness, rights, safety, privacy) are assessed and documented.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*
- **Do:** Add group fairness metrics to the evaluation suite, set tolerances, and commission an independent bias audit where the law requires one. *(owner: Head of Data Science; effort: medium)*

### ISO/IEC 42001 AI Management System A.7.2 - Data for development and enhancement of AI system

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Data management processes for development and enhancement of AI systems are defined, documented and implemented.
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*

### ISO/IEC 42001 AI Management System A.7.3 - Acquisition of data

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Details about acquisition and selection of data used in AI systems are determined and documented.
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*

### ISO/IEC 42001 AI Management System A.7.5 - Data provenance

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: A process records the provenance of data used in AI systems over the data and system lifecycles.
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*

### ISO/IEC 42001 AI Management System A.8.2 - System documentation and information for users

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Information users need about the AI system is determined and provided.
- **Do:** Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; effort: low)*
- **Do:** Add clear AI-interaction notices at the point of use and label or watermark AI-generated content. *(owner: Product Lead; effort: low)*

### ISO/IEC 42001 AI Management System A.8.3 - External reporting

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Interested parties can report adverse impacts of the AI system.
- **Do:** Provide an appeal channel with human review and a correction route for every consequential AI-assisted decision. *(owner: Customer Operations / HR; effort: low)*

### NIST AI Risk Management Framework GOVERN 1.1 - Legal and regulatory requirements

Gap, high priority, score 0

1 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not in place: Legal and regulatory requirements involving AI are understood, managed, and documented.
- **Do:** Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; effort: low)*

### NIST AI Risk Management Framework GOVERN 1.5 - Monitoring and periodic review

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Ongoing monitoring and periodic review of the risk management process and its outcomes are planned and organizational roles and responsibilities clearly defined, including determining the frequency of periodic review.
- **Do:** Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; effort: medium)*

### NIST AI Risk Management Framework GOVERN 2.2 - AI risk management training

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: The organization's personnel and partners receive AI risk management training to enable them to perform their duties and responsibilities consistent with related policies, procedures, and agreements.
- **Do:** Roll out role-based AI literacy training (all staff, operators, developers, leadership) and track completion. *(owner: HR / Learning & Development; effort: low)*

### NIST AI Risk Management Framework GOVERN 4.2 - Documenting and communicating impacts

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Organizational teams document the risks and potential impacts of the AI technology they design, develop, deploy, evaluate, and use, and they communicate about the impacts more broadly.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### NIST AI Risk Management Framework GOVERN 6.2 - Third-party contingency

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Contingency processes are in place to handle failures or incidents in third-party data or AI systems deemed to be high-risk.
- **Do:** Pin and record vendor model versions, re-run your evaluation suite on every model change, and define a fallback for vendor outage or withdrawal. *(owner: Engineering Lead; effort: low)*

### NIST AI Risk Management Framework MANAGE 3.2 - Pre-trained model monitoring

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Pre-trained models which are used for development are monitored as part of AI system regular monitoring and maintenance.
- **Do:** Pin and record vendor model versions, re-run your evaluation suite on every model change, and define a fallback for vendor outage or withdrawal. *(owner: Engineering Lead; effort: low)*

### NIST AI Risk Management Framework MAP 3.2 - Costs of errors documented

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Potential costs, including non-monetary costs, which result from expected or realized AI errors or system functionality and trustworthiness are examined and documented.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### NIST AI Risk Management Framework MAP 3.4 - Operator proficiency

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Processes for operator and practitioner proficiency with AI system performance and trustworthiness, and relevant technical standards and certifications, are defined, assessed, and documented.
- **Do:** Roll out role-based AI literacy training (all staff, operators, developers, leadership) and track completion. *(owner: HR / Learning & Development; effort: low)*

### NIST AI Risk Management Framework MAP 4.2 - Internal risk controls for components

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Internal risk controls for components of the AI system, including third-party AI technologies, are identified and documented.
- **Do:** Pin and record vendor model versions, re-run your evaluation suite on every model change, and define a fallback for vendor outage or withdrawal. *(owner: Engineering Lead; effort: low)*

### NIST AI Risk Management Framework MEASURE 1.3 - Independent assessment

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Internal experts who did not serve as front-line developers for the system and/or independent assessors are involved in regular assessments and updates.
- **Do:** Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; effort: medium)*

### NIST AI Risk Management Framework MEASURE 2.10 - Privacy risk

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Privacy risk of the AI system is examined and documented.
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*

### NIST AI Risk Management Framework MEASURE 2.11 - Fairness and bias

Gap, high priority, score 0

1 of 1 test(s) answered, 0 verified by evidence. Evidence check 12/100: 'incident-response.md' addresses 1 of 3 expected elements.

- Gap: Not in place: Fairness and bias are evaluated and results are documented.
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Add group fairness metrics to the evaluation suite, set tolerances, and commission an independent bias audit where the law requires one. *(owner: Head of Data Science; effort: medium)*
- **Do:** Add a bias examination step to data preparation covering protected groups and proxies, and document findings and mitigations. *(owner: Head of Data Science; effort: medium)*
- Evidence [doc:incident-response.md]: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."

### NIST AI Risk Management Framework MEASURE 2.7 - Security and resilience

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: AI system security and resilience are evaluated and documented.
- **Do:** Threat-model each AI system, run adversarial/red-team testing before release, and harden model, data and pipeline access. *(owner: Chief Information Security Officer; effort: medium)*

### NIST AI Risk Management Framework MEASURE 3.3 - User feedback and appeal

Gap, high priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Feedback processes for end users and impacted communities to report problems and appeal system outcomes are established and integrated into AI system evaluation metrics.
- **Do:** Provide an appeal channel with human review and a correction route for every consequential AI-assisted decision. *(owner: Customer Operations / HR; effort: low)*

### NYC Automated Employment Decision Tools Law 6 RCNY 5-302 - Data requirements

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: The bias audit uses historical data of the AEDT, or test data where historical data is insufficient, with an explanation of why test data was used and how it was generated.
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*
- **Do:** Add group fairness metrics to the evaluation suite, set tolerances, and commission an independent bias audit where the law requires one. *(owner: Head of Data Science; effort: medium)*

### NYC Automated Employment Decision Tools Law 6 RCNY 5-303 - Published results

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: The published summary includes the audit date, data source and explanation, number of individuals assessed and in unknown categories, selection or scoring rates and impact ratios for all categories, and the distribution date, and stays posted for at least six months after last use.
- **Do:** Issue advance notices to people subject to AI-assisted decisions and publish the required summaries (for example bias audit results) on your website. *(owner: Legal / HR / Product; effort: low)*

### NYC Automated Employment Decision Tools Law 6 RCNY 5-304 - Notice to candidates and employees

Gap, high priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Notice is given through the website, job posting, mail or email as permitted by the rules, with instructions for requesting an alternative selection process or reasonable accommodation.
- **Do:** Issue advance notices to people subject to AI-assisted decisions and publish the required summaries (for example bias audit results) on your website. *(owner: Legal / HR / Product; effort: low)*

### OECD AI Principles 1.2 - Respect for the rule of law, human rights and democratic values, including fairness and privacy

Gap, high priority, score 9

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 11/100: 'ai-policy.md' addresses 1 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Safeguards respect human rights, non-discrimination, privacy and fairness, with human agency and oversight appropriate to the context.
- **Do:** Add group fairness metrics to the evaluation suite, set tolerances, and commission an independent bias audit where the law requires one. *(owner: Head of Data Science; effort: medium)*
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*
- Evidence [doc:ai-policy.md]: "Human oversight is required for any decision that affects a customer's access to credit."

### ISO/IEC 42001 AI Management System A.7.4 - Quality of data for AI systems

Gap, high priority, score 10

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 12/100: 'incident-response.md' addresses 1 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Data quality requirements are defined, documented and met by data used to develop and operate AI systems.
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*
- **Do:** Add a bias examination step to data preparation covering protected groups and proxies, and document findings and mitigations. *(owner: Head of Data Science; effort: medium)*
- Evidence [doc:incident-response.md]: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."

### NIST AI Risk Management Framework MANAGE 2.4 - Disengage or deactivate

Gap, high priority, score 14

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 17/100: 'ai-policy.md' addresses 1 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with intended use.
- **Do:** Define the oversight model for each system (who reviews what, when), build override and stop mechanisms, and train reviewers on automation bias. *(owner: System Owner / Operations Lead; effort: medium)*
- **Do:** Define suspension and decommissioning criteria and a retirement procedure covering model, data and user communication. *(owner: System Owner; effort: low)*
- Evidence [doc:ai-policy.md]: "Human oversight is required for any decision that affects a customer's access to credit."

### EU Artificial Intelligence Act Art. 20 - Corrective actions and duty of information

Gap, high priority, score 24 - binding law

0 of 2 test(s) answered, 0 verified by evidence. Evidence check 30/100: 'incident-response.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Is there a procedure to correct, withdraw, disable or recall a non-conforming high-risk system without delay?
- Gap: Not answered; evidence is incomplete for: Does the procedure require informing the value chain and, where a risk exists, the competent authorities and notified body?
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Define suspension and decommissioning criteria and a retirement procedure covering model, data and user communication. *(owner: System Owner; effort: low)*
- **Do:** Extend the incident process to AI harms and malfunctions, with severity criteria, regulator notification deadlines and post-incident review. *(owner: CISO / AI Governance Lead; effort: medium)*
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"
- Evidence [doc:incident-response.md]: "Personal data breaches are reported to the supervisory authority within 72 hours"

### ISO/IEC 42001 AI Management System A.6.2.4 - AI system verification and validation

Gap, high priority, score 25

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 31/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Verification and validation measures and their criteria are defined and documented.
- **Do:** Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; effort: medium)*
- **Do:** Add group fairness metrics to the evaluation suite, set tolerances, and commission an independent bias audit where the law requires one. *(owner: Head of Data Science; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Validation"
- Evidence [doc:model-risk-procedure.md]: "The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set)"

### OECD AI Principles 1.4 - Robustness, security and safety

Gap, high priority, score 25

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 31/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: AI systems are robust, secure and safe throughout their lifecycle, with mechanisms to override, repair or decommission them if they risk undue harm.
- **Do:** Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; effort: medium)*
- **Do:** Threat-model each AI system, run adversarial/red-team testing before release, and harden model, data and pipeline access. *(owner: Chief Information Security Officer; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Validation"
- Evidence [doc:model-risk-procedure.md]: "The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set)"

### EU Artificial Intelligence Act Art. 16 - Obligations of providers of high-risk AI systems

Gap, high priority, score 26 - binding law

0 of 2 test(s) answered, 0 verified by evidence. Evidence check 33/100: 'repo/MODEL_CARD.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Is the provider's name, registered trade name or trademark and contact address indicated on the system, its packaging or documentation?
- Gap: Not answered; evidence is incomplete for: Is there a tracked plan showing each provider obligation (QMS, documentation, logs, conformity assessment, declaration, CE marking, registration, corrective action, accessibility) is met for every high-risk system?
- **Do:** Plan the conformity assessment route for each high-risk system, prepare the declaration of conformity and register the system before placing it on the market. *(owner: Regulatory Affairs / Product Compliance; effort: high)*
- **Do:** Create a model/system card for each AI system covering intended purpose, architecture, data, metrics and limitations, and keep it under version control with the code. *(owner: Engineering Lead; effort: medium)*
- Evidence [repo:repo/MODEL_CARD.md]: "Model card: CreditScore v4"
- Evidence [repo:repo/MODEL_CARD.md]: "Intended use:** decision support for consumer loan applications in the EU and US"

### NIST AI Risk Management Framework MAP 3.5 - Human oversight processes

Gap, high priority, score 26

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 33/100: 'ai-policy.md' addresses 1 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Processes for human oversight are defined, assessed, and documented in accordance with organizational policies.
- **Do:** Define the oversight model for each system (who reviews what, when), build override and stop mechanisms, and train reviewers on automation bias. *(owner: System Owner / Operations Lead; effort: medium)*
- Evidence [doc:ai-policy.md]: "Human oversight is required for any decision that affects a customer's access to credit."

### ISO/IEC 42001 AI Management System A.6.2.6 - AI system operation and monitoring

Gap, high priority, score 30

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 38/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Elements needed for ongoing operation (monitoring, repairs, updates, support) are defined and documented.
- **Do:** Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; effort: medium)*
- **Do:** Define suspension and decommissioning criteria and a retirement procedure covering model, data and user communication. *(owner: System Owner; effort: low)*
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### Colorado Artificial Intelligence Act 6-1-1702 - Developer duty to avoid algorithmic discrimination - required documentation

Gap, high priority, score 32 - binding law

0 of 4 test(s) answered, 0 verified by evidence. Evidence check 40/100: 'repo/MODEL_CARD.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Do deployers receive a general statement of foreseeable uses and known harmful uses, a summary of training data, known limitations, purpose and intended benefits?
- Gap: Not answered; evidence is incomplete for: Do deployers receive documentation of how the system was evaluated for performance and algorithmic discrimination, data governance measures, mitigation measures, and how it should be used and monitored?
- Gap: Not answered; evidence is incomplete for: Is a public statement on the website summarising the high-risk systems developed and how algorithmic discrimination risks are managed, kept current?
- Gap: Not answered; evidence is incomplete for: Are known or reasonably foreseeable risks of algorithmic discrimination disclosed to the Attorney General and known deployers within 90 days of discovery?
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Create a model/system card for each AI system covering intended purpose, architecture, data, metrics and limitations, and keep it under version control with the code. *(owner: Engineering Lead; effort: medium)*
- **Do:** Add group fairness metrics to the evaluation suite, set tolerances, and commission an independent bias audit where the law requires one. *(owner: Head of Data Science; effort: medium)*
- Evidence [repo:repo/MODEL_CARD.md]: "Model card: CreditScore v4"
- Evidence [repo:repo/MODEL_CARD.md]: "Intended use:** decision support for consumer loan applications in the EU and US"
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"

### EU Artificial Intelligence Act Art. 12 - Record-keeping

Gap, high priority, score 32 - binding law

0 of 2 test(s) answered, 0 verified by evidence. Evidence check 40/100: Technical signals present: logging_usage.

- Gap: Not answered; evidence is incomplete for: Does each high-risk system automatically log events relevant to identifying risk situations and substantial modifications, post-market monitoring and deployer monitoring?
- Gap: Not answered; evidence is incomplete for: For remote biometric identification systems, do logs record period of use, reference database, input data matched and the persons verifying results?
- **Do:** Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; effort: medium)*

### EU Artificial Intelligence Act Art. 19 - Automatically generated logs

Gap, high priority, score 32 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 40/100: Technical signals present: logging_usage.

- Gap: Not answered; evidence is incomplete for: Providers keep the automatically generated logs under their control for a period appropriate to the intended purpose, of at least six months unless other law provides otherwise.
- **Do:** Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; effort: medium)*

### General Data Protection Regulation Art. 25 - Data protection by design and by default

Partial, high priority, score 35 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 44/100: 'model-risk-procedure.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Data protection principles are built into the design of AI systems (for example pseudonymisation, minimisation, access limits), and by default only data necessary for each purpose is processed.
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*
- **Do:** Version models and datasets alongside code, require reviewed and approved changes, and define what counts as a substantial modification that re-triggers assessment. *(owner: Engineering Lead / MLOps; effort: low)*
- Evidence [doc:model-risk-procedure.md]: "Change management"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### EU Artificial Intelligence Act Art. 15 - Accuracy, robustness and cybersecurity

Partial, high priority, score 37 - binding law

0 of 3 test(s) answered, 0 verified by evidence. Evidence check 46/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Are accuracy levels and metrics declared in the instructions for use and verified by testing?
- Gap: Not answered; evidence is incomplete for: Is the system resilient to errors, faults and inconsistencies (technical redundancy, fail-safe plans), and are feedback loops in continuously learning systems mitigated?
- Gap: Not answered; evidence is incomplete for: Is the system protected against AI-specific attacks such as data poisoning, model poisoning, adversarial examples, model evasion and confidentiality attacks?
- **Do:** Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; effort: medium)*
- **Do:** Threat-model each AI system, run adversarial/red-team testing before release, and harden model, data and pipeline access. *(owner: Chief Information Security Officer; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Validation"
- Evidence [doc:model-risk-procedure.md]: "The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set)"

### Colorado Artificial Intelligence Act 6-1-1703 - Deployer duty to avoid algorithmic discrimination - risk management policy and program

Partial, high priority, score 50 - binding law

7 of 7 test(s) answered, 0 verified by evidence. Evidence check 43/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Partly in place: Is there a risk management policy and programme for high-risk systems, reasonable in light of a recognised framework such as NIST AI RMF or ISO/IEC 42001?
- Gap: Partly in place: Is an impact assessment completed for each high-risk system, annually and within 90 days of any intentional and substantial modification?
- Gap: Partly in place: Is each deployed high-risk system reviewed at least annually to ensure it is not causing algorithmic discrimination?
- Gap: Partly in place: Are consumers notified before a consequential decision that a high-risk system is used, with its purpose and nature of the decision?
- Gap: Partly in place: For adverse decisions, do consumers receive the principal reasons, an opportunity to correct incorrect personal data, and an opportunity to appeal with human review where technically feasible?
- Gap: Partly in place: Is a public website statement maintained on the types of high-risk systems deployed, risk management, and the information collected and used?
- Gap: Partly in place: Is discovered algorithmic discrimination disclosed to the Attorney General within 90 days?
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Implement an AI risk management procedure with a risk register per system, defined scoring, treatment plans, residual-risk sign-off and re-assessment triggers. *(owner: Chief Risk Officer; effort: medium)*
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Model Risk Management Procedure (Credit Models)"
- Evidence [doc:model-risk-procedure.md]: "Each credit model has an entry in the model risk register with likelihood and severity ratings, mitigation actions and a control owner"
- Evidence [repo:repo/MODEL_CARD.md]: "Explanations:** SHAP values provide the main factors behind each score for the applicant-facing reason codes."

### EU Artificial Intelligence Act Art. 10 - Data and data governance

Partial, high priority, score 50 - binding law

4 of 4 test(s) answered, 0 verified by evidence. Evidence check 8/100: 'incident-response.md' addresses 1 of 3 expected elements.

- Gap: Partly in place: Do documented data governance practices cover design choices, data collection and origin, preparation (annotation, labelling, cleaning), assumptions, and an assessment of availability and suitability?
- Gap: Partly in place: Are data sets examined for possible biases likely to affect health, safety or fundamental rights or lead to discrimination, with measures to detect, prevent and mitigate them?
- Gap: Partly in place: Are data sets relevant, sufficiently representative, as free of errors and complete as possible, and do they reflect the geographical, contextual and behavioural setting of use?
- Gap: Partly in place: Where special-category personal data is processed for bias detection, are the strict Art. 10(5) conditions and safeguards met and documented?
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*
- **Do:** Add a bias examination step to data preparation covering protected groups and proxies, and document findings and mitigations. *(owner: Head of Data Science; effort: medium)*
- Evidence [doc:incident-response.md]: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."

### EU Artificial Intelligence Act Art. 14 - Human oversight

Partial, high priority, score 50 - binding law

4 of 4 test(s) answered, 0 verified by evidence. Evidence check 33/100: 'ai-policy.md' addresses 1 of 3 expected elements.

- Gap: Partly in place: Are oversight measures identified and either built into the system or specified for the deployer to implement?
- Gap: Partly in place: Can overseers understand capacities and limitations, detect anomalies, stay aware of automation bias, and correctly interpret output?
- Gap: Partly in place: Can overseers decide not to use the system, disregard, override or reverse output, and interrupt it through a stop procedure that brings it to a safe state?
- Gap: Partly in place: For Annex III point 1(a) biometric identification, is any action based on the result verified by at least two competent persons?
- **Do:** Define the oversight model for each system (who reviews what, when), build override and stop mechanisms, and train reviewers on automation bias. *(owner: System Owner / Operations Lead; effort: medium)*
- Evidence [doc:ai-policy.md]: "Human oversight is required for any decision that affects a customer's access to credit."

### EU Artificial Intelligence Act Art. 17 - Quality management system

Partial, high priority, score 50 - binding law

3 of 3 test(s) answered, 0 verified by evidence. Evidence check 66/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Partly in place: Does the QMS cover a regulatory compliance strategy (including management of modifications), design and development control, quality assurance, and test and validation procedures?
- Gap: Partly in place: Does it cover technical specifications and standards, data management, risk management, post-market monitoring, serious incident reporting, and communication with authorities and customers?
- Gap: Partly in place: Does it cover record-keeping, resource management (including security of supply) and an accountability framework defining management and staff responsibilities?
- **Do:** Draft and adopt an AI policy covering scope, principles, risk appetite, prohibited uses and review cadence; obtain executive or board approval. *(owner: Chief Risk Officer / AI Governance Lead; effort: medium)*
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"
- Evidence [doc:ai-policy.md]: "Approved by the Executive Committee on 14 March 2026"
- Evidence [doc:model-risk-procedure.md]: "Change management"

### EU Artificial Intelligence Act Art. 26 - Obligations of deployers of high-risk AI systems

Partial, high priority, score 50 - binding law

7 of 7 test(s) answered, 0 verified by evidence. Evidence check 42/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Partly in place: Are technical and organisational measures in place to use each high-risk system in accordance with its instructions for use?
- Gap: Partly in place: Is human oversight assigned to persons with the necessary competence, training, authority and support?
- Gap: Partly in place: Where the deployer controls input data, is it relevant and sufficiently representative for the intended purpose?
- Gap: Partly in place: Is operation monitored, with the provider and authorities informed and use suspended where a risk or serious incident arises?
- Gap: Partly in place: Are logs under the deployer's control kept for at least six months?
- Gap: Partly in place: Before workplace use, are workers' representatives and affected workers informed?
- Gap: Partly in place: Are natural persons subject to Annex III decisions informed that a high-risk AI system is used?
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Define the oversight model for each system (who reviews what, when), build override and stop mechanisms, and train reviewers on automation bias. *(owner: System Owner / Operations Lead; effort: medium)*
- **Do:** Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"

### General Data Protection Regulation Art. 22 - Automated individual decision-making, including profiling

Partial, high priority, score 50 - binding law

4 of 4 test(s) answered, 0 verified by evidence. Evidence check 33/100: 'repo/MODEL_CARD.md' addresses 3 of 3 expected elements.

- Gap: Partly in place: Has the entity identified every decision based solely on automated processing with legal or similarly significant effects?
- Gap: Partly in place: Does each such decision rely on an Art. 22(2) exception (contract necessity, authorised by law, or explicit consent)?
- Gap: Partly in place: Can people obtain human intervention, express their point of view and contest the decision?
- Gap: Partly in place: Is special-category data excluded unless Art. 9(2)(a) or (g) applies with safeguards?
- **Do:** Provide an appeal channel with human review and a correction route for every consequential AI-assisted decision. *(owner: Customer Operations / HR; effort: low)*
- **Do:** Implement explanation methods suited to each model and a process to give affected individuals the main reasons for a decision. *(owner: Head of Data Science / Product Lead; effort: medium)*
- Evidence [repo:repo/MODEL_CARD.md]: "Explanations:** SHAP values provide the main factors behind each score for the applicant-facing reason codes."
- Evidence [repo:repo/MODEL_CARD.md]: "Intended use:** decision support for consumer loan applications in the EU and US"

### General Data Protection Regulation Art. 35 - Data protection impact assessment

Partial, high priority, score 50 - binding law

3 of 3 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Partly in place: Has a DPIA been completed before go-live for each AI processing likely to result in high risk? (DPIA exists for CreditScore; none for TalentRank or Ava)
- Gap: Partly in place: Does it contain a description of processing, necessity and proportionality, risks to rights and freedoms, and mitigating measures? (DPIA exists for CreditScore; none for TalentRank or Ava)
- Gap: Partly in place: Was the DPO's advice sought, and is the DPIA reviewed when the processing or risk changes? (DPIA exists for CreditScore; none for TalentRank or Ava)
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### India Digital Personal Data Protection Act s. 6 - Consent

Partial, high priority, score 50 - binding law

3 of 3 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Partly in place: Is consent for AI processing obtained through a clear affirmative action, limited to necessary data, and specific to the purpose?
- Gap: Partly in place: Can consent be withdrawn as easily as given, with processing (including by processors) stopped within a reasonable time?
- Gap: Partly in place: Can the Data Fiduciary prove the notice given and consent obtained?
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*

### General Data Protection Regulation Art. 18 - Right to restriction of processing

Gap, medium priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Processing can be restricted (for example while accuracy is contested), and restricted data is marked and not used for AI processing.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*

### General Data Protection Regulation Art. 20 - Right to data portability

Gap, medium priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Where processing is automated and based on consent or contract, people can receive their data in a structured, commonly used, machine-readable format and transmit it to another controller.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*

### General Data Protection Regulation Art. 31 - Cooperation with the supervisory authority

Gap, medium priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: The controller and processor cooperate with the supervisory authority on request.
- **Do:** Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; effort: low)*

### India Digital Personal Data Protection Act s. 14 - Right to nominate

Gap, medium priority, score 0 - binding law

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Data Principals can nominate another individual to exercise their rights in the event of death or incapacity.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*

### ISO/IEC 42001 AI Management System 10.1 - Continual improvement

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: The suitability, adequacy and effectiveness of the AIMS are continually improved.
- **Do:** Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; effort: medium)*

### ISO/IEC 42001 AI Management System 7.3 - Awareness

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: People are aware of the AI policy, their contribution to the AIMS and the implications of not conforming.
- **Do:** Roll out role-based AI literacy training (all staff, operators, developers, leadership) and track completion. *(owner: HR / Learning & Development; effort: low)*

### ISO/IEC 42001 AI Management System 7.4 - Communication

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Internal and external communications relevant to the AIMS (what, when, with whom, how) are determined.
- **Do:** Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; effort: low)*

### ISO/IEC 42001 AI Management System A.10.4 - Customers

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: The organisation's responsible approach to AI takes customers' expectations and needs into account.
- **Do:** Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; effort: low)*

### ISO/IEC 42001 AI Management System A.4.5 - System and computing resources

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Information about system and computing resources used by AI systems is documented.
- **Do:** Threat-model each AI system, run adversarial/red-team testing before release, and harden model, data and pipeline access. *(owner: Chief Information Security Officer; effort: medium)*

### ISO/IEC 42001 AI Management System A.4.6 - Human resources

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Information about the human resources and competences used for AI systems is documented.
- **Do:** Roll out role-based AI literacy training (all staff, operators, developers, leadership) and track completion. *(owner: HR / Learning & Development; effort: low)*

### ISO/IEC 42001 AI Management System A.5.5 - Assessing societal impacts of AI systems

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Potential societal impacts are assessed and documented.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### ISO/IEC 42001 AI Management System A.7.6 - Data preparation

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Criteria for selecting data preparations and the methods used are defined and documented.
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*

### ISO/IEC 42001 AI Management System A.8.5 - Information for interested parties

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Obligations to report information about AI systems to interested parties (including authorities) are determined and documented.
- **Do:** Issue advance notices to people subject to AI-assisted decisions and publish the required summaries (for example bias audit results) on your website. *(owner: Legal / HR / Product; effort: low)*
- **Do:** Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; effort: low)*

### NIST AI Risk Management Framework GOVERN 1.7 - Decommissioning

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Processes and procedures are in place for decommissioning and phasing out AI systems safely and in a manner that does not increase risks or decrease the organization's trustworthiness.
- **Do:** Define suspension and decommissioning criteria and a retirement procedure covering model, data and user communication. *(owner: System Owner; effort: low)*

### NIST AI Risk Management Framework MAP 3.1 - Benefits documented

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Potential benefits of intended AI system functionality and performance are examined and documented.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### NIST AI Risk Management Framework MAP 5.2 - Engagement with affected actors

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Practices and personnel for supporting regular engagement with relevant AI actors and integrating feedback about positive, negative, and unanticipated impacts are in place and documented.
- **Do:** Provide an appeal channel with human review and a correction route for every consequential AI-assisted decision. *(owner: Customer Operations / HR; effort: low)*

### NIST AI Risk Management Framework MEASURE 2.13 - Effectiveness of TEVV

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: Effectiveness of the employed TEVV metrics and processes in the MEASURE function are evaluated and documented.
- **Do:** Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; effort: medium)*

### OECD AI Principles 1.1 - Inclusive growth, sustainable development and well-being

Gap, medium priority, score 0

0 of 1 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Not answered and no evidence found for: AI is used to pursue beneficial outcomes for people and the planet, reducing inequalities and protecting natural environments.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### ISO/IEC 42001 AI Management System A.9.4 - Intended use of the AI system

Gap, medium priority, score 14

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 17/100: 'ai-policy.md' addresses 1 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: AI systems are used according to their intended uses and accompanying documentation.
- **Do:** Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; effort: low)*
- **Do:** Define the oversight model for each system (who reviews what, when), build override and stop mechanisms, and train reviewers on automation bias. *(owner: System Owner / Operations Lead; effort: medium)*
- Evidence [doc:ai-policy.md]: "Human oversight is required for any decision that affects a customer's access to credit."

### EU Artificial Intelligence Act Art. 21 - Cooperation with competent authorities

Gap, medium priority, score 16 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 20/100: Technical signals present: logging_usage.

- Gap: Not answered; evidence is incomplete for: On a reasoned request, providers give competent authorities all information and documentation needed to demonstrate conformity, in an easily understood language, and access to logs under their control.
- **Do:** Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; effort: low)*
- **Do:** Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; effort: medium)*

### NIST AI Risk Management Framework MEASURE 2.8 - Transparency and accountability risks

Gap, medium priority, score 16

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 20/100: Technical signals present: logging_usage.

- Gap: Not answered; evidence is incomplete for: Risks associated with transparency and accountability are examined and documented.
- **Do:** Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; effort: low)*
- **Do:** Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; effort: medium)*

### General Data Protection Regulation Art. 19 - Notification obligation regarding rectification or erasure of personal data or restriction of processing

Gap, medium priority, score 20 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 25/100: 'ai-policy.md' addresses 2 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Rectification, erasure or restriction is communicated to each recipient of the data unless impossible or disproportionate.
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*
- **Do:** Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; effort: medium)*
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"

### ISO/IEC 42001 AI Management System A.10.3 - Suppliers

Gap, medium priority, score 20

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 25/100: 'ai-policy.md' addresses 2 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: A process ensures that services, products or materials from suppliers align with the organisation's approach to responsible AI.
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; effort: medium)*
- **Do:** Pin and record vendor model versions, re-run your evaluation suite on every model change, and define a fallback for vendor outage or withdrawal. *(owner: Engineering Lead; effort: low)*
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"

### NIST AI Risk Management Framework MANAGE 3.1 - Third-party risk monitoring

Gap, medium priority, score 20

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 25/100: 'ai-policy.md' addresses 2 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: AI risks and benefits from third-party resources are regularly monitored, and risk controls are applied and documented.
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; effort: medium)*
- **Do:** Pin and record vendor model versions, re-run your evaluation suite on every model change, and define a fallback for vendor outage or withdrawal. *(owner: Engineering Lead; effort: low)*
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"

### ISO/IEC 42001 AI Management System 10.2 - Nonconformity and corrective action

Gap, medium priority, score 24

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 30/100: 'incident-response.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Nonconformities are reacted to, causes analysed, corrective actions taken and their effectiveness reviewed, with evidence retained.
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; effort: medium)*
- **Do:** Extend the incident process to AI harms and malfunctions, with severity criteria, regulator notification deadlines and post-incident review. *(owner: CISO / AI Governance Lead; effort: medium)*
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"
- Evidence [doc:incident-response.md]: "Personal data breaches are reported to the supervisory authority within 72 hours"

### NIST AI Risk Management Framework GOVERN 3.2 - Human-AI configurations and oversight roles

Gap, medium priority, score 26

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 33/100: 'ai-policy.md' addresses 1 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Policies and procedures are in place to define and differentiate roles and responsibilities for human-AI configurations and oversight of AI systems.
- **Do:** Define the oversight model for each system (who reviews what, when), build override and stop mechanisms, and train reviewers on automation bias. *(owner: System Owner / Operations Lead; effort: medium)*
- Evidence [doc:ai-policy.md]: "Human oversight is required for any decision that affects a customer's access to credit."

### ISO/IEC 42001 AI Management System 9.1 - Monitoring, measurement, analysis and evaluation

Gap, medium priority, score 30

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 38/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: What is monitored and measured, methods, timing and evaluation of AIMS performance and effectiveness are determined and evidenced.
- **Do:** Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; effort: medium)*
- **Do:** Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### NIST AI Risk Management Framework GOVERN 5.1 - External feedback

Gap, medium priority, score 30

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 38/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Organizational policies and practices are in place to collect, consider, prioritize, and integrate feedback from those external to the team that developed or deployed the AI system regarding the potential individual and societal impacts related to AI risks.
- **Do:** Provide an appeal channel with human review and a correction route for every consequential AI-assisted decision. *(owner: Customer Operations / HR; effort: low)*
- **Do:** Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### ISO/IEC 42001 AI Management System A.6.2.8 - AI system recording of event logs

Gap, medium priority, score 32

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 40/100: Technical signals present: logging_usage.

- Gap: Not answered; evidence is incomplete for: The lifecycle phases in which event logging is enabled are determined, at a minimum while the system is in use.
- **Do:** Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; effort: medium)*

### ISO/IEC 42001 AI Management System A.6.2.5 - AI system deployment

Partial, medium priority, score 35

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 44/100: 'model-risk-procedure.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: A deployment plan is documented and requirements are met before deployment.
- **Do:** Version models and datasets alongside code, require reviewed and approved changes, and define what counts as a substantial modification that re-triggers assessment. *(owner: Engineering Lead / MLOps; effort: low)*
- **Do:** Plan the conformity assessment route for each high-risk system, prepare the declaration of conformity and register the system before placing it on the market. *(owner: Regulatory Affairs / Product Compliance; effort: high)*
- Evidence [doc:model-risk-procedure.md]: "Change management"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### ISO/IEC 42001 AI Management System A.9.2 - Processes for responsible use of AI systems

Partial, medium priority, score 37

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 46/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Processes for the responsible use of AI systems are defined and documented.
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Define the oversight model for each system (who reviews what, when), build override and stop mechanisms, and train reviewers on automation bias. *(owner: System Owner / Operations Lead; effort: medium)*
- **Do:** Add input/output guardrails, evaluate hallucination and prompt-injection resistance before release, and publish an acceptable-use policy for generative AI tools. *(owner: Product Lead / CISO; effort: medium)*
- Evidence [doc:ai-policy.md]: "Generative AI"
- Evidence [doc:ai-policy.md]: "A guardrail and hallucination evaluation standard will be developed in 2027."
- Evidence [doc:ai-policy.md]: "Human oversight is required for any decision that affects a customer's access to credit."

### NIST AI Risk Management Framework MAP 2.3 - Scientific integrity and TEVV

Partial, medium priority, score 37

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 46/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Scientific integrity and TEVV considerations are identified and documented, including those related to experimental design, data collection and selection, system trustworthiness, and construct validation.
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*
- **Do:** Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Validation"
- Evidence [doc:model-risk-procedure.md]: "The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set)"

### NIST AI Risk Management Framework MEASURE 2.1 - TEVV documentation

Partial, medium priority, score 37

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 46/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Test sets, metrics, and details about the tools used during TEVV are documented.
- **Do:** Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; effort: medium)*
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Validation"
- Evidence [doc:model-risk-procedure.md]: "The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set)"

### EU Artificial Intelligence Act Art. 13 - Transparency and provision of information to deployers

Partial, medium priority, score 40 - binding law

0 of 2 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'repo/MODEL_CARD.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Do instructions for use state the provider's identity, the system's characteristics, capabilities and limitations, intended purpose, accuracy and robustness metrics, known risks, and conditions affecting performance?
- Gap: Not answered; evidence is incomplete for: Do they describe human oversight measures, required computational resources, expected lifetime, maintenance, and how to collect and interpret logs?
- **Do:** Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; effort: low)*
- **Do:** Implement explanation methods suited to each model and a process to give affected individuals the main reasons for a decision. *(owner: Head of Data Science / Product Lead; effort: medium)*
- Evidence [repo:repo/MODEL_CARD.md]: "Explanations:** SHAP values provide the main factors behind each score for the applicant-facing reason codes."
- Evidence [repo:repo/MODEL_CARD.md]: "Intended use:** decision support for consumer loan applications in the EU and US"

### EU Artificial Intelligence Act Art. 2 - Scope

Partial, medium priority, score 40 - binding law

0 of 2 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Has the entity documented, per AI system, whether the AI Act applies and in which role (provider, deployer, importer, distributor, authorised representative)?
- Gap: Not answered; evidence is incomplete for: Where an exclusion is relied on, is the reasoning recorded and approved?
- **Do:** Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; effort: low)*
- **Do:** Build a central AI system register (including vendor and embedded AI), with owner, purpose, role, risk tier and data categories; make registration a gate before deployment. *(owner: AI Governance Lead; effort: medium)*
- Evidence [doc:ai-policy.md]: "The classification rationale is recorded in the AI system inventory."
- Evidence [doc:ai-policy.md]: "Policy owner: Chief Risk Officer"

### EU Artificial Intelligence Act Art. 49 - Registration

Partial, medium priority, score 40 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Before placing an Annex III high-risk system on the market, the provider registers itself and the system in the EU database; providers relying on the Art. 6(3) derogation also register; public-authority deployers register their use.
- **Do:** Plan the conformity assessment route for each high-risk system, prepare the declaration of conformity and register the system before placing it on the market. *(owner: Regulatory Affairs / Product Compliance; effort: high)*
- **Do:** Build a central AI system register (including vendor and embedded AI), with owner, purpose, role, risk tier and data categories; make registration a gate before deployment. *(owner: AI Governance Lead; effort: medium)*
- Evidence [doc:ai-policy.md]: "The classification rationale is recorded in the AI system inventory."
- Evidence [doc:ai-policy.md]: "Policy owner: Chief Risk Officer"

### EU Artificial Intelligence Act Art. 86 - Right to explanation of individual decision-making

Partial, medium priority, score 40 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'repo/MODEL_CARD.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: A person affected by a decision based on the output of an Annex III high-risk system that has legal or similarly significant effects can obtain from the deployer clear and meaningful explanations of the role of the AI system in the decision and the main elements of the decision.
- **Do:** Implement explanation methods suited to each model and a process to give affected individuals the main reasons for a decision. *(owner: Head of Data Science / Product Lead; effort: medium)*
- **Do:** Provide an appeal channel with human review and a correction route for every consequential AI-assisted decision. *(owner: Customer Operations / HR; effort: low)*
- Evidence [repo:repo/MODEL_CARD.md]: "Explanations:** SHAP values provide the main factors behind each score for the applicant-facing reason codes."
- Evidence [repo:repo/MODEL_CARD.md]: "Intended use:** decision support for consumer loan applications in the EU and US"

### General Data Protection Regulation Art. 13 - Information to be provided where personal data are collected from the data subject

Partial, medium priority, score 40 - binding law

0 of 2 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'repo/MODEL_CARD.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Do privacy notices describe each AI processing purpose, lawful basis, recipients, retention and rights?
- Gap: Not answered; evidence is incomplete for: Where automated decision-making or profiling occurs, do notices explain the logic involved and its significance and consequences?
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*
- **Do:** Implement explanation methods suited to each model and a process to give affected individuals the main reasons for a decision. *(owner: Head of Data Science / Product Lead; effort: medium)*
- Evidence [repo:repo/MODEL_CARD.md]: "Explanations:** SHAP values provide the main factors behind each score for the applicant-facing reason codes."
- Evidence [repo:repo/MODEL_CARD.md]: "Intended use:** decision support for consumer loan applications in the EU and US"

### ISO/IEC 42001 AI Management System A.10.2 - Allocating responsibilities

Partial, medium priority, score 40

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'ai-policy.md' addresses 2 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Responsibilities within the AI lifecycle are allocated between the organisation, its partners, suppliers, customers and third parties.
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; effort: medium)*
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"

### NIST AI Risk Management Framework GOVERN 6.1 - Third-party risk policies

Partial, medium priority, score 40

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'ai-policy.md' addresses 2 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Policies and procedures are in place that address AI risks associated with third-party entities, including risks of infringement of a third-party's intellectual property or other rights.
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; effort: medium)*
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"

### NIST AI Risk Management Framework MANAGE 1.4 - Residual risk documented

Partial, medium priority, score 40

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Negative residual risks (defined as the sum of all unmitigated risks) to both downstream acquirers of AI systems and end users are documented.
- **Do:** Implement an AI risk management procedure with a risk register per system, defined scoring, treatment plans, residual-risk sign-off and re-assessment triggers. *(owner: Chief Risk Officer; effort: medium)*
- **Do:** Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; effort: low)*
- Evidence [doc:model-risk-procedure.md]: "Model Risk Management Procedure (Credit Models)"
- Evidence [doc:model-risk-procedure.md]: "Each credit model has an entry in the model risk register with likelihood and severity ratings, mitigation actions and a control owner"

### NIST AI Risk Management Framework MAP 2.2 - Knowledge limits and human use of output

Partial, medium priority, score 40

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'repo/MODEL_CARD.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Information about the AI system's knowledge limits and how system output may be utilized and overseen by humans is documented.
- **Do:** Create a model/system card for each AI system covering intended purpose, architecture, data, metrics and limitations, and keep it under version control with the code. *(owner: Engineering Lead; effort: medium)*
- **Do:** Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; effort: low)*
- Evidence [repo:repo/MODEL_CARD.md]: "Model card: CreditScore v4"
- Evidence [repo:repo/MODEL_CARD.md]: "Intended use:** decision support for consumer loan applications in the EU and US"

### NIST AI Risk Management Framework MAP 4.1 - Mapping legal and technology risks of components

Partial, medium priority, score 40

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'ai-policy.md' addresses 2 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Approaches for mapping AI technology and legal risks of its components, including the use of third-party data or software, are in place, followed, and documented, as are risks of infringement of a third party's intellectual property or other rights.
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; effort: medium)*
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"

### NIST AI Risk Management Framework MAP 5.1 - Likelihood and magnitude of impacts

Partial, medium priority, score 40

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Likelihood and magnitude of each identified impact (both potentially beneficial and harmful) based on expected use, past uses of AI systems in similar contexts, public incident reports, feedback from those external to the team, or other data are identified and documented.
- **Do:** Implement an AI risk management procedure with a risk register per system, defined scoring, treatment plans, residual-risk sign-off and re-assessment triggers. *(owner: Chief Risk Officer; effort: medium)*
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Model Risk Management Procedure (Credit Models)"
- Evidence [doc:model-risk-procedure.md]: "Each credit model has an entry in the model risk register with likelihood and severity ratings, mitigation actions and a control owner"

### OECD AI Principles 1.3 - Transparency and explainability

Partial, medium priority, score 40

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'repo/MODEL_CARD.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Meaningful information is provided so people understand when they interact with AI and can understand and challenge outcomes.
- **Do:** Add clear AI-interaction notices at the point of use and label or watermark AI-generated content. *(owner: Product Lead; effort: low)*
- **Do:** Implement explanation methods suited to each model and a process to give affected individuals the main reasons for a decision. *(owner: Head of Data Science / Product Lead; effort: medium)*
- Evidence [repo:repo/MODEL_CARD.md]: "Explanations:** SHAP values provide the main factors behind each score for the applicant-facing reason codes."
- Evidence [repo:repo/MODEL_CARD.md]: "Intended use:** decision support for consumer loan applications in the EU and US"

### General Data Protection Regulation Art. 34 - Communication of a personal data breach to the data subject

Partial, medium priority, score 48 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 60/100: 'incident-response.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Where a breach is likely to result in a high risk, affected people are told without undue delay in clear and plain language.
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Extend the incident process to AI harms and malfunctions, with severity criteria, regulator notification deadlines and post-incident review. *(owner: CISO / AI Governance Lead; effort: medium)*
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"
- Evidence [doc:incident-response.md]: "Personal data breaches are reported to the supervisory authority within 72 hours"

### ISO/IEC 42001 AI Management System A.8.4 - Communication of incidents

Partial, medium priority, score 48

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 60/100: 'incident-response.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: A plan exists for communicating incidents to users of the AI system.
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Extend the incident process to AI harms and malfunctions, with severity criteria, regulator notification deadlines and post-incident review. *(owner: CISO / AI Governance Lead; effort: medium)*
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"
- Evidence [doc:incident-response.md]: "Personal data breaches are reported to the supervisory authority within 72 hours"

### NIST AI Risk Management Framework MANAGE 2.3 - Responding to unknown risks

Partial, medium priority, score 48

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 60/100: 'incident-response.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Procedures are followed to respond to and recover from a previously unknown risk when it is identified.
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Extend the incident process to AI harms and malfunctions, with severity criteria, regulator notification deadlines and post-incident review. *(owner: CISO / AI Governance Lead; effort: medium)*
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"
- Evidence [doc:incident-response.md]: "Personal data breaches are reported to the supervisory authority within 72 hours"

### NIST AI Risk Management Framework MANAGE 4.3 - Incident communication and recovery

Partial, medium priority, score 48

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 60/100: 'incident-response.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Incidents and errors are communicated to relevant AI actors, including affected communities. Processes for tracking, responding to, and recovering from incidents and errors are followed and documented.
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Extend the incident process to AI harms and malfunctions, with severity criteria, regulator notification deadlines and post-incident review. *(owner: CISO / AI Governance Lead; effort: medium)*
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"
- Evidence [doc:incident-response.md]: "Personal data breaches are reported to the supervisory authority within 72 hours"

### EU Artificial Intelligence Act Art. 4 - AI literacy

Partial, medium priority, score 50 - binding law

2 of 2 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Partly in place: Is AI literacy training provided to staff who build, operate or use AI systems, proportionate to their role and the context of use? (Training delivered to the data science team only)
- Gap: Partly in place: Are training content and completion recorded so the measures can be demonstrated? (Training delivered to the data science team only)
- **Do:** Roll out role-based AI literacy training (all staff, operators, developers, leadership) and track completion. *(owner: HR / Learning & Development; effort: low)*

### NIST AI Risk Management Framework MANAGE 4.1 - Post-deployment monitoring plans

Partial, medium priority, score 54

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 68/100: 'model-risk-procedure.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Post-deployment AI system monitoring plans are implemented, including mechanisms for capturing and evaluating input from users and other relevant AI actors, appeal and override, decommissioning, incident response, recovery, and change management.
- **Do:** Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; effort: medium)*
- **Do:** Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Change management"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"

### EU Artificial Intelligence Act Art. 25 - Responsibilities along the AI value chain

Partial, medium priority, score 55 - binding law

0 of 2 test(s) answered, 0 verified by evidence. Evidence check 69/100: 'model-risk-procedure.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Has the entity checked whether rebranding, substantial modification or a change of intended purpose makes it the provider of any high-risk system?
- Gap: Not answered; evidence is incomplete for: Are there written agreements with suppliers of tools, services, components or models integrated into high-risk systems, specifying information, capabilities, technical access and assistance?
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; effort: medium)*
- **Do:** Version models and datasets alongside code, require reviewed and approved changes, and define what counts as a substantial modification that re-triggers assessment. *(owner: Engineering Lead / MLOps; effort: low)*
- Evidence [doc:model-risk-procedure.md]: "Change management"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."

### EU Artificial Intelligence Act Art. 18 - Documentation keeping

Partial, medium priority, score 56 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 70/100: 'repo/MODEL_CARD.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: For ten years after the system is placed on the market, providers keep the technical documentation, QMS documentation, notified body approvals and decisions, and the EU declaration of conformity available to authorities.
- **Do:** Create a model/system card for each AI system covering intended purpose, architecture, data, metrics and limitations, and keep it under version control with the code. *(owner: Engineering Lead; effort: medium)*
- **Do:** Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; effort: medium)*
- Evidence [repo:repo/MODEL_CARD.md]: "Model card: CreditScore v4"
- Evidence [repo:repo/MODEL_CARD.md]: "Intended use:** decision support for consumer loan applications in the EU and US"

### OECD AI Principles 1.5 - Accountability

Partial, medium priority, score 58

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 72/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: AI actors are accountable for the proper functioning of AI systems, with traceability of datasets, processes and decisions and systematic risk management.
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- **Do:** Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Model Risk Management Procedure (Credit Models)"
- Evidence [doc:model-risk-procedure.md]: "Each credit model has an entry in the model risk register with likelihood and severity ratings, mitigation actions and a control owner"
- Evidence [doc:ai-policy.md]: "Roles and responsibilities"

### EU Artificial Intelligence Act Art. 72 - Post-market monitoring by providers and post-market monitoring plan for high-risk AI systems

Partial, medium priority, score 60 - binding law

0 of 2 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Is there a post-market monitoring plan for each high-risk system, part of its technical documentation?
- Gap: Not answered; evidence is incomplete for: Is performance data (from deployers or other sources) actively collected and analysed to evaluate continuous compliance?
- **Do:** Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### General Data Protection Regulation Art. 5 - Principles relating to processing of personal data

Partial, medium priority, score 60 - binding law

4 of 4 test(s) answered, 0 verified by evidence. Evidence check 33/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Answered yes without supporting evidence - attach or reference the record for: Are the purposes of each AI processing activity (training, fine-tuning, inference, monitoring) specified, and is further use checked for compatibility?
- Gap: Answered yes without supporting evidence - attach or reference the record for: Is data minimised for training and inference, with retention periods set and enforced?
- Gap: Answered yes without supporting evidence - attach or reference the record for: Are steps taken to keep personal data, including AI-generated inferences about people, accurate?
- Gap: Answered yes without supporting evidence - attach or reference the record for: Can the controller demonstrate compliance with each principle (accountability documentation)?
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"
- Evidence [doc:ai-policy.md]: "Approved by the Executive Committee on 14 March 2026"

### General Data Protection Regulation Art. 6 - Lawfulness of processing

Partial, medium priority, score 60 - binding law

3 of 3 test(s) answered, 0 verified by evidence. No supporting evidence found by the evidence checks.

- Gap: Answered yes without supporting evidence - attach or reference the record for: Is a lawful basis identified and recorded for each AI processing purpose?
- Gap: Answered yes without supporting evidence - attach or reference the record for: Where legitimate interests is relied on (for example for model training), is a documented balancing test in place?
- Gap: Answered yes without supporting evidence - attach or reference the record for: Where data is reused for a new purpose, is the Art. 6(4) compatibility assessment documented?
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*

### ISO/IEC 42001 AI Management System 5.1 - Leadership and commitment

Partial, medium priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Top management demonstrates leadership and commitment - AI policy and objectives aligned to strategy, requirements integrated into business processes, resources available, and the AIMS achieving its intended results.
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- Evidence [doc:ai-policy.md]: "Roles and responsibilities"
- Evidence [doc:ai-policy.md]: "Every AI system has a named system owner"

### ISO/IEC 42001 AI Management System 5.3 - Roles, responsibilities and authorities

Partial, medium priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Responsibilities and authorities for relevant roles are assigned and communicated, including for conformity of the AIMS and reporting on its performance.
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- Evidence [doc:ai-policy.md]: "Roles and responsibilities"
- Evidence [doc:ai-policy.md]: "Every AI system has a named system owner"

### ISO/IEC 42001 AI Management System A.3.2 - AI roles and responsibilities

Partial, medium priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Roles and responsibilities for AI are defined and allocated according to the organisation's needs.
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- Evidence [doc:ai-policy.md]: "Roles and responsibilities"
- Evidence [doc:ai-policy.md]: "Every AI system has a named system owner"

### NIST AI Risk Management Framework MEASURE 2.4 - Production monitoring

Partial, medium priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: The functionality and behavior of the AI system and its components are monitored when in production.
- **Do:** Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### ISO/IEC 42001 AI Management System A.4.4 - Tooling resources

Partial, low priority, score 35

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 44/100: 'model-risk-procedure.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Information about tooling resources (algorithms, frameworks, development and deployment tools) is documented.
- **Do:** Version models and datasets alongside code, require reviewed and approved changes, and define what counts as a substantial modification that re-triggers assessment. *(owner: Engineering Lead / MLOps; effort: low)*
- **Do:** Pin and record vendor model versions, re-run your evaluation suite on every model change, and define a fallback for vendor outage or withdrawal. *(owner: Engineering Lead; effort: low)*
- Evidence [doc:model-risk-procedure.md]: "Change management"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### Colorado Artificial Intelligence Act 6-1-1706 - Enforcement by attorney general

Partial, low priority, score 40

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: To support the affirmative defence, the entity discovers and cures violations (through feedback, adversarial testing or internal review) and complies with a recognised AI risk management framework.
- **Do:** Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; effort: medium)*
- **Do:** Implement an AI risk management procedure with a risk register per system, defined scoring, treatment plans, residual-risk sign-off and re-assessment triggers. *(owner: Chief Risk Officer; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Model Risk Management Procedure (Credit Models)"
- Evidence [doc:model-risk-procedure.md]: "Each credit model has an entry in the model risk register with likelihood and severity ratings, mitigation actions and a control owner"

### EU Artificial Intelligence Act Art. 111 - AI systems already placed on the market or put into service and general-purpose AI models already placed on the market

Partial, low priority, score 40 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: The entity has identified AI systems and GPAI models placed on the market or put into service before the application dates, and the transitional deadlines and significant-change triggers that apply to them.
- **Do:** Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; effort: low)*
- **Do:** Build a central AI system register (including vendor and embedded AI), with owner, purpose, role, risk tier and data categories; make registration a gate before deployment. *(owner: AI Governance Lead; effort: medium)*
- Evidence [doc:ai-policy.md]: "The classification rationale is recorded in the AI system inventory."
- Evidence [doc:ai-policy.md]: "Policy owner: Chief Risk Officer"

### General Data Protection Regulation Art. 26 - Joint controllers

Partial, low priority, score 40 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 50/100: 'ai-policy.md' addresses 2 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Where the entity jointly determines purposes and means with another party (for example an AI partner), a transparent arrangement allocates responsibilities, and its essence is available to data subjects.
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; effort: medium)*
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"

### ISO/IEC 42001 AI Management System 8.1 - Operational planning and control

Partial, low priority, score 55

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 69/100: 'model-risk-procedure.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Processes needed to meet requirements are planned, implemented and controlled, including outsourced processes, with criteria and documented evidence.
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Version models and datasets alongside code, require reviewed and approved changes, and define what counts as a substantial modification that re-triggers assessment. *(owner: Engineering Lead / MLOps; effort: low)*
- **Do:** Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Change management"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."

### ISO/IEC 42001 AI Management System 7.5 - Documented information

Partial, low priority, score 56

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 70/100: 'repo/MODEL_CARD.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Documented information required by the standard and the organisation is created, updated and controlled.
- **Do:** Create a model/system card for each AI system covering intended purpose, architecture, data, metrics and limitations, and keep it under version control with the code. *(owner: Engineering Lead; effort: medium)*
- **Do:** Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; effort: medium)*
- Evidence [repo:repo/MODEL_CARD.md]: "Model card: CreditScore v4"
- Evidence [repo:repo/MODEL_CARD.md]: "Intended use:** decision support for consumer loan applications in the EU and US"

### EU Artificial Intelligence Act Art. 87 - Reporting of infringements and protection of reporting persons

Partial, low priority, score 60 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Internal reporting channels cover infringements of the AI Act and protect reporting persons in line with Directive (EU) 2019/1937.
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- Evidence [doc:ai-policy.md]: "Roles and responsibilities"
- Evidence [doc:ai-policy.md]: "Every AI system has a named system owner"

### General Data Protection Regulation Art. 29 - Processing under the authority of the controller or processor

Partial, low priority, score 60 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Staff and processors process personal data only on the controller's instructions.
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- Evidence [doc:ai-policy.md]: "Roles and responsibilities"
- Evidence [doc:ai-policy.md]: "Every AI system has a named system owner"

### ISO/IEC 42001 AI Management System 7.1 - Resources

Partial, low priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Resources needed for the AI management system are determined and provided.
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- Evidence [doc:ai-policy.md]: "Roles and responsibilities"
- Evidence [doc:ai-policy.md]: "Every AI system has a named system owner"

### ISO/IEC 42001 AI Management System A.3.3 - Reporting of concerns

Partial, low priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: A process lets people report concerns about the organisation's role with respect to AI systems throughout their lifecycle.
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- Evidence [doc:ai-policy.md]: "Roles and responsibilities"
- Evidence [doc:ai-policy.md]: "Every AI system has a named system owner"

### NIST AI Risk Management Framework GOVERN 3.1 - Diverse decision-making teams

Partial, low priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Decision-making related to mapping, measuring, and managing AI risks throughout the lifecycle is informed by a diverse team (e.g., diversity of demographics, disciplines, experience, expertise, and backgrounds).
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- Evidence [doc:ai-policy.md]: "Roles and responsibilities"
- Evidence [doc:ai-policy.md]: "Every AI system has a named system owner"

### NIST AI Risk Management Framework MANAGE 2.2 - Sustaining value

Partial, low priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Mechanisms are in place and applied to sustain the value of deployed AI systems.
- **Do:** Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### NIST AI Risk Management Framework MAP 1.2 - Interdisciplinary context team

Partial, low priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Interdisciplinary AI actors, competencies, skills, and capacities for establishing context reflect demographic diversity and broad domain and user experience expertise, and their participation is documented.
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- Evidence [doc:ai-policy.md]: "Roles and responsibilities"
- Evidence [doc:ai-policy.md]: "Every AI system has a named system owner"

### NIST AI Risk Management Framework MEASURE 1.2 - Metrics reviewed

Partial, low priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Appropriateness of AI metrics and effectiveness of existing controls are regularly assessed and updated, including reports of errors and potential impacts on affected communities.
- **Do:** Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### NIST AI Risk Management Framework MEASURE 4.2 - Validated trustworthiness in deployment

Partial, low priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Measurement results regarding AI system trustworthiness in deployment context(s) and across the AI lifecycle are informed by input from domain experts and relevant AI actors to validate whether the system is performing consistently as intended. Results are documented.
- **Do:** Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### NIST AI Risk Management Framework MEASURE 4.3 - Measured improvements and declines

Partial, low priority, score 60

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 75/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Measurable performance improvements or declines based on consultations with relevant AI actors, including affected communities, and field data about context-relevant risks and trustworthiness characteristics are identified and documented.
- **Do:** Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### NIST AI Risk Management Framework GOVERN 4.3 - Testing, incident identification and information sharing

Partial, low priority, score 61

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 76/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Organizational practices are in place to enable AI testing, identification of incidents, and information sharing.
- Gap: Evidence states: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Extend the incident process to AI harms and malfunctions, with severity criteria, regulator notification deadlines and post-incident review. *(owner: CISO / AI Governance Lead; effort: medium)*
- **Do:** Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Validation"
- Evidence [doc:model-risk-procedure.md]: "The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set)"
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"

### NIST AI Risk Management Framework MEASURE 2.6 - Safety evaluation

Partial, low priority, score 61

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 76/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: The AI system is evaluated regularly for safety risks. The AI system to be deployed is demonstrated to be safe, its residual negative risk does not exceed the risk tolerance, and it can fail safely, particularly if made to operate beyond its knowledge limits.
- Gap: Evidence states: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; effort: medium)*
- **Do:** Add input/output guardrails, evaluate hallucination and prompt-injection resistance before release, and publish an acceptable-use policy for generative AI tools. *(owner: Product Lead / CISO; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Validation"
- Evidence [doc:model-risk-procedure.md]: "The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set)"
- Evidence [doc:ai-policy.md]: "Generative AI"

### General Data Protection Regulation Art. 24 - Responsibility of the controller

Partial, low priority, score 70 - binding law

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 88/100: 'ai-policy.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: The controller implements appropriate technical and organisational measures, including data protection policies, to ensure and demonstrate compliance, and reviews them.
- **Do:** Draft and adopt an AI policy covering scope, principles, risk appetite, prohibited uses and review cadence; obtain executive or board approval. *(owner: Chief Risk Officer / AI Governance Lead; effort: medium)*
- **Do:** Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; effort: low)*
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"
- Evidence [doc:ai-policy.md]: "Approved by the Executive Committee on 14 March 2026"
- Evidence [doc:ai-policy.md]: "Roles and responsibilities"

### ISO/IEC 42001 AI Management System 6.3 - Planning of changes

Partial, low priority, score 70

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 88/100: 'model-risk-procedure.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Changes to the AI management system are carried out in a planned manner.
- **Do:** Version models and datasets alongside code, require reviewed and approved changes, and define what counts as a substantial modification that re-triggers assessment. *(owner: Engineering Lead / MLOps; effort: low)*
- Evidence [doc:model-risk-procedure.md]: "Change management"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### ISO/IEC 42001 AI Management System A.6.1.3 - Processes for responsible AI system design and development

Partial, low priority, score 70

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 88/100: 'model-risk-procedure.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Processes for responsible design and development are defined and documented.
- **Do:** Version models and datasets alongside code, require reviewed and approved changes, and define what counts as a substantial modification that re-triggers assessment. *(owner: Engineering Lead / MLOps; effort: low)*
- Evidence [doc:model-risk-procedure.md]: "Change management"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### NIST AI Risk Management Framework GOVERN 5.2 - Incorporating adjudicated feedback

Partial, low priority, score 70

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 88/100: 'model-risk-procedure.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Mechanisms are established to enable the team that developed or deployed AI systems to regularly incorporate adjudicated feedback from relevant AI actors into system design and implementation.
- **Do:** Version models and datasets alongside code, require reviewed and approved changes, and define what counts as a substantial modification that re-triggers assessment. *(owner: Engineering Lead / MLOps; effort: low)*
- Evidence [doc:model-risk-procedure.md]: "Change management"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### NIST AI Risk Management Framework MANAGE 4.2 - Continual improvement

Partial, low priority, score 70

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 88/100: 'model-risk-procedure.md' addresses 3 of 3 expected elements.

- Gap: Not answered; evidence is incomplete for: Measurable activities for continual improvements are integrated into AI system updates and include regular engagement with interested parties, including relevant AI actors.
- **Do:** Version models and datasets alongside code, require reviewed and approved changes, and define what counts as a substantial modification that re-triggers assessment. *(owner: Engineering Lead / MLOps; effort: low)*
- Evidence [doc:model-risk-procedure.md]: "Change management"
- Evidence [doc:model-risk-procedure.md]: "Model changes follow change control: peer review, sign-off by Model Validation, and a documented rollback plan"

### NIST AI Risk Management Framework MEASURE 3.1 - Tracking emergent risks

Partial, low priority, score 70

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 88/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Approaches, personnel, and documentation are in place to regularly identify and track existing, unanticipated, and emergent AI risks based on factors such as intended and actual performance in deployed contexts.
- **Do:** Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; effort: medium)*
- **Do:** Implement an AI risk management procedure with a risk register per system, defined scoring, treatment plans, residual-risk sign-off and re-assessment triggers. *(owner: Chief Risk Officer; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Model Risk Management Procedure (Credit Models)"
- Evidence [doc:model-risk-procedure.md]: "Each credit model has an entry in the model risk register with likelihood and severity ratings, mitigation actions and a control owner"
- Evidence [doc:model-risk-procedure.md]: "A model monitoring dashboard tracks population drift monthly"

### NIST AI Risk Management Framework MEASURE 1.1 - Metrics selected

Partial, low priority, score 74

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 92/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Approaches and metrics for measurement of AI risks enumerated during the MAP function are selected for implementation starting with the most significant AI risks. The risks or trustworthiness characteristics that will not or cannot be measured are properly documented.
- **Do:** Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Validation"
- Evidence [doc:model-risk-procedure.md]: "The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set)"

### NIST AI Risk Management Framework MEASURE 2.2 - Human-subject evaluations

Partial, low priority, score 74

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 92/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Evaluations involving human subjects meet applicable requirements (including human subject protection) and are representative of the relevant population.
- **Do:** Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Validation"
- Evidence [doc:model-risk-procedure.md]: "The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set)"

### NIST AI Risk Management Framework MEASURE 2.3 - Performance in deployment-like conditions

Partial, low priority, score 74

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 92/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: AI system performance or assurance criteria are measured qualitatively or quantitatively and demonstrated for conditions similar to deployment setting(s). Measures are documented.
- **Do:** Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Validation"
- Evidence [doc:model-risk-procedure.md]: "The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set)"

### NIST AI Risk Management Framework MEASURE 4.1 - Context-informed measurement

Partial, low priority, score 74

0 of 1 test(s) answered, 0 verified by evidence. Evidence check 92/100: 'model-risk-procedure.md' addresses 4 of 4 expected elements.

- Gap: Not answered; evidence is incomplete for: Measurement approaches for identifying AI risks are connected to deployment context(s) and informed through consultation with domain experts and other end users. Approaches are documented.
- **Do:** Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; effort: medium)*
- Evidence [doc:model-risk-procedure.md]: "Validation"
- Evidence [doc:model-risk-procedure.md]: "The validation report records AUC, precision and recall against the acceptance criteria (AUC of at least 0.78 on the hold-out test set)"

## Roadmap

### Stabilise (0-30 days)
- [critical] Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; closes 13 article(s): EUAIA.ART.27, GDPR.ART.36, ISO42001.6.1.4, ISO42001.8.4, ISO42001.A.5.2, ISO42001.A.5.3, ISO42001.A.5.4, NIST.GOVERN4.2, NIST.MAP3.2, GDPR.ART.35, ISO42001.A.5.5, NIST.MAP3.1)*
- [critical] Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; closes 11 article(s): DPDP.S.4, GDPR.ART.7, GDPR.ART.88, DPDP.S.5, DPDP.S.7, NIST.MEASURE2.10, GDPR.ART.25, DPDP.S.6, GDPR.ART.13, GDPR.ART.5, GDPR.ART.6)*
- [critical] Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; closes 11 article(s): DPDP.S.8, GDPR.ART.14, ISO42001.A.4.3, ISO42001.A.7.2, ISO42001.A.7.3, ISO42001.A.7.5, NYCLL144.6RCNY5-302, ISO42001.A.7.4, EUAIA.ART.10, ISO42001.A.7.6, NIST.MAP2.3)*
- [critical] Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; closes 8 article(s): GDPR.ART.28, ISO42001.A.10.3, NIST.MANAGE3.1, ISO42001.A.10.2, NIST.GOVERN6.1, NIST.MAP4.1, EUAIA.ART.25, GDPR.ART.26)*
- [critical] Extend the incident process to AI harms and malfunctions, with severity criteria, regulator notification deadlines and post-incident review. *(owner: CISO / AI Governance Lead; closes 6 article(s): EUAIA.ART.73, GDPR.ART.34, ISO42001.A.8.4, NIST.MANAGE2.3, NIST.MANAGE4.3, NIST.GOVERN4.3)*
- [critical] Plan the conformity assessment route for each high-risk system, prepare the declaration of conformity and register the system before placing it on the market. *(owner: Regulatory Affairs / Product Compliance; closes 5 article(s): EUAIA.ART.43, EUAIA.ART.47, EUAIA.ART.48, EUAIA.ART.16, EUAIA.ART.49)*
- [critical] Add group fairness metrics to the evaluation suite, set tolerances, and commission an independent bias audit where the law requires one. *(owner: Head of Data Science; closes 4 article(s): NYCLL144.20-871.A, NYCLL144.6RCNY5-301, NIST.MEASURE2.11, OECD.1.2)*
- [critical] Issue advance notices to people subject to AI-assisted decisions and publish the required summaries (for example bias audit results) on your website. *(owner: Legal / HR / Product; closes 4 article(s): NYCLL144.20-871.B, NYCLL144.6RCNY5-303, NYCLL144.6RCNY5-304, ISO42001.A.8.5)*
- [critical] Threat-model each AI system, run adversarial/red-team testing before release, and harden model, data and pipeline access. *(owner: Chief Information Security Officer; closes 3 article(s): GDPR.ART.32, NIST.MEASURE2.7, ISO42001.A.4.5)*
- [high] Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; closes 7 article(s): ISO42001.4.1, ISO42001.4.2, NIST.GOVERN1.1, GDPR.ART.31, EUAIA.ART.21, EUAIA.ART.2, EUAIA.ART.111)*
- [high] Roll out role-based AI literacy training (all staff, operators, developers, leadership) and track completion. *(owner: HR / Learning & Development; closes 6 article(s): ISO42001.7.2, NIST.GOVERN2.2, NIST.MAP3.4, ISO42001.7.3, ISO42001.A.4.6, EUAIA.ART.4)*
- [high] Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; closes 6 article(s): ISO42001.A.8.2, ISO42001.7.4, ISO42001.A.10.4, ISO42001.A.9.4, NIST.MEASURE2.8, EUAIA.ART.13)*
- [high] Provide an appeal channel with human review and a correction route for every consequential AI-assisted decision. *(owner: Customer Operations / HR; closes 5 article(s): ISO42001.A.8.3, NIST.MEASURE3.3, GDPR.ART.22, NIST.MAP5.2, NIST.GOVERN5.1)*
- [high] Add clear AI-interaction notices at the point of use and label or watermark AI-generated content. *(owner: Product Lead; closes 3 article(s): COAI.6-1-1704, EUAIA.ART.50, OECD.1.3)*
- [high] Pin and record vendor model versions, re-run your evaluation suite on every model change, and define a fallback for vendor outage or withdrawal. *(owner: Engineering Lead; closes 3 article(s): NIST.GOVERN6.2, NIST.MANAGE3.2, NIST.MAP4.2)*
- [high] Define suspension and decommissioning criteria and a retirement procedure covering model, data and user communication. *(owner: System Owner; closes 2 article(s): EUAIA.ART.20, NIST.GOVERN1.7)*

### Build (31-90 days)
- [high] Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; closes 12 article(s): GDPR.ART.12, GDPR.ART.15, GDPR.ART.16, GDPR.ART.17, GDPR.ART.21, DPDP.S.11, DPDP.S.12, DPDP.S.13, GDPR.ART.18, GDPR.ART.20, DPDP.S.14, GDPR.ART.19)*
- [high] Deploy production monitoring for performance, drift and fairness with alert thresholds, owners and documented response playbooks. *(owner: MLOps Lead; closes 10 article(s): ISO42001.A.6.2.6, ISO42001.9.1, NIST.MANAGE4.1, EUAIA.ART.72, NIST.MEASURE2.4, NIST.MANAGE2.2, NIST.MEASURE1.2, NIST.MEASURE4.2, NIST.MEASURE4.3, NIST.MEASURE3.1)*
- [high] Define metrics and release thresholds per system, automate evaluation in CI, and retain signed-off test reports. *(owner: Head of Data Science / QA; closes 9 article(s): ISO42001.A.6.2.4, OECD.1.4, EUAIA.ART.15, NIST.MEASURE2.1, NIST.MEASURE2.6, NIST.MEASURE1.1, NIST.MEASURE2.2, NIST.MEASURE2.3, NIST.MEASURE4.1)*
- [high] Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; closes 8 article(s): ISO42001.9.2, ISO42001.9.3, NIST.GOVERN1.5, NIST.MEASURE1.3, ISO42001.10.1, NIST.MEASURE2.13, ISO42001.10.2, COAI.6-1-1706)*
- [high] Define the oversight model for each system (who reviews what, when), build override and stop mechanisms, and train reviewers on automation bias. *(owner: System Owner / Operations Lead; closes 6 article(s): NIST.MANAGE2.4, NIST.MAP3.5, EUAIA.ART.14, EUAIA.ART.26, NIST.GOVERN3.2, ISO42001.A.9.2)*
- [high] Create a model/system card for each AI system covering intended purpose, architecture, data, metrics and limitations, and keep it under version control with the code. *(owner: Engineering Lead; closes 4 article(s): COAI.6-1-1702, NIST.MAP2.2, EUAIA.ART.18, ISO42001.7.5)*
- [high] Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; closes 3 article(s): EUAIA.ART.12, EUAIA.ART.19, ISO42001.A.6.2.8)*
- [high] Implement an AI risk management procedure with a risk register per system, defined scoring, treatment plans, residual-risk sign-off and re-assessment triggers. *(owner: Chief Risk Officer; closes 3 article(s): COAI.6-1-1703, NIST.MANAGE1.4, NIST.MAP5.1)*
- [high] Draft and adopt an AI policy covering scope, principles, risk appetite, prohibited uses and review cadence; obtain executive or board approval. *(owner: Chief Risk Officer / AI Governance Lead; closes 2 article(s): EUAIA.ART.17, GDPR.ART.24)*
- [medium] Establish an AI governance committee with a named accountable executive, assign an owner to every AI system, and publish a RACI with escalation and concern-reporting routes. *(owner: Chief Executive / Accountable Executive; closes 10 article(s): OECD.1.5, ISO42001.5.1, ISO42001.5.3, ISO42001.A.3.2, EUAIA.ART.87, GDPR.ART.29, ISO42001.7.1, ISO42001.A.3.3, NIST.GOVERN3.1, NIST.MAP1.2)*
- [medium] Version models and datasets alongside code, require reviewed and approved changes, and define what counts as a substantial modification that re-triggers assessment. *(owner: Engineering Lead / MLOps; closes 7 article(s): ISO42001.A.6.2.5, ISO42001.A.4.4, ISO42001.8.1, ISO42001.6.3, ISO42001.A.6.1.3, NIST.GOVERN5.2, NIST.MANAGE4.2)*
- [medium] Implement explanation methods suited to each model and a process to give affected individuals the main reasons for a decision. *(owner: Head of Data Science / Product Lead; closes 1 article(s): EUAIA.ART.86)*

## Articles met

- EU Artificial Intelligence Act Art. 5 Prohibited AI practices
- EU Artificial Intelligence Act Art. 6 Classification rules for high-risk AI systems
- EU Artificial Intelligence Act Art. 8 Compliance with the requirements
- EU Artificial Intelligence Act Art. 9 Risk management system
- EU Artificial Intelligence Act Art. 11 Technical documentation
- EU Artificial Intelligence Act Art. 95 Codes of conduct for voluntary application of specific requirements
- General Data Protection Regulation Art. 30 Records of processing activities
- General Data Protection Regulation Art. 33 Notification of a personal data breach to the supervisory authority
- ISO/IEC 42001 AI Management System 4.3 Determining the scope of the AI management system
- ISO/IEC 42001 AI Management System 4.4 AI management system
- ISO/IEC 42001 AI Management System 5.2 AI policy
- ISO/IEC 42001 AI Management System 6.1.1 Actions to address risks and opportunities - general
- ISO/IEC 42001 AI Management System 6.1.2 AI risk assessment
- ISO/IEC 42001 AI Management System 6.1.3 AI risk treatment
- ISO/IEC 42001 AI Management System 6.2 AI objectives and planning to achieve them
- ISO/IEC 42001 AI Management System 8.2 AI risk assessment (operation)
- ISO/IEC 42001 AI Management System 8.3 AI risk treatment (operation)
- ISO/IEC 42001 AI Management System A.2.2 AI policy
- ISO/IEC 42001 AI Management System A.2.3 Alignment with other organizational policies
- ISO/IEC 42001 AI Management System A.2.4 Review of the AI policy
- ISO/IEC 42001 AI Management System A.4.2 Resource documentation
- ISO/IEC 42001 AI Management System A.6.1.2 Objectives for responsible development of AI system
- ISO/IEC 42001 AI Management System A.6.2.2 AI system requirements and specification
- ISO/IEC 42001 AI Management System A.6.2.3 Documentation of AI system design and development
- ISO/IEC 42001 AI Management System A.6.2.7 AI system technical documentation
- ISO/IEC 42001 AI Management System A.9.3 Objectives for responsible use of AI system
- NIST AI Risk Management Framework GOVERN 1.2 Trustworthy AI in policy
- NIST AI Risk Management Framework GOVERN 1.3 Risk-based level of risk management
- NIST AI Risk Management Framework GOVERN 1.4 Transparent risk management policies
- NIST AI Risk Management Framework GOVERN 1.6 AI system inventory
- NIST AI Risk Management Framework GOVERN 2.1 Roles and responsibilities
- NIST AI Risk Management Framework GOVERN 2.3 Executive accountability
- NIST AI Risk Management Framework GOVERN 4.1 Safety-first culture
- NIST AI Risk Management Framework MAP 1.1 Intended purpose and context
- NIST AI Risk Management Framework MAP 1.3 Mission and goals
- NIST AI Risk Management Framework MAP 1.4 Business value
- NIST AI Risk Management Framework MAP 1.5 Risk tolerance
- NIST AI Risk Management Framework MAP 1.6 System requirements
- NIST AI Risk Management Framework MAP 2.1 Tasks and methods defined
- NIST AI Risk Management Framework MAP 3.3 Application scope
- NIST AI Risk Management Framework MEASURE 2.5 Validity and reliability
- NIST AI Risk Management Framework MEASURE 2.9 Explainability
- NIST AI Risk Management Framework MEASURE 2.12 Environmental impact
- NIST AI Risk Management Framework MEASURE 3.2 Hard-to-measure risks
- NIST AI Risk Management Framework MANAGE 1.1 Go / no-go determination
- NIST AI Risk Management Framework MANAGE 1.2 Risk treatment prioritised
- NIST AI Risk Management Framework MANAGE 1.3 Responses to high-priority risks
- NIST AI Risk Management Framework MANAGE 2.1 Resources and non-AI alternatives

## Notes

- System 'TalentRank' is declared 'limited' but screening suggests 'high': Matches high-risk area(s): employment. The stricter tier is used; confirm the classification.

---
This report is a governance diagnostic produced by rule-based tests, not legal advice or a certification. Article summaries are paraphrased; confirm applicability, current wording and effective dates against the official texts and with qualified counsel before relying on a finding.
