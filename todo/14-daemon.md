# 14 - daemon

**Goal:** `kp watch` runs locally, detects file changes, pipelines them through process + sync automatically.
**Depends on:** 10

**In scope:**
- `kp watch <repo-path>` command using `watchdog` (or `inotify` via `pyinotify`)
- Debounced: wait N seconds after last change before processing (avoid thrashing during a save-storm)
- Runs `kp process` → `kp sync-obsidian` → `kp sync-anki` on each debounced event
- Respects `.gitignore` patterns in the watched repo
- Structured logging to a daemon log (`$XDG_STATE_HOME/kp/watch.log`)
- Graceful shutdown on SIGTERM

**Out of scope:**
- Running as a systemd unit (can be added outside this slice)
- Reacting to external triggers (webhooks, etc.)
- Cost guardrails (relies on slice 08's usage log — maybe refuse to run if daily cost exceeds a configured ceiling)

**Steps:**
1. Add `watchdog` dep
2. Watcher loop with debounce
3. Pipeline invocation on each event
4. Graceful shutdown + log rotation

**Test:**
- Start `kp watch`, edit a note in another terminal, see the Anki deck and Obsidian vault update within ~5 seconds
- Rapid-fire saves (touch file 10x in a row) trigger only one processing run
- Ctrl+C shuts down cleanly without a half-written `_review.jsonl`

**Done when:**
- [ ] Edit → card update loop feels fast enough to rely on
- [ ] No duplicate processing under rapid saves
- [ ] Log is readable and useful for debugging
