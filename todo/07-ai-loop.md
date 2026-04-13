# 07 - ai loop

**Goal:** Add AI card generation on top of the walking skeleton, with a review queue gating AI output from the main deck. Thin slice complete after this. 🎯 SECOND STOP-AND-USE-IT GATE.
**Depends on:** 06

**⚠️ Bundle warning:** This slice intentionally bundles what used to be three separate slices (old 08 claude-synthesize + 09 review-queue + 10 pipeline-ai). Do NOT split across worktrees — the synthesis output format, the review queue format, and the pipeline routing all share one contract and must ship together.

**In scope:**

*Synthesis (`kp/synthesize.py`):*
- `propose_cards(text: str, source_path: str) -> list[Card]`: one Anthropic SDK call, API key from `config.claude_api_key_env`
- Prompt lives in `prompts/v1.md` (versioned file, read at runtime, not hardcoded)
- **Basic Q/A cards only** — cloze generation is slice 20
- Prompt caching enabled
- Returns `Card` records with `card_type="basic"` and populated source metadata

*Usage tracking (`kp/usage.py`):*
- Each synthesis call appends a row to `$XDG_DATA_HOME/kp/usage.log`: `{timestamp, slice, model, input_tokens, output_tokens, cache_read_tokens, estimated_cost}`
- `kp usage` CLI command summarizes totals (today, week, all-time) with rough cost estimate
- `--dry-run` flag on `kp process` prints the full prompt + estimated input tokens, does NOT call the API, does NOT append to `usage.log`

*Review queue:*
- `_review.jsonl` format lives at `<repo>/generated/anki/_review.jsonl`; same shape as `cards.jsonl` with an additional `approved: bool | None` field
- `kp review` command opens `_review.jsonl` in `$EDITOR` (fallback to `vi`) with a short instructions header; on save, approved cards move into `cards.jsonl`, rejected/unmarked cards archive to `_review_rejected.jsonl`
- Explicit `#flashcard` cards continue to flow directly to `cards.jsonl` — they bypass review (already trusted)

*Pipeline wiring:*
- `kp process` runs `extract_explicit` AND `propose_cards` on each changed markdown file
- Explicit → `cards.jsonl` directly
- AI-proposed → `_review.jsonl`
- `kp sync-anki` (from slice 06) is unchanged — it just reads `cards.jsonl`

**Out of scope:**
- Everything Phase 3 and beyond (images, prompt evals, GitHub Action, daemon, etc.)
- Cloze generation (slice 20)
- LLM-as-judge card quality scoring

**Steps:**
1. Add `anthropic` dep to `pyproject.toml`
2. Write `prompts/v1.md` — a first-draft Q/A card generation prompt
3. Implement `kp/synthesize.py` with SDK call + JSON parsing
4. Implement `kp/usage.py` with log writer and `kp usage` command
5. Implement `--dry-run` flag plumbing through `kp process`
6. Implement `_review.jsonl` read/write helpers (reuse slice 03's writer with the extra field)
7. Implement `kp review` command using `$EDITOR`
8. Wire `kp process` to route explicit vs AI cards appropriately
9. Update / extend the slice 06 fixture repo to include paragraph-shaped content (not just `#flashcard` blocks) so synthesize has something to work with
10. Run full integration

**Test:**

*Unit:*
- Mock the SDK: `propose_cards` parses a JSON response into `Card` records correctly
- Mock the SDK: each call appends exactly one row to a temp `usage.log`
- `--dry-run` does NOT call the SDK, does NOT append to `usage.log`
- Review queue round-trip: write 3 proposals, mark 2 approved, apply → 2 in `cards.jsonl`, 1 archived

*Realism check (required):*
- Integration test: run `kp process` against the realistic fixture repo from slice 06 using absolute paths
- Verify: explicit cards land directly in `cards.jsonl`, AI proposals land in `_review.jsonl`, both use correct `source_path` / `source_line` / `backlinks`
- Run `kp review` with a scripted editor ("$EDITOR" set to a shell script that flips `approved: true` on 2 of 3 proposals)
- After approval: 2 approved cards joined the explicit cards in `cards.jsonl`
- `kp sync-anki` → all expected cards reach Anki (manual step)

*Manual (requires API key + Anki):*
- Run the full 7-step thin-slice verification from the main plan against your own knowledge repo (not a fixture):
  1. Create a `knowledge/` repo with 3 markdown notes, one containing explicit `#flashcard`
  2. `kp process knowledge/`
  3. `kp review` → approve some AI proposals
  4. `kp sync-anki` → cards in `KP::Inbox`
  5. `kp sync-obsidian ~/ObsidianVault` → vault updated
  6. Check `kp usage` → reasonable cost
  7. Re-run `kp process` → state DB skips unchanged files

**Done when:**
- [ ] All unit tests pass
- [ ] Realism-check integration tests pass
- [ ] Full 7-step manual verification passes against real content
- [ ] `kp usage` output is readable and accurate
- [ ] Prompt lives in `prompts/v1.md`, not inline in `synthesize.py`
- [ ] 🎯 **THIN SLICE COMPLETE.** Commit, then use the tool on real content for at least a week before starting any Phase 3 slice. This gate is where you accumulate the real fixtures that slice 13 (prompt evals) will need.
