# 17 - prompt evals

**Goal:** Harness for measuring synthesis quality so prompt iteration doesn't silently regress. ⚠️ Fixtures must come from REAL usage, not synthetic.
**Depends on:** 08 + at least a week of real usage after slice 10

**In scope:**
- `prompts/eval/` directory with:
  - `inputs/` — real markdown/image files you've actually processed, copied verbatim from your knowledge repo
  - `golden/` — last-known-good card output for each input (JSONL matching `cards.jsonl` shape)
- `kp eval` command:
  - Runs current prompt against every input
  - Diffs output against golden
  - Prints: unchanged / added / removed / modified counts + full diff of changed cards
  - `--accept` flag promotes current output to new golden
- Runs against the same model + temperature so diffs reflect prompt changes, not sampling noise
- Usage log tags eval runs with `slice: eval` so you can see how much the harness costs

**Out of scope:**
- LLM-as-judge quality scoring (future idea, not this slice)
- Cross-model comparisons

**Critical:**
- Fixtures MUST be real. Synthetic fixtures test what you *think* the tool will see, not what it *actually* sees. If you can't wait the week, you're not ready for this slice.

**Steps:**
1. After at least a week of real usage, pick 8-12 representative inputs from your knowledge repo
2. Copy them into `prompts/eval/inputs/`
3. Run current prompt, accept output as first golden
4. Build the `kp eval` command + diff printer

**Test:**
- Change `prompts/v1.md` intentionally (e.g. add a sentence) → `kp eval` shows diffs across the fixtures
- `kp eval --accept` → diffs become new golden, re-run is clean
- Fresh clone of the repo + `kp eval` → deterministic results (same cards from same inputs)

**Done when:**
- [ ] Fixtures are real files from your actual usage, not invented
- [ ] Eval diff output is clear enough to scan in ~30 seconds
- [ ] Cost of one full eval run is logged and acceptable (single-digit dollars)
