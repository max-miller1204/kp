# 09 - review queue

**Goal:** AI-proposed cards land in a review queue instead of straight in `cards.jsonl`. User approves before anything goes to Anki.
**Depends on:** 03

**In scope:**
- `generated/anki/_review.jsonl` format (same shape as `cards.jsonl` but with an `approved: bool` field defaulting to None)
- `kp review` command — opens `_review.jsonl` in `$EDITOR` with instructions at the top; user edits `approved: true` on cards they want to keep
- On save, `kp review` reads the file, moves approved cards to `cards.jsonl`, leaves the rest alone (or moves rejected ones to `_review_rejected.jsonl` archive)
- TUI can come later; `$EDITOR` is fine for v1

**Out of scope:**
- TUI / fancy interactive review
- Bulk-approve commands
- Editing card contents during review (v2 — just approve/reject for now)

**Steps:**
1. Extend `Card` / JSONL helpers with an `approved` field for review records
2. `kp review` implementation with $EDITOR
3. Tests

**Test:**
- Write 3 records to a temp `_review.jsonl`, simulate editing 2 to `approved: true`, run the approval step
- Verify: 2 cards now in `cards.jsonl`, `_review.jsonl` is clean (empty or contains only un-actioned rows)
- Rejected cards archive is populated correctly

**Done when:**
- [ ] Approval loop round-trips correctly
- [ ] Running approval on an empty queue is a clean no-op
- [ ] `$EDITOR` fallback to `vi` if unset
