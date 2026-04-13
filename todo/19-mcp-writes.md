# 19 - mcp (writes)

**Goal:** Add write tools to the MCP server, using an append-only `inbox/` pattern to avoid concurrent-session merge conflicts.
**Depends on:** 16 (and after you've lived with read-only MCP for at least a week)

**In scope:**
- `propose_card(front, back, source)` tool — writes a single card to `inbox/cards/<timestamp>-<uuid>.jsonl`
- `add_inbox_note(title, body)` tool — writes a new note to `inbox/notes/<timestamp>-<uuid>.md`
- `inbox/` tree is append-only. Writes NEVER touch `cards.jsonl` or the main vault directly.
- New `kp reconcile` command:
  - Reads everything in `inbox/`
  - Feeds card proposals through the normal review queue (slice 07)
  - Folds inbox notes into the vault after user confirmation
  - Archives reconciled files to `inbox/processed/<date>/`
- Concurrency: timestamped + UUID'd filenames mean two simultaneous writes never collide

**Out of scope:**
- Bulk-edit tools (too dangerous)
- Deleting cards or notes via MCP (intentional: read-only memory + write-only inbox)

**Steps:**
1. Add write tools to server
2. Implement `kp reconcile`
3. Concurrency test: two parallel sessions writing simultaneously
4. Manual test from Claude Desktop + Claude Code

**Test:**

*Unit:*
- Two simultaneous writes produce distinct filenames, no race conditions
- `kp reconcile` correctly routes proposals to the review queue, notes to the vault
- Reconciled files land in `processed/` correctly

*Realism check (required):*
- From two parallel real Claude sessions, call `propose_card` simultaneously → both land in `inbox/cards/` with distinct filenames
- Run `kp reconcile` → both proposals flow through review into Anki
- Use it in a real learning conversation to propose cards from inside a chat

**Done when:**
- [ ] Parallel write test passes
- [ ] `kp reconcile` never touches `cards.jsonl` or the vault without user confirmation
- [ ] You've used it in a real Claude session to propose cards from inside a chat
