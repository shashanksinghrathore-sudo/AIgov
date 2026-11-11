"""Generic REST pull: fetch JSON or text from any internal system (GRC tool, ticketing, wiki).

config:
    url          endpoint to GET
    title        label for the evidence
    token_env    name of an environment variable holding a bearer token (never put tokens in config)
    header       header name for the token (default "Authorization", sent as "Bearer <token>")
"""
from __future__ import annotations

import json
import os
import urllib.request

from ..models import Evidence
from .base import Connector, register


def fetch(url: str, token_env: str | None = None, header: str = "Authorization", timeout: int = 30) -> str:
    if not url.lower().startswith(("https://", "http://")):
        raise ValueError(f"unsupported URL scheme: {url}")
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "aigov"})
    token = os.environ.get(token_env or "", "")
    if token:
        req.add_header(header, f"Bearer {token}" if header == "Authorization" else token)
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (scheme checked above)
        return resp.read().decode("utf-8", errors="replace")


@register("http")
class HttpConnector(Connector):
    def collect(self) -> list[Evidence]:
        url = self.config["url"]
        try:
            body = fetch(url, self.config.get("token_env"), self.config.get("header", "Authorization"))
        except Exception as e:
            self.warnings.append(f"http: could not fetch {url}: {e}")
            return []
        try:
            body = json.dumps(json.loads(body), indent=1, sort_keys=True)
        except ValueError:
            pass
        title = self.config.get("title", url)
        return [Evidence(id=f"http:{title}", connector="http", kind="api", title=title, ref=url, text=body)]
