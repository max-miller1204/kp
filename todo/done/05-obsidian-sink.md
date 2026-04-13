# 05 - obsidian sink

**Goal:** Idempotently write generated markdown notes into the Obsidian vault with backlinks to the source.
**Depends on:** 03

**In scope:**
- `kp/sinks/obsidian.py` with `write_note(vault_path, source_path, body, cards)`
- Generated note lives at `<vault>/generated/<relative-source-path>.md`
- Frontmatter: `source: <original path>`, `cards: [id1, id2]`, `generated_at`, `source_hash`
- Idempotent: running twice with same content produces same file (byte-for-byte); different content overwrites cleanly
- Understands `media: []` field; copies referenced files from a `generated/media/` dir to `<vault>/generated/media/` (no-op if empty)

**Out of scope:**
- Actually generating note bodies (that's the pipeline wiring step)
- Obsidian-style backlinks graph / tag routing
- Deleting orphaned generated notes

**Steps:**
1. `write_note` with frontmatter builder
2. Media copy helper
3. Tests with a tmp_path "vault"

**Test:**
- Call `write_note` with a fake source + 1 card → file exists, frontmatter has `source:` and `cards:` correctly
- Call twice with same body → second call is a no-op (mtime or content hash unchanged)
- Call with different body → file contents update
- `media: [foo.png]` → `foo.png` ends up in `<vault>/generated/media/foo.png`

**Done when:**
- [x] 4 tests pass
- [x] Generated notes resolve their `source:` path when opened in Obsidian
