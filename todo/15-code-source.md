# 15 - code source

**Goal:** Process source code files with explicit `// anki:` comments + AI-generated cards on the code's concepts.
**Depends on:** 10

**In scope:**
- `kp/sources/code.py` with `extract_explicit` (scan for `// anki: front :: back` and `/* anki ... */` blocks) + AI path
- Language-aware comment parsing: support `//`, `#`, `/* */` styles
- AI prompt variant that focuses on "what does this code teach" rather than "what does this document say"
- Respects language / file-extension filtering via config

**Out of scope:**
- Static analysis beyond comment extraction
- Running or importing the code

**Steps:**
1. Comment parser for the supported styles
2. AI prompt variant `prompts/code-v1.md`
3. Integration test with a fixture repo

**Test:**
- Fixture file with `// anki: foo :: bar` → produces that card exactly
- Fixture file without explicit comments → AI produces sensible cards on the code's ideas
- Unsupported extension is skipped

**Done when:**
- [ ] Both explicit and AI modes work on fixture code files
- [ ] At least 3 language styles parse correctly
