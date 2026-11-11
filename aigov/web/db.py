"""SQLite storage for the web platform (standard library only)."""
from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS entities (id TEXT PRIMARY KEY, data TEXT NOT NULL, created TEXT, updated TEXT);
CREATE TABLE IF NOT EXISTS evidence (
  id TEXT PRIMARY KEY, entity_id TEXT NOT NULL, ev_id TEXT NOT NULL, title TEXT, kind TEXT, connector TEXT,
  text TEXT, signals TEXT, size INTEGER, created TEXT);
CREATE TABLE IF NOT EXISTS answers (
  entity_id TEXT NOT NULL, test_id TEXT NOT NULL, answer TEXT NOT NULL, note TEXT, evidence_ref TEXT, updated TEXT,
  PRIMARY KEY (entity_id, test_id));
CREATE TABLE IF NOT EXISTS assessments (id TEXT PRIMARY KEY, entity_id TEXT NOT NULL, created TEXT, overall REAL, data TEXT);
CREATE TABLE IF NOT EXISTS rules (id TEXT PRIMARY KEY, data TEXT NOT NULL, created TEXT, updated TEXT);
CREATE INDEX IF NOT EXISTS ix_ev_entity ON evidence(entity_id);
CREATE INDEX IF NOT EXISTS ix_as_entity ON assessments(entity_id);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class DB:
    def __init__(self, path: str | Path):
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.Lock()
        with self.lock:
            self.conn.executescript(SCHEMA)

    def q(self, sql: str, args: tuple = ()) -> list[sqlite3.Row]:
        with self.lock:
            cur = self.conn.execute(sql, args)
            rows = cur.fetchall()
            self.conn.commit()
            return rows

    # ---------------------------------------------------------------- entities
    def list_entities(self) -> list[dict]:
        out = []
        for r in self.q("SELECT * FROM entities ORDER BY updated DESC"):
            d = json.loads(r["data"])
            last = self.q("SELECT id, created, overall FROM assessments WHERE entity_id=? ORDER BY created DESC LIMIT 1", (r["id"],))
            n_ev = self.q("SELECT COUNT(*) c FROM evidence WHERE entity_id=?", (r["id"],))[0]["c"]
            n_ans = self.q("SELECT COUNT(*) c FROM answers WHERE entity_id=?", (r["id"],))[0]["c"]
            out.append({"id": r["id"], "updated": r["updated"], "profile": d, "evidence": n_ev, "answers": n_ans,
                        "last_assessment": dict(last[0]) if last else None})
        return out

    def get_entity(self, eid: str) -> dict | None:
        rows = self.q("SELECT data FROM entities WHERE id=?", (eid,))
        return json.loads(rows[0]["data"]) if rows else None

    def save_entity(self, profile: dict, eid: str | None = None) -> str:
        eid = eid or uuid.uuid4().hex[:10]
        if self.get_entity(eid) is None:
            self.q("INSERT INTO entities VALUES (?,?,?,?)", (eid, json.dumps(profile), now(), now()))
        else:
            self.q("UPDATE entities SET data=?, updated=? WHERE id=?", (json.dumps(profile), now(), eid))
        return eid

    def touch(self, eid: str) -> None:
        self.q("UPDATE entities SET updated=? WHERE id=?", (now(), eid))

    def delete_entity(self, eid: str) -> None:
        for t in ("evidence", "answers", "assessments"):
            self.q(f"DELETE FROM {t} WHERE entity_id=?", (eid,))  # noqa: S608 (fixed table names)
        self.q("DELETE FROM entities WHERE id=?", (eid,))

    # ---------------------------------------------------------------- evidence
    def add_evidence(self, eid: str, ev: dict) -> dict:
        taken = {r["ev_id"] for r in self.q("SELECT ev_id FROM evidence WHERE entity_id=?", (eid,))}
        base, n, ev_id = ev["id"], 2, ev["id"]
        while ev_id in taken:
            ev_id, n = f"{base}#{n}", n + 1
        rid = uuid.uuid4().hex[:12]
        self.q("INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?,?)", (
            rid, eid, ev_id, ev["title"], ev["kind"], ev["connector"], ev.get("text", ""),
            json.dumps(ev.get("signals", {})), len(ev.get("text", "")), now()))
        self.touch(eid)
        return {"id": rid, "ev_id": ev_id, "title": ev["title"], "kind": ev["kind"]}

    def list_evidence(self, eid: str, with_text: bool = False) -> list[dict]:
        out = []
        for r in self.q("SELECT * FROM evidence WHERE entity_id=? ORDER BY created", (eid,)):
            d = {k: r[k] for k in ("id", "ev_id", "title", "kind", "connector", "size", "created")}
            d["signals"] = json.loads(r["signals"] or "{}")
            if with_text:
                d["text"] = r["text"]
            else:
                d["preview"] = (r["text"] or "")[:300]
            out.append(d)
        return out

    def delete_evidence(self, eid: str, rid: str) -> bool:
        found = self.q("SELECT id FROM evidence WHERE entity_id=? AND id=?", (eid, rid))
        self.q("DELETE FROM evidence WHERE entity_id=? AND id=?", (eid, rid))
        return bool(found)

    # ---------------------------------------------------------------- answers
    def get_answers(self, eid: str) -> list[dict]:
        return [dict(r) for r in self.q("SELECT test_id, answer, note, evidence_ref, updated FROM answers WHERE entity_id=?", (eid,))]

    def put_answer(self, eid: str, test_id: str, answer: str | None, note: str = "", evidence_ref: str = "") -> None:
        if answer is None:
            self.q("DELETE FROM answers WHERE entity_id=? AND test_id=?", (eid, test_id))
        else:
            self.q("INSERT INTO answers VALUES (?,?,?,?,?,?) ON CONFLICT(entity_id, test_id) DO UPDATE SET "
                   "answer=excluded.answer, note=excluded.note, evidence_ref=excluded.evidence_ref, updated=excluded.updated",
                   (eid, test_id, answer, note, evidence_ref, now()))

    # ---------------------------------------------------------------- assessments
    def save_assessment(self, eid: str, aid: str, overall: float, data: str) -> None:
        self.q("INSERT INTO assessments VALUES (?,?,?,?,?)", (aid, eid, now(), overall, data))
        self.touch(eid)

    def list_assessments(self, eid: str) -> list[dict]:
        return [dict(r) for r in self.q("SELECT id, created, overall FROM assessments WHERE entity_id=? ORDER BY created DESC", (eid,))]

    def get_assessment(self, aid: str) -> str | None:
        rows = self.q("SELECT data FROM assessments WHERE id=?", (aid,))
        return rows[0]["data"] if rows else None

    # ---------------------------------------------------------------- custom rules
    def list_rules(self) -> list[dict]:
        return [json.loads(r["data"]) for r in self.q("SELECT data FROM rules ORDER BY created")]

    def save_rule(self, rid: str, data: dict) -> None:
        if self.q("SELECT id FROM rules WHERE id=?", (rid,)):
            self.q("UPDATE rules SET data=?, updated=? WHERE id=?", (json.dumps(data), now(), rid))
        else:
            self.q("INSERT INTO rules VALUES (?,?,?,?)", (rid, json.dumps(data), now(), now()))

    def delete_rule(self, rid: str) -> bool:
        found = self.q("SELECT id FROM rules WHERE id=?", (rid,))
        self.q("DELETE FROM rules WHERE id=?", (rid,))
        return bool(found)
