# 23 - cloze generation

**Goal:** Add cloze-deletion card generation to synthesis. MUST come after prompt evals (17) so quality is measurable.
**Depends on:** 17

**Why this is a separate slice (not part of 08):**
Getting basic Q/A cards right is already prompt-hard. Mixing cloze in before evals exist means you can't tell whether cloze output is any good, AND you can't tell whether adding it regressed basic cards. Evals let you measure both.

**In scope:**
- `prompts/cloze-v1.md` — prompt variant for cloze-deletion cards
- `synthesize.py` now produces both `basic` AND `cloze` cards; prompt decides which shape fits the content
- Cloze card format: `{{c1::term1}} ... {{c2::term2}}` using Anki's native cloze syntax (already supported by sink in slice 06)
- Update `kp eval` fixtures with cloze examples after verifying quality

**Out of scope:**
- Image cloze (slice 20 / future)
- Cloze-only mode (mixed basic + cloze is intentional)

**Steps:**
1. Run `kp eval` → snapshot current (basic-only) output as baseline
2. Write `prompts/cloze-v1.md`
3. Update `synthesize.propose_cards` to return mixed types
4. Run `kp eval` → verify basic card output is unchanged (no regression)
5. Manually review the new cloze cards on the eval fixtures — are they good?
6. If yes, `kp eval --accept` the new golden

**Test:**
- Baseline eval before change: N basic cards
- Eval after change: same N basic cards unchanged + M cloze cards on paragraph fixtures
- Cloze cards use correct `{{cN::...}}` syntax
- Manual quality check: cloze cards test load-bearing facts, not trivia

**Done when:**
- [ ] No regression in basic card quality (per eval diff)
- [ ] Cloze cards produced on paragraph fixtures are actually useful to study
- [ ] New golden accepted
