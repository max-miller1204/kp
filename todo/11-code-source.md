# 11 - code source

**Goal:** Process source code files with explicit `// anki:` comments + AI-generated cards on the code's concepts.
**Depends on:** 07

**In scope:**
- `kp/sources/code.py` with `extract_explicit` (scan for `// anki: front :: back` one-liners and `/* anki ... */` blocks) + AI path
- Language-aware comment styles: at minimum `//`, `#`, `/* */`
- AI prompt variant `prompts/code-v1.md` focused on "what does this code teach" rather than "what does this document say"
- Respects language / file-extension filtering via config (e.g., `enabled_code_extensions = [".py", ".ts", ".rs"]`)

**Out of scope:**
- Static analysis beyond comment extraction
- Actually running or importing the code
- AST-level concept extraction

**Steps:**
1. Comment parser for the supported styles
2. Wire into `kp process` file walker (handle the new extensions)
3. AI prompt variant `prompts/code-v1.md`
4. Tests with realistic fixture code files

**Test:**

*Unit:*
- Fixture with `// anki: foo :: bar` → produces that card exactly
- Fixture with `/* anki\nfront\n::\nback\n*/` → produces that card exactly
- Unsupported extension is skipped cleanly

*Realism check (required):*
- Fixture code repo with at least 3 languages (Python `#`, TS `//`, Rust `//`), subdirectory structure, absolute paths
- Mix of files with explicit `anki:` comments and files without
- Run `kp process <fixture>` → explicit comments become direct cards, files without comments produce AI proposals in `_review.jsonl`

**Done when:**
- [ ] Both explicit and AI modes work on fixture code files
- [ ] At least 3 comment styles parse correctly
- [ ] Real run on your own code produces sensible cards
