# 12 - image source

**Goal:** Process PNG/JPG files (handwritten note photos, screenshots) through Claude vision, emit cards with the image on the front.
**Depends on:** 10

**In scope:**
- `kp/sources/image.py` with `process_image(path) -> list[Card]`
- Copy original to `generated/media/<hash>.<ext>` (content-addressed)
- Claude vision call: "transcribe handwriting, describe diagrams, list key concepts"
- Feed image + transcription into `synthesize.py` with a vision-aware prompt variant (`prompts/image-v1.md`)
- Cards get `media: [<hash>.<ext>]` populated (Anki sink already supports it)
- Generated Obsidian note embeds the image with `![[<hash>.<ext>]]`

**Out of scope:**
- Image occlusion / labeled-region questions (slice 20)
- GoodNotes-specific handling (slice 13)
- Auto-capture from phone/screenshot folder (that's a `kp watch` concern, slice 14)

**Steps:**
1. Image copy + content-addressed naming
2. Vision prompt + Claude call
3. Integrate into `kp process`
4. Obsidian sink already handles media (slice 05) — verify end-to-end

**Test:**
- Drop a photo of a handwritten note in `knowledge/images/test.jpg`
- `kp process knowledge/` → `_review.jsonl` has proposed cards referencing the image
- Approve cards, `kp sync-anki` → Anki card front shows the image + a text question
- Obsidian vault has a note embedding the image

**Done when:**
- [ ] End-to-end test with a real handwritten note works
- [ ] Media file is stored once (content-addressed), not duplicated per card
- [ ] Usage log reflects the vision call costs
