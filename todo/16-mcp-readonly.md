# 16 - mcp (read-only)

**Goal:** Expose the knowledge repo as an MCP server so any Claude session can query your notes and cards. Read-only first.
**Depends on:** 07 (ideally also 14 for `weak_areas()`)

**In scope:**
- `kp mcp-serve` command launching an MCP server process
- Uses the official MCP Python SDK
- Tools exposed (ALL READ-ONLY):
  - `search_notes(query: str)` — keyword/substring search over vault markdown
  - `get_note(path: str)` — fetch a specific note's content
  - `find_related_cards(concept: str)` — search `cards.jsonl` by front/back/tag match
  - `recent_learning(days: int = 7)` — recently-added sources in the knowledge repo
  - `weak_areas()` — pulls from slice 14 if available; otherwise returns empty with a note
- Registered in `~/.claude/settings.json` under `mcpServers` so Claude Code and Claude Desktop both see it automatically
- No authentication needed (local-only, stdio transport)

**Out of scope:**
- ANY write tools (that's slice 19)
- Semantic / vector search (keyword is fine for v1; can upgrade later)

**Steps:**
1. Add `mcp` SDK dep
2. Implement server + tools
3. Register in `~/.claude/settings.json`
4. Manual test from a fresh Claude session

**Test:**

*Unit:*
- Each tool function returns well-shaped results on fixture input
- Missing vault / missing cards.jsonl → clean error messages, no crashes
- Grep the source: zero write operations anywhere in the tool implementations

*Realism check (required):*
- From a fresh Claude Code or Claude Desktop session:
  - "What have I learned about X this week?" → model calls `search_notes` + `recent_learning`, returns grounded answer citing your notes
  - "Do I have any cards on concept Y?" → model calls `find_related_cards`, lists them
- Both queries use the REAL knowledge repo and real cards.jsonl, not a fixture

**Done when:**
- [ ] Server installs and registers without manual JSON editing
- [ ] Real Claude session uses the tools correctly on first try
- [ ] Zero write tools in the code (grep-verified)
