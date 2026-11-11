"""Policy and procedure documents from a folder (Markdown, text, PDF, DOCX, YAML, JSON)."""
from __future__ import annotations

from pathlib import Path

from ..models import Evidence
from .base import Connector, register

TEXT_EXT = {".md", ".txt", ".rst", ".yaml", ".yml", ".json", ".csv", ".html"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def _read(path: Path) -> str | None:
    ext = path.suffix.lower()
    if ext in TEXT_EXT:
        return path.read_text(errors="replace")
    if ext == ".pdf":
        from pypdf import PdfReader  # optional dependency
        return "\n".join((p.extract_text() or "") for p in PdfReader(str(path)).pages)
    if ext == ".docx":
        import docx  # optional dependency (python-docx)
        return "\n".join(p.text for p in docx.Document(str(path)).paragraphs)
    return None


@register("documents")
class DocumentsConnector(Connector):
    """config: path (folder or file)"""

    def collect(self) -> list[Evidence]:
        root = Path(self.config["path"])
        if not root.exists():
            self.warnings.append(f"documents: path not found: {root}")
            return []
        files = [root] if root.is_file() else sorted(
            p for p in root.rglob("*") if p.is_file() and not (set(p.parts) & SKIP_DIRS)
        )
        out = []
        for p in files:
            try:
                text = _read(p)
            except ImportError as e:
                self.warnings.append(f"documents: skipped {p.name} (install '{e.name}' to read {p.suffix} files)")
                continue
            except Exception as e:  # unreadable file should not abort an assessment
                self.warnings.append(f"documents: could not read {p.name}: {e}")
                continue
            if text is None or not text.strip():
                continue
            rel = p.name if root.is_file() else str(p.relative_to(root))
            out.append(Evidence(id=f"doc:{rel}", connector="documents", kind="document", title=rel, ref=str(p), text=text))
        return out
