"""Risk classification of AI systems and framework/control applicability.

The keyword classifier is a screening aid, not a legal determination: it flags systems
that *look like* they fall in a prohibited or high-risk category so a person can confirm.
A tier declared in the profile is kept, but a stricter screening result is surfaced as a warning.
"""
from __future__ import annotations

import re

from ..models import AISystem, Framework, Profile, Requirement

TIER_RANK = {"minimal": 0, "limited": 1, "high": 2, "prohibited": 3}

# Every flag a rule can be conditioned on. Entity-level flags are ticked on the profile;
# the rest are derived from the declared AI systems.
FLAG_LABELS = {
    "provider": "Provider / developer of an AI system",
    "deployer": "Deployer / user of an AI system",
    "importer": "Imports AI systems into the EU market",
    "distributor": "Distributes AI systems made by others",
    "gpai_provider": "Provides a general-purpose AI model",
    "gpai_systemic": "Provides a general-purpose AI model with systemic risk",
    "high_risk": "Has a high-risk AI system",
    "personal_data": "Processes personal data with AI",
    "special_category_data": "Processes special-category / sensitive personal data",
    "criminal_data": "Processes criminal-offence data",
    "children_data": "Processes children's personal data",
    "automated_decisions": "Makes solely automated decisions with significant effects",
    "consequential_decisions": "Uses AI in consequential decisions (credit, employment, housing, health, education)",
    "credit_or_insurance": "Uses AI for credit scoring or life / health insurance pricing",
    "employment": "Uses AI in hiring, promotion or other employment decisions",
    "consumer_facing": "AI interacts directly with people",
    "generative": "AI generates synthetic text, images, audio or video",
    "emotion_biometric": "Uses emotion recognition or biometric categorisation",
    "public_body": "Public authority or private provider of public services",
    "non_eu_established": "Established outside the EU but serving the EU market",
    "international_transfers": "Transfers personal data across borders",
    "large_scale_processing": "Large-scale processing or systematic monitoring",
    "significant_data_fiduciary": "Notified as a Significant Data Fiduciary (India)",
    "real_world_testing": "Tests high-risk AI in real-world conditions",
}
ENTITY_FLAGS = [
    "importer", "distributor", "gpai_provider", "gpai_systemic", "special_category_data", "criminal_data",
    "children_data", "public_body", "non_eu_established", "international_transfers", "large_scale_processing",
    "significant_data_fiduciary", "real_world_testing",
]
JURISDICTIONS = {"EU": "European Union", "US": "United States (federal)", "US-CO": "Colorado, USA",
                 "US-NY": "New York City, USA", "IN": "India", "UK": "United Kingdom", "OTHER": "Other"}

# EU AI Act Art. 5 style practices (screening phrases)
PROHIBITED = {
    "social scoring": r"social scor",
    "subliminal or manipulative techniques": r"sublimin|manipulat\w* (technique|behaviou?r)|exploit\w* vulnerab",
    "untargeted facial image scraping": r"scrap\w* .{0,40}(facial|face) image|facial recognition database",
    "emotion recognition in workplace or education": r"emotion (recognition|detection|inference).{0,60}(workplace|employee|student|school|classroom)",
    "biometric categorisation by sensitive traits": r"biometric categori[sz]ation|infer\w* .{0,30}(race|religion|sexual orientation|political)",
    "predictive policing based on profiling": r"predict\w* .{0,40}(criminal|crime|offen[cs]e).{0,40}(profil|personality)",
    "real-time remote biometric identification in public": r"real[- ]time .{0,30}biometric identification",
}

# EU AI Act Annex III style areas (also drives "consequential decision" flags)
HIGH_RISK = {
    "biometrics": r"biometric|facial recognition|face recognition|emotion recognition",
    "critical infrastructure": r"critical infrastructure|power grid|water supply|traffic management|gas supply",
    "education": r"admission|exam (scoring|proctoring)|student assessment|grading of students|proctor",
    "employment": r"recruit|hiring|resume|cv screening|candidate|applicant tracking|promotion decision|termination|employee performance|workforce management|task allocation",
    "essential services": r"credit ?scor|creditworth|loan (approval|decision|underwriting)|underwriting|insurance (pricing|risk)|benefit eligibility|public assistance|emergency (call|dispatch)|tenant screening|housing",
    "law enforcement": r"law enforcement|police|recidivism|criminal risk|evidence reliability",
    "migration and border": r"migration|asylum|visa|border control",
    "justice and democracy": r"judicial|court|sentenc|election|voter",
    "healthcare / medical device": r"medical device|diagnos|clinical decision|triage|patient risk",
    "product safety component": r"safety component|machinery|vehicle|aviation|medical device",
}

EMPLOYMENT = re.compile(HIGH_RISK["employment"], re.I)
CONSEQUENTIAL = re.compile(
    "|".join([HIGH_RISK[k] for k in ("education", "employment", "essential services", "healthcare / medical device", "justice and democracy")])
    + r"|legal service|financial service|lending",
    re.I,
)
EMOTION_BIOMETRIC = re.compile(r"emotion (recognition|detection|inference)|biometric categori[sz]", re.I)
CREDIT_INSURANCE = re.compile(r"credit ?scor|creditworth|loan|lending|underwrit|(life|health) insurance|insurance pricing", re.I)
LIMITED = re.compile(r"chatbot|virtual assistant|conversational|deepfake|synthetic (media|content)|image generat|text generat|content generat", re.I)


