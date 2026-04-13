# 12 - chat source

**Goal:** Handle AI conversation transcripts in generic JSON or markdown format.
**Depends on:** 07

**In scope:**
- `kp/sources/chat.py` for transcripts in `{role, content}` JSON arrays or markdown with `## user` / `## assistant` headings
- Heuristic for identifying learning-shaped conversations (Q&A pattern, explanations, not just tool calls)
- AI prompt variant `prompts/chat-v1.md`: "the user was learning — extract cards on what they figured out"

**Out of scope:**
- Claude Code session-specific format — that's slice 15 (separate because the format is fragile)
- Real-time capture from a live chat (that's the MCP write slice 19)

**Steps:**
1. Parser for both formats
2. Heuristic scoring for learning-shaped detection
3. AI prompt variant
4. Tests with fixture transcripts

**Test:**

*Unit:*
- Fixture JSON transcript parses correctly
- Fixture markdown transcript parses correctly
- Non-learning conversation (pure code-edit requests) scores low and produces zero cards

*Realism check (required):*
- Fixture knowledge repo includes a real-shaped transcript from a past learning conversation
- `kp process <fixture>` → proposed cards focused on concepts the user learned, not surface-level "what was said"

**Done when:**
- [ ] Both formats parse correctly
- [ ] Cards are meaningfully different from what a raw "summarize this" would produce
- [ ] Heuristic correctly filters out non-learning chats
