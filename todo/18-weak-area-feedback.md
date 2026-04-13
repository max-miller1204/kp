# 18 - weak area feedback

**Goal:** Query Anki for cards you keep failing and ask Claude to generate better/different cards on the same concepts. Closes the learning loop.
**Depends on:** 10

**In scope:**
- `kp weak-areas` command: queries AnkiConnect for cards with low retention (lapses > N, or retention < threshold)
- Groups struggling cards by `source_path` and `tags`
- Feeds each group into Claude with a prompt like: "the user keeps failing these cards — generate 3 new cards approaching the same concept from a different angle, OR reformulate existing cards more clearly"
- New proposals land in `_review.jsonl` with a `reason: "weak-area <group>"` annotation
- Configurable threshold in `kp.toml`

**Out of scope:**
- Auto-suspending cards (user decides what to keep)
- Retention prediction / FSRS integration

**Steps:**
1. AnkiConnect query wrapper for card stats
2. Grouping + filtering logic
3. `prompts/weak-area-v1.md`
4. CLI wiring
5. Tests with mocked AnkiConnect responses

**Test:**
- Mark 5 fixture cards as failed in Anki (or mock the stats response)
- Run `kp weak-areas`
- Verify new proposals in `_review.jsonl` that reference the struggling concepts
- `reason` field is populated correctly

**Done when:**
- [ ] Real weak-area run against your actual deck produces useful-looking suggestions
- [ ] Proposals show up in the normal review queue so you can approve/reject
