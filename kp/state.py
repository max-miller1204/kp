from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


@dataclass
class StateRow:
    path: str
    content_hash: str
    card_ids: list[str]
    updated_at: str


def default_db_path() -> Path:
    base = os.environ.get("XDG_DATA_HOME")
    root = Path(base) if base else Path.home() / ".local" / "share"
    return root / "kp" / "state.db"


_SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
    path TEXT PRIMARY KEY,
    content_hash TEXT NOT NULL,
    card_ids TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_files_hash ON files(content_hash);
"""


class StateDB:
    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path is not None else default_db_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "StateDB":
        return self

    def __exit__(self, *exc: object) -> None:
        del exc
        self.close()

    def _row_to_state(self, row: sqlite3.Row) -> StateRow:
        return StateRow(
            path=row["path"],
            content_hash=row["content_hash"],
            card_ids=json.loads(row["card_ids"]),
            updated_at=row["updated_at"],
        )

    def get(self, path: str) -> StateRow | None:
        cur = self._conn.execute("SELECT * FROM files WHERE path = ?", (str(path),))
        row = cur.fetchone()
        return self._row_to_state(row) if row else None

    def find_by_hash(self, content_hash: str) -> list[StateRow]:
        cur = self._conn.execute(
            "SELECT * FROM files WHERE content_hash = ?", (content_hash,)
        )
        return [self._row_to_state(r) for r in cur.fetchall()]

    def all_paths(self) -> list[str]:
        cur = self._conn.execute("SELECT path FROM files ORDER BY path")
        return [r["path"] for r in cur.fetchall()]

    def all_rows(self) -> list[StateRow]:
        cur = self._conn.execute("SELECT * FROM files ORDER BY path")
        return [self._row_to_state(r) for r in cur.fetchall()]

    def delete(self, path: str) -> None:
        self._conn.execute("DELETE FROM files WHERE path = ?", (str(path),))
        self._conn.commit()

    def upsert(
        self, path: str, content_hash: str, card_ids: list[str]
    ) -> StateRow:
        path = str(path)
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")

        existing_at_path = self.get(path)
        if existing_at_path is None:
            matches = [
                r for r in self.find_by_hash(content_hash) if r.path != path
            ]
            if matches:
                old = matches[0]
                merged = card_ids if card_ids else old.card_ids
                self._conn.execute("DELETE FROM files WHERE path = ?", (old.path,))
                self._conn.execute(
                    "INSERT INTO files(path, content_hash, card_ids, updated_at)"
                    " VALUES (?, ?, ?, ?)",
                    (path, content_hash, json.dumps(merged), now),
                )
                self._conn.commit()
                return StateRow(path, content_hash, merged, now)

        merged = card_ids
        if existing_at_path and not card_ids:
            merged = existing_at_path.card_ids
        self._conn.execute(
            "INSERT INTO files(path, content_hash, card_ids, updated_at)"
            " VALUES (?, ?, ?, ?)"
            " ON CONFLICT(path) DO UPDATE SET"
            "  content_hash = excluded.content_hash,"
            "  card_ids = excluded.card_ids,"
            "  updated_at = excluded.updated_at",
            (path, content_hash, json.dumps(merged), now),
        )
        self._conn.commit()
        return StateRow(path, content_hash, merged, now)

    def orphans(self) -> list[StateRow]:
        return [r for r in self.all_rows() if not Path(r.path).exists()]


@contextmanager
def open_state(path: Path | None = None) -> Iterator[StateDB]:
    db = StateDB(path)
    try:
        yield db
    finally:
        db.close()
