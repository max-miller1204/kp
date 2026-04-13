# 10 - daemon

**Goal:** `kp watch` runs locally, detects file changes in a knowledge repo, pipelines them through process + sync automatically.
**Depends on:** 07

**In scope:**
- `kp watch <repo-path>` command using `watchdog` (or `inotify` via `pyinotify`)
- Debounced: wait N seconds after the last change before processing (avoid thrashing during save-storms)
- Runs `kp process` → `kp sync-obsidian` → `kp sync-anki` on each debounced event
- Respects `.gitignore` patterns in the watched repo
- Structured logging to `$XDG_STATE_HOME/kp/watch.log`
- Graceful shutdown on SIGTERM
- Optional: daily cost ceiling (refuse to run if `kp usage` shows today exceeds a config value)

**Out of scope:**
- Running as a systemd unit (separate concern, can be layered on outside the slice)
- Reacting to external triggers (webhooks, remote changes, etc.)

**Steps:**
1. Add `watchdog` dep
2. Watcher loop with debounce
3. Pipeline invocation on each event
4. Graceful shutdown + log writer
5. Cost guardrail

**Test:**

*Realism check (required):*
- Start `kp watch <fixture-repo>` in a subprocess
- Edit a note in the fixture repo from another process
- Within ~5 seconds: `cards.jsonl` updates, obsidian vault updates
- Rapid-fire saves (touch the file 10 times in a row) trigger only ONE processing run
- Send SIGTERM → process exits cleanly, no half-written `_review.jsonl`

**Done when:**
- [ ] Edit → card update loop feels fast enough to rely on
- [ ] No duplicate processing under rapid saves
- [ ] Log is readable and useful for debugging
