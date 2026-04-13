# 08 - claude synthesize

**Goal:** One Claude API call that takes a markdown file and returns proposed `basic` card JSON. Plus usage tracking and `--dry-run`.
**Depends on:** 03

**In scope:**
- `kp/synthesize.py` with `propose_cards(text: str, source_path: str) -> list[Card]`
- Uses Anthropic SDK, API key from `config.claude_api_key_env` env var
- Prompt lives in `prompts/v1.md` (versioned file, read at runtime)
- **Basic Q/A cards only** — cloze generation is slice 23
- Prompt caching enabled
- Usage log: every call appends a row to `$XDG_DATA_HOME/kp/usage.log`:
  `{timestamp, slice, model, input_tokens, output_tokens, cache_read_tokens, estimated_cost}`
- `kp usage` CLI command summarizes totals (today, week, all-time)
- `--dry-run` flag on `kp process` prints the full prompt + estimated input tokens, never calls the API, never appends to `usage.log`

**Out of scope:**
- Cloze generation (slice 23)
- Image / vision input (slice 12)
- Prompt evals (slice 17)
- Review queue / wiring into `kp process` (slices 09, 10)

**Steps:**
1. Add `anthropic` to `pyproject.toml` dependencies
2. `prompts/v1.md` with the Q/A card generation prompt
3. `synthesize.propose_cards()` with SDK call + JSON parsing
4. Usage log module (`kp/usage.py`) + `kp usage` command
5. `--dry-run` plumbing
6. Tests with mocked SDK

**Test:**
- Unit: mock SDK, verify `propose_cards` parses JSON response into `Card` records with `card_type="basic"`
- Unit: mock SDK, verify each call appends exactly one row to a temp `usage.log`
- Unit: `--dry-run` does NOT call the SDK and does NOT append to `usage.log`
- Integration (manual, marked): run on a real fixture file, eyeball the output — sensible cards?

**Done when:**
- [ ] Unit tests pass
- [ ] Manual run on a real note produces reasonable basic cards
- [ ] `kp usage` shows accumulated tokens and rough cost estimate
- [ ] Prompt is in `prompts/v1.md`, not hardcoded in `synthesize.py`
