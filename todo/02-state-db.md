# 02 - state db

**Goal:** Local-only sqlite module that tracks which source files produced which cards, with rename + delete handling.
**Depends on:** 01

**In scope:**
- `kp/state.py`: sqlite schema `(path TEXT, content_hash TEXT, card_ids JSON, updated_at)`
- DB lives at `$XDG_DATA_HOME/kp/state.db` (fallback `~/.local/share/kp/state.db`); **never committed**
- API: `upsert(path, content_hash, card_ids)`, `get(path)`, `find_by_hash(content_hash)`, `all_paths()`, `delete(path)`
- Rename detection: same hash, different path → reuse card IDs, update path
- `kp orphans` CLI command: lists `(path, card_ids)` for files that no longer exist on disk

**Out of scope:**
- Auto-deleting cards from Anki (report only)
- Any Claude / AnkiConnect / Obsidian I/O

**Steps:**
1. `kp/state.py` with sqlite init + CRUD
2. Rename/delete logic
3. Wire `kp orphans` into `cli.py`
4. Tests in `tests/test_state.py`

**Test:**
- Unit: insert → lookup → update → round-trip
- Rename: insert `a.md` hash=X, then `b.md` hash=X → second call reuses card_ids, `get("a.md")` returns None, `get("b.md")` returns same IDs
- Delete: insert `a.md`, remove file from disk, `kp orphans` lists `a.md` and its cards
- DB path respects `$XDG_DATA_HOME` override via monkeypatch

**Done when:**
- [ ] All state tests pass
- [ ] `kp orphans` works against a temp DB + temp source tree
- [ ] State DB is in `.gitignore` (or lives outside repo entirely)
