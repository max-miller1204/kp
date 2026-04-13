# 06 - walking skeleton (explicit loop)

**Goal:** Close the end-to-end loop for explicit `#flashcard` cards: markdown file → `cards.jsonl` → Anki + Obsidian. No AI yet. 🎯 FIRST STOP-AND-USE-IT GATE.
**Depends on:** 05

**⚠️ Bundle warning:** This slice intentionally bundles what used to be three separate slices (old 06 anki-sink + 07 pipeline-explicit). Do NOT split across worktrees — the Anki sink contract, pipeline wiring, and real-path handling must be designed together and tested against a single realistic fixture.

**In scope:**

*Anki sink (`kp/sinks/anki.py`):*
- AnkiConnect HTTP client (`http://localhost:8765`)
- `addNote` wrapper supporting `basic` and `cloze` note types (cloze generation itself is slice 20 — sink just needs to accept the type)
- Auto-create target deck from `config.anki_deck`
- `storeMediaFile` helper (stub usage OK — real media arrives in slice 09)
- Every card's "Extra" field gets a clickable `obsidian://` link to the generated note and a `file://` link to the source line
- Duplicate handling by card ID

*Pipeline (`kp/cli.py` additions):*
- `kp process <repo-path>`: walks the repo, handles only `.md` files, runs `extract_explicit` from slice 04, writes to `<repo>/generated/anki/cards.jsonl` and `<repo>/generated/obsidian/`
- Uses the state DB (slice 02) to skip files whose content hash is unchanged
- **Passes `repo_root=<repo-path>` to `write_note`** so subdirectory structure is preserved (this is the path-collision fix from the slice-05 audit)
- `kp sync-anki [--dry-run] [--cards PATH]`: reads `cards.jsonl`, pushes to AnkiConnect. NEVER called from `kp process`. Clean error if Anki is down, no partial sync.
- `kp sync-obsidian <vault-path>`: copies `<repo>/generated/obsidian/` into the real vault

**Out of scope:**
- AI synthesis (slice 07)
- Review queue (slice 07)
- Image / vision / other sources (Phase 3)
- GitHub Action (slice 08)

**Steps:**
1. Write `kp/sinks/anki.py` with the AnkiConnect client + `addNote` + deck auto-create
2. Write `sync_cards(cards_path, deck, *, dry_run)` top-level function
3. Wire `kp sync-anki` command
4. Write `kp process` walker that iterates `.md` files under the given repo path, calls `extract_explicit`, merges results into `cards.jsonl`, calls `write_note` with `repo_root=<repo-path>`, updates state DB
5. Wire `kp sync-obsidian` command
6. Build a **realistic fixture knowledge repo** under `tests/fixtures/knowledge-repo/` with:
   - At least 2 subdirectories (e.g., `topology/`, `algebra/`)
   - At least 3 `.md` files total, at least 2 with the same basename in different subdirs (to catch path collisions)
   - At least 2 files with explicit `#flashcard` blocks (mix single-line and multi-line)
   - At least one non-flashcard file (should be ignored cleanly)
7. Integration test runs the full pipeline against this fixture

**Test:**

*Unit:*
- `build_add_note_request(card)` produces expected JSON for basic + cloze note types
- Anki sink `--dry-run` never hits the network (mock httpx/urllib)
- Anki sink raises cleanly when AnkiConnect is unreachable (mock 500 / connection error)

*Realism check (required):*
- Integration test runs `kp process` against `tests/fixtures/knowledge-repo/` using **absolute paths** from `tmp_path`
- Verifies: `cards.jsonl` contains all explicit cards, obsidian notes land in the correct subdirectories (not collided at the root), state DB has entries for all processed files
- Run `kp process` twice → second run is a no-op (state DB skip)
- Touch one source file → only that file gets reprocessed
- Rename a source file (move it, same content) → rename detection kicks in, no duplicate cards
- `kp sync-anki --dry-run` against the generated `cards.jsonl` → prints expected requests without calling the network

*Manual (requires Anki):*
- Start Anki with AnkiConnect installed
- Run `kp sync-anki --cards <fixture>/generated/anki/cards.jsonl` → cards appear in `KP::Inbox` deck, Extra field links open the generated obsidian note and the source file
- Run twice → duplicate handling works, no double-insertion

**Done when:**
- [ ] All unit tests pass
- [ ] Realism-check integration tests pass
- [ ] Manual Anki test passes with real Anki
- [ ] `kp process` source code has zero references to `anki.py`
- [ ] Real run against your own knowledge notes produces sensible output
- [ ] 🎯 **Commit, then use it for at least a week on real content before starting slice 07.** This gate exists so you discover the ergonomic pain points before layering AI on top. Log frustrations in a scratch file to inform the AI-loop slice.
