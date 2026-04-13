# 16 - chat source

**Goal:** Handle AI conversation transcripts in generic JSON or markdown format.
**Depends on:** 10

**In scope:**
- `kp/sources/chat.py` for transcripts in `{role, content}` JSON arrays or markdown with `## user` / `## assistant` headings
- Heuristic for identifying learning-shaped conversations (Q&A pattern, explanations, not just tool calls)
- AI prompt variant `prompts/chat-v1.md`: "the user was learning — extract cards on what they figured out"

**Out of scope:**
- Claude Code session-specific format — that's slice 19
- Real-time capture from a live chat

**Steps:**
1. Parser for both formats
2. AI prompt variant
3. Tests with fixture transcripts

**Test:**
- Fixture chat transcript → produces cards focused on concepts the user learned
- Non-learning conversation (pure code-edit requests) → skipped or produces zero cards

**Done when:**
- [ ] Both formats parse correctly
- [ ] Cards are meaningfully different from what a raw "summarize this" would produce