def _text(s: AISystem) -> str:
    return " ".join([s.name, s.description, s.purpose, s.domain]).lower()


def classify_system(s: AISystem) -> tuple[str, str]:
    """Return (tier, rationale) from keyword screening."""
    t = _text(s)
    hits = [name for name, rx in PROHIBITED.items() if re.search(rx, t)]
    if hits:
        return "prohibited", "Screening matched potentially prohibited practice(s): " + "; ".join(hits) + ". Requires legal review."
    hits = [name for name, rx in HIGH_RISK.items() if re.search(rx, t)]
    if hits:
        return "high", "Matches high-risk area(s): " + "; ".join(hits) + "."
    if s.generative or s.consumer_facing or LIMITED.search(t):
        return "limited", "Interacts with people or generates content; transparency obligations apply."
    return "minimal", "No high-risk or transparency indicators found."


def classify_profile(profile: Profile) -> list[str]:
    """Set assessed_risk_tier on every system. Returns warnings."""
    warnings = []
    for s in profile.systems:
        tier, why = classify_system(s)
        if s.risk_tier and TIER_RANK[tier] > TIER_RANK[s.risk_tier]:
            warnings.append(
                f"System '{s.name}' is declared '{s.risk_tier}' but screening suggests '{tier}': {why} "
                "The stricter tier is used; confirm the classification."
            )
            s.assessed_risk_tier, s.risk_rationale = tier, why  # type: ignore[assignment]
        elif s.risk_tier:
            s.assessed_risk_tier = s.risk_tier
            s.risk_rationale = f"Declared in profile. Screening result: {tier}. {why}"
        else:
            s.assessed_risk_tier, s.risk_rationale = tier, why  # type: ignore[assignment]
        if s.assessed_risk_tier == "prohibited":
            warnings.append(f"System '{s.name}' may involve a prohibited practice. Stop and obtain legal review before any further use.")
    return warnings


def derive_flags(profile: Profile) -> set[str]:
    """Profile flags used by framework and requirement applicability rules."""
    flags: set[str] = {a for a in profile.entity.attributes if a in FLAG_LABELS}
    if "gpai_systemic" in flags:
        flags.add("gpai_provider")
    for s in profile.systems:
        t = _text(s)
        if s.assessed_risk_tier in ("high", "prohibited"):
            flags.add("high_risk")
        if s.uses_personal_data:
            flags.add("personal_data")
        if s.generative:
            flags.add("generative")
        if s.gpai_model_provider:
            flags.add("gpai_provider")
        if s.consumer_facing:
            flags.add("consumer_facing")
        if s.automated_decisions:
            flags.add("automated_decisions")
        if EMPLOYMENT.search(t):
            flags.add("employment")
        if CONSEQUENTIAL.search(t):
            flags.add("consequential_decisions")
        if CREDIT_INSURANCE.search(t):
            flags.update({"credit_or_insurance", "consequential_decisions"})
        if EMOTION_BIOMETRIC.search(t):
            flags.add("emotion_biometric")
        flags.add("provider" if s.role in ("provider", "both") else "deployer")
        if s.role == "both":
            flags.add("deployer")
    return flags


def framework_applies(fw: Framework, profile: Profile, flags: set[str]) -> tuple[bool, str]:
    juris = fw.applies_when.get("jurisdictions", [])
    need = fw.applies_when.get("flags", [])
    ent = [j.upper() for j in profile.entity.jurisdictions]
    if juris:
        # "US-CO" in profile satisfies rule "US-CO"; rule "EU" needs "EU" in profile.
        if not any(e == j or e.startswith(j + "-") for e in ent for j in juris):
            return False, f"Entity does not operate in {', '.join(juris)}."
    missing = [f for f in need if f not in flags]
    if missing:
        return False, "No system in scope has: " + ", ".join(m.replace("_", " ") for m in missing) + "."
    if not juris and not need:
        return True, "Voluntary global framework; assessed for every entity."
    parts = []
    if juris:
        parts.append("operates in " + "/".join(juris))
    if need:
        parts.append("has systems with " + ", ".join(n.replace("_", " ") for n in need))
    return True, "Entity " + " and ".join(parts) + "."


def requirement_applies(r: Requirement, flags: set[str]) -> tuple[bool, str]:
    if r.kind == "info":
        return False, "Reference provision: no obligation on the entity to test."
    missing = [f for f in r.need if f not in flags]
    if missing:
        return False, "Applies only to entities that: " + "; ".join(FLAG_LABELS.get(f, f).lower() for f in missing) + "."
    if r.when and not set(r.when) & flags:
        return False, "Applies only to entities that: " + " OR ".join(FLAG_LABELS.get(f, f).lower() for f in r.when) + "."
    return True, ""
