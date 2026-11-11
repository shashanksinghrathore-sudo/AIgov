# AI Governance & Compliance Assessment: Acme Lending (example)

- **Date:** 2026-11-11T15:37:08+00:00
- **Assessment method:** Rule-based (offline)
- **Jurisdictions:** EU, US-CO, US-NY, IN
- **Overall score:** 46/100 (Level 3 - Defined)

## Executive summary

Acme Lending (example) scores 46 out of 100 against the unified AI governance control catalog (Level 3 - Defined). 10 of 32 applicable controls are met, 7 are partly met and 15 are gaps.

Binding law in scope: EU Artificial Intelligence Act (49/100); General Data Protection Regulation (46/100); Colorado Artificial Intelligence Act (52/100); NYC Automated Employment Decision Tools Law (14/100); India Digital Personal Data Protection Act (34/100). 4 critical gap(s) carry direct legal exposure: DAT-01 Data quality, provenance and documentation, DEV-03 Fairness and non-discrimination testing, DEV-04 Security and adversarial resilience, RSK-04 Conformity assessment, declaration and registration. Systems screened as high-risk: CreditScore v4, TalentRank.

Weakest areas: Third-Party & Supply Chain (18/100) and Data Governance (20/100).

This summary was produced by the rule-based evaluator, which checks whether evidence addresses each control, not whether the control is effective. Run with AI mode enabled for a substantive review and tailored recommendations.

## Frameworks

| Framework | Type | In scope | Score | Met | Partial | Gap |
|---|---|---|---|---|---|---|
| EU Artificial Intelligence Act (Regulation (EU) 2024/1689) | Binding law | Yes | 49 | 10 | 6 | 12 |
| General Data Protection Regulation (Regulation (EU) 2016/679) | Binding law | Yes | 46 | 3 | 4 | 4 |
| Colorado Artificial Intelligence Act (Colorado SB 24-205 (C.R.S. 6-1-1701 et seq.)) | Binding law | Yes | 52 | 5 | 3 | 6 |
| NYC Automated Employment Decision Tools Law (NYC Local Law 144 of 2021 (Admin. Code 20-870 et seq.)) | Binding law | Yes | 14 | 0 | 1 | 2 |
| India Digital Personal Data Protection Act (Act No. 22 of 2023, with DPDP Rules 2025) | Binding law | Yes | 34 | 1 | 4 | 4 |
| NIST AI Risk Management Framework (NIST AI 100-1 (AI RMF 1.0) and AI 600-1 (Generative AI Profile)) | Voluntary | Yes | 49 | 10 | 7 | 13 |
| ISO/IEC 42001 AI Management System (ISO/IEC 42001:2023) | Voluntary | Yes | 47 | 10 | 7 | 14 |
| OECD AI Principles (OECD/LEGAL/0449 (2019, revised 2024)) | Voluntary | Yes | 52 | 7 | 4 | 7 |

## AI systems

| System | Role | Risk tier | Basis |
|---|---|---|---|
| CreditScore v4 | provider | high | Declared in profile. Screening result: high. Matches high-risk area(s): essential services. |
| TalentRank | deployer | high | Matches high-risk area(s): employment. |
| Ava support assistant | deployer | limited | Declared in profile. Screening result: limited. Interacts with people or generates content; transparency obligations apply. |

## Domain scores

- Governance & Accountability: 63/100
- Risk Management: 59/100
- Data Governance: 20/100
- Development & Technical Documentation: 54/100
- Transparency & Explainability: 25/100
- Human Oversight: 40/100
- Operations & Monitoring: 52/100
- Third-Party & Supply Chain: 18/100
- Generative AI Safeguards: 60/100

## Gaps and recommendations

### DAT-01 Data quality, provenance and documentation (Gap, critical priority, score 0)

No evidence found.

*Requirements:* EU Artificial Intelligence Act: Art. 10; NIST AI Risk Management Framework: MAP 2.3, MEASURE 2.1; ISO/IEC 42001 AI Management System: A.4.3, A.7.2, A.7.3, A.7.4, A.7.5, A.7.6; India Digital Personal Data Protection Act: s. 8(3); General Data Protection Regulation: Art. 5(1)(d)

