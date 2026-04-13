# 07 - pipeline (explicit)

**Goal:** End-to-end: markdown with `#flashcard` → Obsidian note + Anki card. Explicit-only mode. 🎯 FIRST STOP-AND-USE-IT GATE.
**Depends on:** 04, 05, 06

**In scope:**
- `kp process <repo-path>`: walks the repo, processes `.md` files, runs 04's explicit extractor, writes to `generated/anki/cards.jsonl` and `generated/obsidian/`
- Skips unchanged files using state DB (slice 02)
- Still NO Claude API calls, NO AI
- `kp sync-obsidian <vault-path>`: copies `generated/obsidian/` tree into the real vault
- Wire `kp sync-anki` (from slice 06) as the last step

**Out of scope:**
- AI mode (slice 08-10)
- GitHub Action (slice 11)
- Daemon / watch mode (slice 14)

**Steps:**
1. Implement `kp process` walker
2. Implement `kp sync-obsidian`
3. Create a test knowledge repo with 3 markdown files, one containing explicit `#flashcard` blocks
4. Run the full acceptance sequence manually

**Test:**
1. `kp process ./test-knowledge/` → new files appear in `./test-knowledge/generated/obsidian/` and `cards.jsonl` has the explicit cards
2. `kp sync-obsidian ~/ObsidianVault` → vault updated, notes visible in Obsidian
3. `kp sync-anki` → cards appear in `KP::Inbox` deck
4. Re-run `kp process` → no changes (state DB skips unchanged files)

**Done when:**
- [ ] All 4 manual acceptance steps pass
- [ ] 🎯 You commit and then **actually use the tool for at least a week before starting slice 08**. Feed real notes through it. Note frustrations in a scratch file.
