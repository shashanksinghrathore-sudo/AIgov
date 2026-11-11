"""MLflow Model Registry: pulls registered models and checks documentation hygiene.

config:
    url         MLflow tracking server base URL
    token_env   environment variable with a bearer token (optional)
"""
from __future__ import annotations

import json

from ..models import Evidence
from .base import Connector, register
from .http import fetch


@register("mlflow")
class MlflowConnector(Connector):
    def collect(self) -> list[Evidence]:
        base = self.config["url"].rstrip("/")
        models, token = [], ""
        try:
            while True:
                url = f"{base}/api/2.0/mlflow/registered-models/search?max_results=100" + (f"&page_token={token}" if token else "")
                page = json.loads(fetch(url, self.config.get("token_env")))
                models += page.get("registered_models", [])
                token = page.get("next_page_token", "")
                if not token:
                    break
        except Exception as e:
            self.warnings.append(f"mlflow: could not query {base}: {e}")
            return []

        described = 0
        owned = 0
        lines = [f"MLflow model registry at {base}: {len(models)} registered model(s)."]
        for m in models:
            tags = {t["key"].lower(): t.get("value", "") for t in m.get("tags", [])}
            desc = (m.get("description") or "").strip()
            owner = tags.get("owner") or tags.get("model_owner") or ""
            described += bool(desc)
            owned += bool(owner)
            versions = [f"v{v.get('version')}:{v.get('current_stage', '-')}" for v in m.get("latest_versions", [])]
            lines.append(
                f"- {m.get('name')} | versions={', '.join(versions) or '-'} | owner={owner or 'MISSING'} "
                f"| risk_tier={tags.get('risk_tier', 'MISSING')} | description={'yes' if desc else 'MISSING'}"
            )
        n = len(models)
        return [Evidence(
            id="mlflow:registry", connector="mlflow", kind="api", title="MLflow model registry", ref=base, text="\n".join(lines),
            signals={
                "experiment_tracking": True,
                "inventory_present": n > 0,
                "registry_models": n,
                "registry_described": described,
                "registry_owned": owned,
            },
        )]