- Gap: No document found that addresses this control.
- Gap: Technical signals not detected: datasheet, data_versioning
- **Do:** Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; effort: medium)*

### DEV-03 Fairness and non-discrimination testing (Gap, critical priority, score 0)

Management reports the control is not in place. Management note: No bias audit of TalentRank has been commissioned

*Requirements:* EU Artificial Intelligence Act: Art. 10(2)(f), Art. 15(4); NIST AI Risk Management Framework: MEASURE 2.11; ISO/IEC 42001 AI Management System: A.5.4, A.6.2.4; OECD AI Principles: 1.2; NYC Automated Employment Decision Tools Law: 20-871(a)(1), 6 RCNY 5-301; Colorado Artificial Intelligence Act: 6-1-1703(1), 6-1-1703(3)

- Gap: No document found that addresses this control.
- Gap: Technical signals not detected: fairness_lib
- **Do:** Add group fairness metrics to the evaluation suite, set tolerances, and commission an independent bias audit where the law requires one. *(owner: Head of Data Science; effort: medium)*

### DEV-04 Security and adversarial resilience (Gap, critical priority, score 0)

No evidence found.

*Requirements:* EU Artificial Intelligence Act: Art. 15(5); NIST AI Risk Management Framework: MEASURE 2.7, MANAGE 2.3; ISO/IEC 42001 AI Management System: A.6.2.4, A.4.5; General Data Protection Regulation: Art. 32; India Digital Personal Data Protection Act: s. 8(5); OECD AI Principles: 1.4

- Gap: No document found that addresses this control.
- Gap: Technical signals not detected: security_policy, adversarial_testing, dependency_lock
- **Do:** Threat-model each AI system, run adversarial/red-team testing before release, and harden model, data and pipeline access. *(owner: Chief Information Security Officer; effort: medium)*

### RSK-04 Conformity assessment, declaration and registration (Gap, critical priority, score 0)

No evidence found.

*Requirements:* EU Artificial Intelligence Act: Art. 16, Art. 43, Art. 47, Art. 48, Art. 49; ISO/IEC 42001 AI Management System: A.6.2.5

- Gap: No document found that addresses this control.
- **Do:** Plan the conformity assessment route for each high-risk system, prepare the declaration of conformity and register the system before placing it on the market. *(owner: Regulatory Affairs / Product Compliance; effort: high)*

### DAT-04 Individual rights and automated decision safeguards (Gap, high priority, score 0)

No evidence found.

*Requirements:* General Data Protection Regulation: Art. 15, Art. 16, Art. 17, Art. 21, Art. 22; India Digital Personal Data Protection Act: s. 11, s. 12, s. 13; Colorado Artificial Intelligence Act: 6-1-1703(4); NIST AI Risk Management Framework: MEASURE 2.10

- Gap: No document found that addresses this control.
- **Do:** Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; effort: medium)*

### GOV-04 Legal and regulatory requirements register (Gap, high priority, score 0)

No evidence found.

*Requirements:* NIST AI Risk Management Framework: GOVERN 1.1; ISO/IEC 42001 AI Management System: 4.1, 4.2, 6.1; OECD AI Principles: 1.2

- Gap: No document found that addresses this control.
- **Do:** Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; effort: low)*

### GOV-06 Internal audit and management review (Gap, high priority, score 0)

Management reports the control is not in place.

*Requirements:* NIST AI Risk Management Framework: GOVERN 1.5, MEASURE 1.3; ISO/IEC 42001 AI Management System: 9.2, 9.3, 10.1, 10.2; India Digital Personal Data Protection Act: s. 10(2)(b)

- Gap: No document found that addresses this control.
- **Do:** Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; effort: medium)*

### TPR-02 Monitoring of third-party and pre-trained models (Gap, high priority, score 0)

No evidence found.

*Requirements:* NIST AI Risk Management Framework: MANAGE 3.1, MANAGE 3.2, GOVERN 6.2; ISO/IEC 42001 AI Management System: A.10.3, A.4.4; EU Artificial Intelligence Act: Art. 25(4)

