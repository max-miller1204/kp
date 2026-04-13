# 08 - github action

**Goal:** GitHub Action runs `kp process` on push to the knowledge repo and commits the generated tree back.
**Depends on:** 07

**In scope:**
- `.github/workflows/kp.yml` triggered on push to `notes/**` (or whatever source patterns you settle on) in a knowledge repo
- Installs kp (either via `pip install git+https://...` from this repo, or a published wheel — decide during implementation), runs `kp process .`, commits `generated/` back with a `[kp]` prefix message
- `ANTHROPIC_API_KEY` from repo secrets
- Does NOT push to AnkiConnect (CI can't reach your desktop) — only writes `generated/` tree
- Guardrail: skips processing if no source files changed

**Out of scope:**
- Anki sync from CI (structurally impossible)
- Slack / email notifications
- Self-hosted runner setup (use standard GHA runners)

**Steps:**
1. Write `kp.yml`
2. Test on a throwaway branch in a test knowledge repo
3. Wire secrets

**Test:**

*Realism check (required):*
- Push a change to `notes/test.md` in a real (or test) knowledge repo
- GHA run triggers, completes green
- A new commit `[kp] update generated/` appears with updated `cards.jsonl` and `generated/obsidian/test.md`
- Guardrail works: pushing a change to `README.md` does not trigger processing
- API cost is reasonable (check `kp usage` locally against the repo first to calibrate)

**Done when:**
- [ ] End-to-end GHA run succeeds
- [ ] Committed generated/ diff is sensible
- [ ] Guardrail skips no-op pushes
