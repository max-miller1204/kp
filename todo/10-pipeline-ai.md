# 10 - pipeline (ai)

**Goal:** Wire AI synthesis into `kp process`. End-to-end: markdown → Claude → review queue → Anki + Obsidian. 🎯 SECOND STOP-AND-USE-IT GATE — thin slice complete.
**Depends on:** 07, 08, 09

**In scope:**
- `kp process` now runs 08's `propose_cards` on each changed markdown file alongside the explicit extractor
- Explicit cards → `cards.jsonl` directly (they're already trusted)
- AI-proposed cards → `_review.jsonl` (need approval)
- `kp review` → approved cards flow into `cards.jsonl`
- `kp sync-anki` → pushes to deck
- `kp sync-obsidian` → updates vault

**Out of scope:**
- Everything after slice 10 (that's v2)

**Steps:**
1. Update `kp process` to call synthesize for AI cards
2. Route explicit → `cards.jsonl`, AI → `_review.jsonl`
3. Verify the thin-slice verification steps (1-7) from the plan all pass

**Test:**
- Run the full 7-step thin-slice verification sequence from the main plan
- Specifically: 3 markdown files, 1 with explicit `#flashcard`, 2 without. After `kp process` + `kp review` (approve 2 of N proposed cards) + sync: deck has 1 explicit card + 2 approved AI cards; vault has 3 generated notes

**Done when:**
- [ ] Full 7-step verification passes
- [ ] 🎯 **THIN SLICE COMPLETE.** Commit, then actually use the tool for at least a week on real content before starting any v2 slice. This gate exists for a reason.