- Gap: No document found that addresses this control.
- Gap: Technical signals not detected: dependency_lock, eval_scripts
- **Do:** Pin and record vendor model versions, re-run your evaluation suite on every model change, and define a fallback for vendor outage or withdrawal. *(owner: Engineering Lead; effort: low)*

### TRN-01 AI interaction disclosure and AI-generated content marking (Gap, high priority, score 0)

No evidence found.

*Requirements:* EU Artificial Intelligence Act: Art. 50; Colorado Artificial Intelligence Act: 6-1-1704; NIST AI Risk Management Framework: GOVERN 5.1, MEASURE 2.8; ISO/IEC 42001 AI Management System: A.8.2; OECD AI Principles: 1.3

- Gap: No document found that addresses this control.
- **Do:** Add clear AI-interaction notices at the point of use and label or watermark AI-generated content. *(owner: Product Lead; effort: low)*

### TRN-02 Instructions for use and information for deployers and users (Gap, high priority, score 0)

No evidence found.

*Requirements:* EU Artificial Intelligence Act: Art. 13, Art. 26(1); NIST AI Risk Management Framework: MAP 2.2, MAP 3.4; ISO/IEC 42001 AI Management System: A.8.2, A.8.5, A.9.2, A.9.4, A.10.4; OECD AI Principles: 1.3; Colorado Artificial Intelligence Act: 6-1-1702(2), 6-1-1702(3)

- Gap: No document found that addresses this control.
- **Do:** Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; effort: low)*

### TRN-04 Notices to affected individuals and public statements (Gap, high priority, score 0)

Management reports the control is not in place.

*Requirements:* EU Artificial Intelligence Act: Art. 26(7), Art. 26(11); NYC Automated Employment Decision Tools Law: 20-871(a)(2), 20-871(b); Colorado Artificial Intelligence Act: 6-1-1703(4)(a), 6-1-1703(5); ISO/IEC 42001 AI Management System: A.8.3, A.8.5

- Gap: No document found that addresses this control.
- **Do:** Issue advance notices to people subject to AI-assisted decisions and publish the required summaries (for example bias audit results) on your website. *(owner: Legal / HR / Product; effort: low)*

### DAT-02 Bias examination and mitigation in data (Gap, high priority, score 25)

'incident-response.md' addresses 1 of 3 expected elements. The document itself indicates the control is incomplete or only planned.

*Requirements:* EU Artificial Intelligence Act: Art. 10(2)(f), Art. 10(2)(g); NIST AI Risk Management Framework: MEASURE 2.11, MAP 2.3; ISO/IEC 42001 AI Management System: A.7.4, A.5.4; OECD AI Principles: 1.2; Colorado Artificial Intelligence Act: 6-1-1702(1), 6-1-1703(1)

- Gap: No evidence of: protected characteristic / protected attribute / protected class
- Gap: No evidence of: mitigat / re-weight / resampl
- Gap: Stated as absent or planned: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- Gap: Technical signals not detected: fairness_lib
- **Do:** Add a bias examination step to data preparation covering protected groups and proxies, and document findings and mitigations. *(owner: Head of Data Science; effort: medium)*
- Evidence [doc:incident-response.md]: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."

### TPR-01 Vendor and third-party AI due diligence (Gap, high priority, score 30)

'ai-policy.md' addresses 2 of 4 expected elements. The document itself indicates the control is incomplete or only planned. Management reports the control is not in place. Documents mention the topic, so they may be drafts or not operational.

*Requirements:* EU Artificial Intelligence Act: Art. 25, Art. 26(1); General Data Protection Regulation: Art. 28; NIST AI Risk Management Framework: GOVERN 6.1, GOVERN 6.2, MAP 4.1, MAP 4.2, MANAGE 3.1; ISO/IEC 42001 AI Management System: A.10.2, A.10.3

- Gap: No evidence of: due diligence / vendor assessment / risk assessment
- Gap: No evidence of: contract / data processing agreement / dpa
- Gap: Stated as absent or planned: "A guardrail and hallucination evaluation standard will be developed in 2027."
- **Do:** Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; effort: medium)*
- Evidence [doc:ai-policy.md]: "This AI policy applies to every AI system that Acme builds, buys or embeds in a product, including vendor tools."
- Evidence [doc:ai-policy.md]: "Acme Lending AI Policy"

