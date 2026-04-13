# 04 - markdown source (explicit)

**Goal:** Extract explicit `#flashcard` blocks from markdown files into `Card` records. No AI.
**Depends on:** 03

**In scope:**
- `kp/sources/markdown.py` with `extract_explicit(path: Path) -> list[Card]`
- Recognize Obsidian-flashcards convention: `#flashcard` tag on a line, then Q/A separated by `?` (single-line) or line-separated
- Populate `source_path`, `source_line`, `source_hash`, `card_type="basic"`, empty `media` / empty `backlinks`
- Deterministic card ID from `(source_hash, source_line)` so re-extraction is idempotent

**Out of scope:**
- AI synthesis (slice 08)
- Cloze-style markdown (slice 23)
- Frontmatter parsing
- Writing anywhere — only extraction

**Steps:**
1. Parser for `#flashcard` blocks
2. Card construction with stable IDs
3. Tests with fixture markdown files

**Test:**
- Fixture `.md` with exactly 2 explicit cards → `extract_explicit` returns exactly 2 cards with correct front/back
- Fixture with no `#flashcard` tags → returns `[]`
- Running twice produces identical card IDs (idempotent)

**Done when:**
- [x] 3 tests pass
- [x] Cards include `source_line` pointing at the right line
