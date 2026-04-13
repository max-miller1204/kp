# 15 - claude sessions source

**Goal:** Read `~/.claude/projects/**/*.jsonl` and turn learning-shaped conversations into cards. Zero capture friction — the data is already on disk.
**Depends on:** 07

**⚠️ Implementation risk:**
The Claude Code session format is NOT a stable public API. Field names and structure may change between CLI versions. Isolate the parser in one small function, snapshot the current format in a test fixture, and expect maintenance when Claude Code updates. If it breaks after a CLI update, this is the first place to look.

**In scope:**
- `kp/sources/claude_sessions.py`
- Session discovery: walk `~/.claude/projects/`
- Per-session parser → normalized `{timestamp, role, content}` list
- "Learning-shaped" heuristic: score by ratio of user questions + assistant explanations vs. tool calls / edit requests. Threshold configurable.
- Feed filtered transcripts into `synthesize.py` with `prompts/claude-session-v1.md`: "what did the user just figure out?"
- State tracks processed sessions by file hash so re-runs don't reprocess

**Out of scope:**
- Live / real-time capture mid-session
- Parsing any session field beyond user/assistant content (ignore tool calls for card-generation purposes)

**Steps:**
1. Pin a real recent session as a test fixture (you have one right now — this conversation)
2. Isolated parser with the fixture as its regression test
3. Heuristic for learning-shaped detection
4. Prompt + synthesize wiring
5. Tests + one real-session manual run

**Test:**

*Unit:*
- Fixture-based parser test pins the current session format — if the test breaks after a CLI update, you know exactly where the adapter needs updating
- Heuristic correctly flags a learning session vs. a pure edit session on fixtures

*Realism check (required):*
- Point it at a real session from the past week (not a fixture) → sensible card proposals in `_review.jsonl`
- Verify the heuristic doesn't pull from hundreds of mundane sessions — tune threshold until signal ≥ noise

**Done when:**
- [ ] Parser is one small, isolated function
- [ ] Fixture test exists (you'll need it the day Claude Code updates the format)
- [ ] Real-session manual test produces useful cards
