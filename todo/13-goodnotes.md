# 13 - goodnotes

**Goal:** Auto-export GoodNotes notebooks into the knowledge repo so they flow through the image/PDF pipeline.
**Depends on:** 12

**In scope:**
- Investigate: does GoodNotes 6 still export OCR'd PDFs, or only flat? What's the best auto-export path (iCloud sync of notebooks, a Shortcut on save, scheduled "Export All")?
- Document findings in the slice file itself (update this file during the work)
- A shim (script or daemon component) that watches the chosen cloud folder and drops new/updated GoodNotes files into `knowledge/goodnotes/<notebook-name>/`
- If PDF path: `kp/sources/goodnotes.py` using `pypdf`/`pdfplumber` to extract OCR'd text layer
- If per-page image path: reuse `sources/image.py` from slice 12 directly (no new source needed)

**Out of scope:**
- Rolling our own OCR if GoodNotes doesn't provide one — fall back to image path via Claude vision instead
- Building a GoodNotes plugin

**Steps:**
1. Test GoodNotes export options on your real device
2. Pick the lowest-friction path, document the decision here
3. Implement the shim
4. Wire into `kp process`

**Test:**
- A real GoodNotes page, written/scanned on your device, ends up as an Anki card and Obsidian note within X minutes of editing
- Per-notebook folder granularity works (git diffs stay small)

**Done when:**
- [ ] Investigation notes recorded here
- [ ] A real GoodNotes page round-trips to Anki end-to-end
- [ ] You haven't had to manually "Export" anything during the test
