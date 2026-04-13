# 06 - anki sink

**Goal:** Read `cards.jsonl` and push cards to Anki via AnkiConnect. `kp process` NEVER talks to Anki — only `kp sync-anki` does.
**Depends on:** 03

**In scope:**
- `kp/sinks/anki.py`: AnkiConnect HTTP client (`http://localhost:8765`)
- `addNote` wrapper supporting `basic` and `cloze` note types (cloze generation itself is slice 23 — just accept the type here)
- Auto-create target deck from `config.anki_deck`
- `storeMediaFile` helper (stub usage OK — real media arrives in slice 12)
- Every card's "Extra" field populated with clickable `obsidian://` link + `file://` source link
- `kp sync-anki [--dry-run] [--cards PATH]` CLI command
  - `--dry-run` prints what would be sent, never calls AnkiConnect
  - Clean error if Anki isn't running (no data loss, no partial sync)
- Duplicate handling: if a card with the same `id` was already added, skip

**Out of scope:**
- `kp process` touching Anki at all (intentional separation)
- Card suspension, scheduling, tag routing beyond source-file tag
- Occlusion note type (slice 20)

**Steps:**
1. AnkiConnect client with request helper
2. `addNote` for basic + cloze
3. `sync_cards(cards, deck, dry_run)` top-level function
4. CLI wiring
5. Tests: unit-test the request payload builder; integration test behind `@pytest.mark.anki` marker that only runs if `ANKI_CONNECT_TEST=1`

**Test:**
- Unit: `build_addNote_request(card)` produces expected JSON for basic + cloze
- Unit: `--dry-run` never hits the network (mock httpx/urllib)
- Unit: AnkiConnect error → clean exception, no partial state
- Integration (manual / marked): push 1 basic + 1 cloze card to `KP::Inbox` with Anki running; verify in Anki GUI that cards exist and Extra links open correctly
- Running sync twice → duplicates detected, not re-added

**Done when:**
- [ ] All unit tests pass
- [ ] Manual integration test against real Anki passes for both note types
- [ ] `kp process` source code has zero references to AnkiConnect
