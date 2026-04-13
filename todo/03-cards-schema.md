# 03 - cards schema

**Goal:** Define `cards.jsonl` record shape with ALL forward-looking fields present from day one.
**Depends on:** 01

**In scope:**
- `kp/cards.py`: `Card` dataclass with fields:
  - `id: str` (content-hash based)
  - `front: str`
  - `back: str`
  - `tags: list[str]`
  - `source_path: str`
  - `source_line: int | None`
  - `source_hash: str`
  - `media: list[str]` (empty list OK)
  - `card_type: Literal["basic", "cloze", "occlusion"]`
  - `backlinks: dict` with `{obsidian: str | None, source: str | None}`
  - `schema_version: int` (= 1)
- `write_cards(path, cards)` and `read_cards(path)` — JSONL
- Schema version check on read; fail loudly on unknown version

**Out of scope:**
- Actually generating any of these fields (sources do that)
- Validating card_type semantics beyond the Literal
- Migration logic (there's only v1)

**Steps:**
1. Define dataclass + serialization helpers
2. Write/read tests with fixtures for each card_type
3. Tests for schema version mismatch

**Test:**
- Write N records of each card_type (basic, cloze, occlusion) with populated `media` and `backlinks`
- Read back → fields round-trip exactly
- Reading a JSONL with `schema_version: 999` raises a clear error

**Done when:**
- [ ] Every field from the plan is in the dataclass
- [ ] Round-trip tests pass for all three card_types
- [ ] Schema version mismatch raises with a useful message
