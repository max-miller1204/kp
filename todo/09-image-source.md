# 09 - image source

**Goal:** Process PNG/JPG files (handwritten note photos, screenshots) through Claude vision, emit cards with the image on the front.
**Depends on:** 07

**In scope:**
- `kp/sources/image.py` with `process_image(path) -> list[Card]`
- Copy original to `generated/media/<hash>.<ext>` (content-addressed)
- Claude vision call: "transcribe handwriting, describe diagrams, list key concepts"
- Feed image + transcription into `synthesize.py` with a vision-aware prompt variant (`prompts/image-v1.md`)
- Cards get `media: [<hash>.<ext>]` populated (Anki sink already supports the field from slice 06)
- Generated Obsidian note embeds the image with `![[<hash>.<ext>]]`

**Out of scope:**
- Image occlusion / labeled-region questions (slice 18)
- GoodNotes-specific handling (slice 17)
- Auto-capture from phone/screenshot folder (slice 10's concern)

**Steps:**
1. Image copy + content-addressed naming helper
2. Vision prompt + Claude call
3. Extend `kp process` to recognize `.png`/`.jpg`/`.jpeg` files alongside `.md`
4. Verify the obsidian sink's existing media copy logic handles the new field correctly

**Test:**

*Unit:*
- Mock the SDK: `process_image` parses a vision response into card records with populated `media` field
- Hash collision safety: same image bytes always produce the same `generated/media/<hash>.png` path

*Realism check (required):*
- Drop a real photo of a handwritten note in `tests/fixtures/knowledge-repo/images/test.jpg` (or add to the existing fixture repo from slice 06)
- `kp process <fixture>` → `_review.jsonl` has proposed cards referencing the image; `<fixture>/generated/media/<hash>.jpg` exists
- `kp sync-obsidian <vault>` → vault has a note embedding the image
- Approve cards, `kp sync-anki` → Anki card front shows the image + a text question

**Done when:**
- [ ] End-to-end test with a real handwritten note works
- [ ] Media file is stored once (content-addressed), not duplicated per card
- [ ] Usage log reflects the vision call costs
