from __future__ import annotations

from pathlib import Path

import pytest

from kp import state
from kp.cli import main
from kp.state import StateDB, default_db_path


@pytest.fixture()
def db(tmp_path: Path) -> StateDB:
    return StateDB(tmp_path / "state.db")


def test_default_db_path_respects_xdg(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    assert default_db_path() == tmp_path / "kp" / "state.db"


def test_default_db_path_fallback(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.delenv("XDG_DATA_HOME", raising=False)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))  # type: ignore[arg-type]
    assert default_db_path() == tmp_path / ".local" / "share" / "kp" / "state.db"


def test_insert_lookup_update_roundtrip(db: StateDB):
    row = db.upsert("/a.md", "hashA", ["1", "2"])
    assert row.card_ids == ["1", "2"]

    got = db.get("/a.md")
    assert got is not None
    assert got.content_hash == "hashA"
    assert got.card_ids == ["1", "2"]

    db.upsert("/a.md", "hashA2", ["1", "2", "3"])
    got = db.get("/a.md")
    assert got is not None
    assert got.content_hash == "hashA2"
    assert got.card_ids == ["1", "2", "3"]

    assert db.all_paths() == ["/a.md"]


def test_find_by_hash(db: StateDB):
    db.upsert("/a.md", "H", ["1"])
    found = db.find_by_hash("H")
    assert [r.path for r in found] == ["/a.md"]
    assert db.find_by_hash("missing") == []


def test_delete(db: StateDB):
    db.upsert("/a.md", "H", ["1"])
    db.delete("/a.md")
    assert db.get("/a.md") is None
    assert db.all_paths() == []


def test_rename_reuses_card_ids(db: StateDB):
    db.upsert("/a.md", "HX", ["c1", "c2"])
    db.upsert("/b.md", "HX", [])

    assert db.get("/a.md") is None
    got = db.get("/b.md")
    assert got is not None
    assert got.card_ids == ["c1", "c2"]
    assert got.content_hash == "HX"
    assert db.all_paths() == ["/b.md"]


def test_orphans(tmp_path: Path, db: StateDB):
    alive = tmp_path / "alive.md"
    alive.write_text("x")
    dead = tmp_path / "dead.md"

    db.upsert(str(alive), "h1", ["1"])
    db.upsert(str(dead), "h2", ["2", "3"])

    orphans = db.orphans()
    assert [r.path for r in orphans] == [str(dead)]
    assert orphans[0].card_ids == ["2", "3"]


def test_orphans_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    db_path = tmp_path / "state.db"
    alive = tmp_path / "alive.md"
    alive.write_text("x")
    dead = tmp_path / "dead.md"

    with StateDB(db_path) as db:
        db.upsert(str(alive), "h1", ["1"])
        db.upsert(str(dead), "h2", ["7", "8"])

    rc = main(["orphans", "--db", str(db_path)])
    assert rc == 0
    out = capsys.readouterr().out
    assert str(dead) in out
    assert "7,8" in out
    assert str(alive) not in out


def test_orphans_cli_empty(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    db_path = tmp_path / "state.db"
    StateDB(db_path).close()
    rc = main(["orphans", "--db", str(db_path)])
    assert rc == 0
    assert "no orphans" in capsys.readouterr().out


def test_db_file_created_in_xdg(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    path = state.default_db_path()
    with StateDB(path) as db:
        db.upsert("/x", "h", ["1"])
    assert path.exists()
