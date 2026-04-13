# 20 - image labeled questions

**Goal:** For diagrams with labeled regions, generate text questions about specific labeled parts. NO masking pipeline — the full image stays on the card.
**Depends on:** 12

**In scope:**
- Extend `kp/sources/image.py` to detect labeled regions via Claude vision ("what labels/arrows/annotations are visible, and what do they point to?")
- For each label, generate a card with:
  - Front: full image + "What structure is indicated by the arrow in the upper-left?" (or similar positional phrasing)
  - Back: the label / explanation
- Card `card_type` stays `basic` or goes to `occlusion` — decide based on whether the fallback Image Occlusion Enhanced addon integration happens

**Out of scope:**
- Rolling our own bounding-box / masking CV pipeline — EXPLICITLY REJECTED. It's a disappointment factory.
- If true masked-region cards turn out to be necessary after using this, integrate with [Image Occlusion Enhanced](https://github.com/glutanimate/image-occlusion-enhanced) addon's JSON format rather than reinventing it.

**Steps:**
1. Vision prompt that enumerates labeled parts with positional descriptions
2. Generate one card per label with the full image attached
3. Test with a real labeled diagram fixture

**Test:**
- Process a labeled anatomy or architecture diagram fixture
- Verify N text-question cards (N = number of labels) with the full image on the front
- Cards make sense to study (eyeball test)

**Done when:**
- [ ] Real diagram produces cards you'd actually want to study
- [ ] Zero custom CV / masking code in the slice
