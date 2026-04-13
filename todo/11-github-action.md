# 11 - github action

**Goal:** GitHub Action runs `kp process` on push and commits the generated tree back.
**Depends on:** 10

**In scope:**
- `.github/workflows/kp.yml` triggered on push to `notes/**` (in the knowledge repo)
- Installs kp, runs `kp process .`, commits `generated/` back with a `[kp]` prefix message
- `ANTHROPIC_API_KEY` from repo secrets
- Runs on a self-hosted runner OR a GHA runner with Python — decide during implementation
- Does NOT push to AnkiConnect (CI can't reach your desktop) — only writes `generated/` tree

**Out of scope:**
- Anki sync from CI (impossible; daemon handles that)
- Slack / email notifications

**Steps:**
1. Write `kp.yml`
2. Test on a throwaway branch in a test knowledge repo
3. Wire secrets

**Test:**
- Push a change to `notes/test.md` in a test knowledge repo
- GHA run triggers, completes green
- New commit `[kp] update generated/` appears with updated `cards.jsonl` and `generated/obsidian/test.md`
- API cost is reasonable (check `kp usage` locally against the repo first)

**Done when:**
- [ ] End-to-end GHA run succeeds
- [ ] Committed generated/ diff is sensible
- [ ] Guardrail: CI skips processing if no `.md` files changed