### HUM-01 Human oversight by design (Gap, high priority, score 33)

'ai-policy.md' addresses 1 of 3 expected elements.

*Requirements:* EU Artificial Intelligence Act: Art. 14, Art. 26(2); NIST AI Risk Management Framework: GOVERN 3.2, MAP 3.5, MANAGE 2.4; ISO/IEC 42001 AI Management System: A.9.2, A.9.3; OECD AI Principles: 1.2, 1.5

- Gap: No evidence of: override / intervene / stop
- Gap: No evidence of: automation bias / over-reliance / overreliance
- **Do:** Define the oversight model for each system (who reviews what, when), build override and stop mechanisms, and train reviewers on automation bias. *(owner: System Owner / Operations Lead; effort: medium)*
- Evidence [doc:ai-policy.md]: "Human oversight is required for any decision that affects a customer's access to credit."

### RSK-03 Impact assessment (AI, fundamental rights, data protection) (Partial, high priority, score 35)

Management reports the control is partly in place. Management note: DPIA exists for CreditScore; none for TalentRank or Ava

*Requirements:* EU Artificial Intelligence Act: Art. 27; General Data Protection Regulation: Art. 35; NIST AI Risk Management Framework: MAP 3.1, MAP 3.2, MAP 5.1, GOVERN 4.2; ISO/IEC 42001 AI Management System: 6.1.4, 8.4, A.5.2, A.5.3, A.5.4, A.5.5; Colorado Artificial Intelligence Act: 6-1-1703(3); India Digital Personal Data Protection Act: s. 10(2)(c); OECD AI Principles: 1.2

- Gap: No document found that addresses this control.
- **Do:** Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; effort: medium)*

### OPS-01 Logging and record-keeping (Partial, high priority, score 40)

Technical signals present: logging_usage. Management reports the control is partly in place.

*Requirements:* EU Artificial Intelligence Act: Art. 12, Art. 19, Art. 26(6); NIST AI Risk Management Framework: MEASURE 2.8, MANAGE 4.1; ISO/IEC 42001 AI Management System: A.6.2.8, 7.5; OECD AI Principles: 1.5

- Gap: No document found that addresses this control.
- **Do:** Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; effort: medium)*

### DAT-03 Privacy, lawful basis and data minimisation (Partial, high priority, score 50)

Management attests the control is in place, but no corroborating evidence was found. Management note: Covered by the group privacy programme

*Requirements:* General Data Protection Regulation: Art. 5, Art. 6, Art. 13, Art. 14, Art. 25, Art. 32; India Digital Personal Data Protection Act: s. 4, s. 5, s. 6, s. 8(5), s. 8(7); EU Artificial Intelligence Act: Art. 10(5); NIST AI Risk Management Framework: MEASURE 2.10; ISO/IEC 42001 AI Management System: A.7.3; OECD AI Principles: 1.2

- Gap: Attested but unverified: provide the document or record that demonstrates this control.
- Gap: No document found that addresses this control.
- Gap: Technical signals not detected: pii_tooling
- **Do:** Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; effort: medium)*

### OPS-04 Corrective action, withdrawal and decommissioning (Gap, medium priority, score 0)

No evidence found.

*Requirements:* EU Artificial Intelligence Act: Art. 20; NIST AI Risk Management Framework: GOVERN 1.7, MANAGE 2.4; ISO/IEC 42001 AI Management System: A.6.2.6, 10.2

- Gap: No document found that addresses this control.
- **Do:** Define suspension and decommissioning criteria and a retirement procedure covering model, data and user communication. *(owner: System Owner; effort: low)*

### GOV-05 AI literacy and competence (Partial, medium priority, score 35)

Management reports the control is partly in place. Management note: Training delivered to data science team only

*Requirements:* EU Artificial Intelligence Act: Art. 4, Art. 26(2); NIST AI Risk Management Framework: GOVERN 2.2, MAP 3.4; ISO/IEC 42001 AI Management System: 7.2, 7.3, A.4.6

