# 13 - prompt evals

**Goal:** Harness for measuring synthesis quality so prompt iteration doesn't silently regress. ⚠️ Fixtures must come from REAL usage, not synthetic.
**Depends on:** 07 + at least a week of real usage

**In scope:**
- `prompts/eval/` directory with:
  - `inputs/` — real markdown/image/chat files you've actually processed, copied verbatim from your knowledge repo during slice 07's usage week
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

**Critical constraint:**
Fixtures MUST be real. Synthetic fixtures test what you *think* the tool will see; real fixtures test what it *actually* sees. If you haven't spent at least a week using the tool on your own notes after slice 07, you are not ready for this slice.

**Steps:**
1. After at least a week of real usage, pick 8-12 representative inputs from your knowledge repo
2. Copy them into `prompts/eval/inputs/`
3. Run current prompt, accept output as first golden
4. Build the `kp eval` command + diff printer
5. Document cost-per-run so you can budget iteration

**Test:**

*Realism check (required, and inherent):*
- Every input in `prompts/eval/inputs/` is a real file from your actual knowledge repo (this is the whole point of the slice)
- Change `prompts/v1.md` intentionally (e.g. add a sentence) → `kp eval` shows diffs across the fixtures
- `kp eval --accept` → diffs become new golden, re-run is clean
- Fresh clone of the repo + `kp eval` → deterministic results (same cards from same inputs, assuming fixed seed / temperature)

**Done when:**
- [ ] Fixtures are real files, not invented
- [ ] Eval diff output is clear enough to scan in ~30 seconds
- [ ] Cost of one full eval run is logged and acceptable (single-digit dollars)
