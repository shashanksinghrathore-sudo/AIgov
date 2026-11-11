"""Static scan of a source repository for AI governance signals.

Reads dependency manifests, file names and source text. It never executes repository code.
"""
from __future__ import annotations

import re
from pathlib import Path

from ..models import Evidence
from .base import Connector, register

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".tox", ".mypy_cache"}
MANIFESTS = {"requirements.txt", "pyproject.toml", "setup.py", "Pipfile", "environment.yml", "package.json", "poetry.lock", "uv.lock", "go.mod"}
LOCKFILES = {"poetry.lock", "uv.lock", "Pipfile.lock", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "requirements.lock"}
MODEL_EXT = {".pt", ".pth", ".onnx", ".pkl", ".joblib", ".h5", ".safetensors", ".gguf", ".pb", ".tflite"}
CODE_EXT = {".py", ".ipynb", ".js", ".ts", ".java", ".go", ".scala", ".r"}
MAX_FILE_BYTES = 400_000

# signal -> regex over dependency manifests + source code
LIB_SIGNALS = {
    "ml_deps": r"\b(torch|tensorflow|keras|scikit-learn|sklearn|xgboost|lightgbm|catboost|transformers|jax|onnxruntime|spacy)\b",
    "llm_usage": r"\b(anthropic|openai|langchain|llama[-_]index|litellm|cohere|google[-.]generativeai|vertexai|bedrock|ollama|mistralai)\b",
    "fairness_lib": r"\b(fairlearn|aif360|aequitas|themis-ml|fairness[-_]indicators)\b",
    "explainability_lib": r"\b(shap|lime|captum|interpret|alibi|eli5)\b",
    "monitoring_lib": r"\b(evidently|whylogs|nannyml|arize|fiddler|alibi[-_]detect|prometheus[-_]client|langfuse|langsmith|opentelemetry)\b",
    "experiment_tracking": r"\b(mlflow|wandb|neptune|comet[-_]ml|clearml|sagemaker)\b",
    "data_versioning": r"\b(dvc|lakefs|great[-_]expectations|pandera|deepchecks)\b",
    "pii_tooling": r"\b(presidio|scrubadub|opacus|diffprivlib|pydp)\b",
    "guardrails_lib": r"\b(guardrails[-_]ai|nemoguardrails|llm[-_]guard|rebuff|lakera|content[-_]safety|moderations?)\b",
    "adversarial_testing": r"\b(garak|pyrit|adversarial[-_]robustness[-_]toolbox|foolbox|textattack|cleverhans|promptfoo|giskard)\b",
    "logging_usage": r"\b(import logging|structlog|loguru|audit[-_ ]?log|logger\.(info|warning|error))\b",
}

# signal -> regex over relative file paths
FILE_SIGNALS = {
    "model_card": r"(^|/)(model[-_ ]?card|system[-_ ]?card)[^/]*\.(md|ya?ml|json)$",
    "datasheet": r"(^|/)(data[-_ ]?sheet|data[-_ ]?card|dataset[-_ ]?card)[^/]*\.(md|ya?ml|json)$",
    "tests": r"(^|/)(tests?|spec)/|(^|/)test_[^/]+\.py$|\.test\.(js|ts)$",
    "eval_scripts": r"(^|/)(evals?|evaluation|benchmarks?)(/|[-_][^/]*\.py$)|(^|/)evaluate[^/]*\.py$",
    "ci": r"^\.github/workflows/[^/]+\.ya?ml$|^\.gitlab-ci\.yml$|^Jenkinsfile$|^azure-pipelines\.yml$|^\.circleci/",
    "security_policy": r"(^|/)SECURITY\.md$",
    "codeowners": r"(^|/)CODEOWNERS$",
    "changelog": r"(^|/)(CHANGELOG|HISTORY|RELEASES)(\.md|\.rst|\.txt)?$",
    "license": r"^LICEN[SC]E(\.md|\.txt)?$",
    "risk_docs": r"(^|/)(risk[-_ ]?(assessment|register)|impact[-_ ]?assessment|dpia|fria)[^/]*\.(md|ya?ml|json|pdf|docx)$",
}

# governance documents inside a repo are worth reading in full
DOC_PATTERN = re.compile(r"(model[-_ ]?card|system[-_ ]?card|data[-_ ]?sheet|data[-_ ]?card|risk|impact[-_ ]?assessment|dpia|fria|SECURITY|GOVERNANCE)", re.I)
SECRET = re.compile(r"(sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC )?PRIVATE KEY-----)")


@register("repo")
class RepoConnector(Connector):
    """config: path (repository root)"""

    def collect(self) -> list[Evidence]:
        root = Path(self.config["path"])
        if not root.is_dir():
            self.warnings.append(f"repo: not a directory: {root}")
            return []
        name = root.resolve().name
        files = [p for p in root.rglob("*") if p.is_file() and not (set(p.relative_to(root).parts) & SKIP_DIRS)]
        rels = {p: p.relative_to(root).as_posix() for p in files}

        signals: dict[str, object] = {}
        found: dict[str, list[str]] = {}

        for sig, rx in FILE_SIGNALS.items():
            hits = [r for r in rels.values() if re.search(rx, r, re.I)]
            signals[sig] = bool(hits)
            if hits:
                found[sig] = hits[:5]

        artifacts = [r for p, r in rels.items() if p.suffix.lower() in MODEL_EXT]
        signals["model_artifacts"] = len(artifacts)
        signals["dependency_lock"] = any(p.name in LOCKFILES for p in files)

        secrets: list[str] = []
        docs: list[Evidence] = []
        for p, rel in rels.items():
            scannable = p.name in MANIFESTS or p.suffix.lower() in CODE_EXT
            is_doc = p.suffix.lower() in {".md", ".yaml", ".yml"} and DOC_PATTERN.search(p.name)
            if not (scannable or is_doc) or p.stat().st_size > MAX_FILE_BYTES:
                continue
            text = p.read_text(errors="replace")
            if is_doc:
                docs.append(Evidence(id=f"repo:{name}/{rel}", connector="repo", kind="document", title=f"{name}/{rel}", ref=str(p), text=text))
            if scannable:
                low = text.lower()
                for sig, rx in LIB_SIGNALS.items():
                    if re.search(rx, low):
                        signals[sig] = True
                        found.setdefault(sig, [])
                        if rel not in found[sig] and len(found[sig]) < 5:
                            found[sig].append(rel)
                if SECRET.search(text):
                    secrets.append(rel)
        for sig in LIB_SIGNALS:
            signals.setdefault(sig, False)
        signals["hardcoded_secrets"] = len(secrets)

        lines = [f"Static scan of repository '{name}' ({len(files)} files)."]
        for sig in sorted(signals):
            val = signals[sig]
            where = f" (e.g. {', '.join(found[sig])})" if found.get(sig) else ""
            lines.append(f"- {sig}: {val}{where}")
        if artifacts:
            lines.append("Model artifacts: " + ", ".join(artifacts[:10]))
        if secrets:
            lines.append("Possible hard-coded credentials in: " + ", ".join(secrets[:10]))
        summary = Evidence(
            id=f"repo:{name}", connector="repo", kind="repository", title=f"Repository scan: {name}",
            ref=str(root), text="\n".join(lines), signals=signals,
        )
        return [summary, *docs]