- Gap: No document found that addresses this control.
- **Do:** Roll out role-based AI literacy training (all staff, operators, developers, leadership) and track completion. *(owner: HR / Learning & Development; effort: low)*

### HUM-02 Contestation, appeal and human review of decisions (Partial, medium priority, score 50)

Management attests the control is in place, but no corroborating evidence was found.

*Requirements:* General Data Protection Regulation: Art. 22(3); Colorado Artificial Intelligence Act: 6-1-1703(4)(b); NIST AI Risk Management Framework: MANAGE 4.1, MEASURE 3.3; ISO/IEC 42001 AI Management System: A.8.3; India Digital Personal Data Protection Act: s. 13; NYC Automated Employment Decision Tools Law: 6 RCNY 5-304

- Gap: Attested but unverified: provide the document or record that demonstrates this control.
- Gap: No document found that addresses this control.
- **Do:** Provide an appeal channel with human review and a correction route for every consequential AI-assisted decision. *(owner: Customer Operations / HR; effort: low)*

### GEN-01 Generative AI safety evaluation and guardrails (Partial, medium priority, score 60)

'ai-policy.md' addresses 4 of 4 expected elements. The document itself indicates the control is incomplete or only planned.

*Requirements:* NIST AI Risk Management Framework: AI 600-1, MEASURE 2.6, MEASURE 2.7; EU Artificial Intelligence Act: Art. 50(2), Art. 15; ISO/IEC 42001 AI Management System: A.9.2, A.6.2.4; OECD AI Principles: 1.4

- Gap: Stated as absent or planned: "A guardrail and hallucination evaluation standard will be developed in 2027."
- Gap: Technical signals not detected: guardrails_lib, adversarial_testing, eval_scripts
- **Do:** Add input/output guardrails, evaluate hallucination and prompt-injection resistance before release, and publish an acceptable-use policy for generative AI tools. *(owner: Product Lead / CISO; effort: medium)*
- Evidence [doc:ai-policy.md]: "Generative AI"
- Evidence [doc:ai-policy.md]: "A guardrail and hallucination evaluation standard will be developed in 2027."
- Evidence [doc:ai-policy.md]: "Staff may only use approved tools for generative AI"

### OPS-03 Incident management and regulatory reporting (Partial, medium priority, score 60)

'incident-response.md' addresses 4 of 4 expected elements. The document itself indicates the control is incomplete or only planned.

*Requirements:* EU Artificial Intelligence Act: Art. 73, Art. 20, Art. 26(5); General Data Protection Regulation: Art. 33, Art. 34; India Digital Personal Data Protection Act: s. 8(6); NIST AI Risk Management Framework: GOVERN 4.3, MANAGE 4.3; ISO/IEC 42001 AI Management System: A.8.4, 10.2; Colorado Artificial Intelligence Act: 6-1-1702(5), 6-1-1703(7)

- Gap: Stated as absent or planned: "AI-specific failures (for example a model producing discriminatory outcomes) are not yet covered by this plan."
- **Do:** Extend the incident process to AI harms and malfunctions, with severity criteria, regulator notification deadlines and post-incident review. *(owner: CISO / AI Governance Lead; effort: medium)*
- Evidence [doc:incident-response.md]: "Security Incident Response Plan"
- Evidence [doc:incident-response.md]: "Personal data breaches are reported to the supervisory authority within 72 hours"
- Evidence [doc:incident-response.md]: "A post-incident review identifies root cause."

## Roadmap

