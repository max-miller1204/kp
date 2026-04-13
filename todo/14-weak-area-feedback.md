# 14 - weak area feedback

**Goal:** Query Anki for cards you keep failing and ask Claude to generate better/different cards on the same concepts. Closes the learning loop.
**Depends on:** 07

**In scope:**
- `kp weak-areas` command: queries AnkiConnect for cards with low retention (lapses > N, or retention < threshold)
- Groups struggling cards by `source_path` and `tags`
- Feeds each group into Claude with a prompt like: "the user keeps failing these cards — generate 3 new cards approaching the same concept from a different angle, OR reformulate existing cards more clearly"
- New proposals land in `_review.jsonl` with a `reason: "weak-area <group>"` annotation
- Thresholds configurable via `kp.toml`

**Out of scope:**
- Auto-suspending cards (user decides what to keep)
- Retention prediction / FSRS integration (future)

**Steps:**
1. AnkiConnect query wrapper for card stats (`getReviewsOfCards`, `findCards` + `cardsInfo`)
2. Grouping + filtering logic
3. `prompts/weak-area-v1.md`
4. CLI wiring
5. Tests with mocked AnkiConnect responses

**Test:**

*Unit:*
- Mock AnkiConnect stats response → grouping function produces expected groups
- Mock Claude SDK → proposals end up in `_review.jsonl` with `reason` populated

*Realism check (required):*
- Mark 5 fixture cards as failed in your real Anki (or use mocked stats for CI)
- Run `kp weak-areas`
- Verify new proposals reference the struggling concepts (not unrelated cards)
- `reason` field annotates which group each proposal came from

**Done when:**
- [ ] Real weak-area run against your actual deck produces useful-looking suggestions
- [ ] Proposals show up in the normal review queue so you can approve/reject
