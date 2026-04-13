# 17 - goodnotes

**Goal:** Auto-export GoodNotes notebooks into the knowledge repo so they flow through the image pipeline.
**Depends on:** 09

**In scope:**
- Investigate (and record findings in this file during the work): does GoodNotes 6 still export OCR'd PDFs, or only flat? What's the best auto-export path (iCloud sync of notebooks, a Shortcut on save, scheduled "Export All")?
- A shim (script or daemon component) that watches the chosen cloud folder and drops new/updated GoodNotes exports into `knowledge/goodnotes/<notebook-name>/` or `knowledge/images/`
- If per-page image path: reuse `sources/image.py` from slice 09 directly (simplest — no new source code needed)
- If PDF path: a thin `sources/goodnotes.py` using `pypdf`/`pdfplumber` to extract the OCR layer, falling back to image-path if no OCR is present

**Out of scope:**
- Rolling our own OCR if GoodNotes doesn't provide one — fall back to image path via Claude vision instead
- Building a GoodNotes plugin

**Steps:**
1. Test GoodNotes export options on your real device
2. Pick the lowest-friction auto-export path, document the decision in this file
3. Implement the shim
4. Wire into `kp process`

**Test:**

*Realism check (required):*
- A real GoodNotes page, written/scanned on your device, ends up as an Anki card and Obsidian note within X minutes of editing
- Per-notebook folder granularity works (git diffs stay small)
- You have not had to manually "Export All" during the test

**Done when:**
- [ ] Investigation notes recorded in this file
- [ ] A real GoodNotes page round-trips to Anki end-to-end
- [ ] Export is fully automatic — no manual steps