### Stabilise (0-30 days)
- Produce a datasheet for every dataset used in AI development (source, licence, preparation, known gaps), and add automated data-quality checks and versioning. *(owner: Head of Data; closes DAT-01)*
- Add group fairness metrics to the evaluation suite, set tolerances, and commission an independent bias audit where the law requires one. *(owner: Head of Data Science; closes DEV-03)*
- Threat-model each AI system, run adversarial/red-team testing before release, and harden model, data and pipeline access. *(owner: Chief Information Security Officer; closes DEV-04)*
- Plan the conformity assessment route for each high-risk system, prepare the declaration of conformity and register the system before placing it on the market. *(owner: Regulatory Affairs / Product Compliance; closes RSK-04)*
- Maintain an obligations register mapping each AI system to the laws and standards that apply to it, with an owner responsible for horizon scanning. *(owner: General Counsel / Compliance; closes GOV-04)*
- Pin and record vendor model versions, re-run your evaluation suite on every model change, and define a fallback for vendor outage or withdrawal. *(owner: Engineering Lead; closes TPR-02)*
- Add clear AI-interaction notices at the point of use and label or watermark AI-generated content. *(owner: Product Lead; closes TRN-01)*
- Publish instructions for use for each system stating capabilities, limitations, intended and prohibited uses, and oversight expectations. *(owner: Product Lead; closes TRN-02)*
- Issue advance notices to people subject to AI-assisted decisions and publish the required summaries (for example bias audit results) on your website. *(owner: Legal / HR / Product; closes TRN-04)*

### Build (31-90 days)
- Extend the rights-request procedure to AI systems (including training data and model outputs) and define safeguards for solely automated decisions. *(owner: Data Protection Officer; closes DAT-04)*
- Add AI governance to the internal audit plan, hold a periodic management review, and track corrective actions to closure. *(owner: Head of Internal Audit; closes GOV-06)*
- Add a bias examination step to data preparation covering protected groups and proxies, and document findings and mitigations. *(owner: Head of Data Science; closes DAT-02)*
- Add AI-specific due diligence to procurement and contract clauses covering documentation, permitted use, audit rights, incident notice and model change notification. *(owner: Procurement / Vendor Risk; closes TPR-01)*
- Define the oversight model for each system (who reviews what, when), build override and stop mechanisms, and train reviewers on automation bias. *(owner: System Owner / Operations Lead; closes HUM-01)*
- Adopt a combined AI/data-protection/fundamental-rights impact assessment template and require a completed assessment before go-live and on material change. *(owner: Data Protection Officer / AI Governance Lead; closes RSK-03)*
- Log inputs, outputs, model version and human interventions for each decision, with tamper-evident storage and a defined retention period. *(owner: Engineering Lead / MLOps; closes OPS-01)*
- Record the lawful basis or consent for each AI processing purpose, update privacy notices, and apply minimisation, retention limits and pseudonymisation to training and inference data. *(owner: Data Protection Officer; closes DAT-03)*
- Define suspension and decommissioning criteria and a retirement procedure covering model, data and user communication. *(owner: System Owner; closes OPS-04)*
- Roll out role-based AI literacy training (all staff, operators, developers, leadership) and track completion. *(owner: HR / Learning & Development; closes GOV-05)*
- Provide an appeal channel with human review and a correction route for every consequential AI-assisted decision. *(owner: Customer Operations / HR; closes HUM-02)*
- Add input/output guardrails, evaluate hallucination and prompt-injection resistance before release, and publish an acceptable-use policy for generative AI tools. *(owner: Product Lead / CISO; closes GEN-01)*
- Extend the incident process to AI harms and malfunctions, with severity criteria, regulator notification deadlines and post-incident review. *(owner: CISO / AI Governance Lead; closes OPS-03)*

## Controls met

- GOV-01 AI governance policy
- GOV-02 Roles, responsibilities and executive accountability
- GOV-03 AI system inventory
- RSK-01 Risk classification and prohibited-practice screening
- RSK-02 Lifecycle AI risk management process
- DEV-01 Technical documentation and model cards
- DEV-02 Testing, validation and performance thresholds
- DEV-05 Change management, versioning and reproducibility
- TRN-03 Explainability and explanation of decisions
- OPS-02 Post-deployment monitoring

## Notes and limitations

- System 'TalentRank' is declared 'limited' but screening suggests 'high': Matches high-risk area(s): employment. The stricter tier is used; confirm the classification.

---
This report is a governance diagnostic, not legal advice or a certification. Framework references are mapped at clause level to help you find the source text; confirm applicability, current wording and effective dates with qualified counsel before relying on them.
