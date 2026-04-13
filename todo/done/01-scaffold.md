# 01 - scaffold

**Goal:** Empty Python package that installs, runs, tests, and loads a `kp.toml` config.
**Depends on:** nothing

**In scope:**
- `pyproject.toml` (hatchling, python >=3.11, pytest dev dep, `kp` entrypoint)
- `kp/__init__.py` with `__version__`
- `kp/cli.py` with argparse, `kp --version`, `kp config show [--config PATH]`
- `kp/config.py` with `Config` dataclass + `load_config()` searching `override → $KP_CONFIG → ./kp.toml → $XDG_CONFIG_HOME/kp/config.toml`
- `flake.nix` devShell (python3 + uv, auto `.venv` activation)
- `tests/test_smoke.py`, `tests/test_config.py`, `tests/fixtures/kp.toml`
- `.gitignore`

**Out of scope:**
- Any real source/sink logic
- README, any docs

**Steps:**
1. Write `pyproject.toml`, `kp/__init__.py`, `kp/config.py`, `kp/cli.py`
2. Write `flake.nix` + `.gitignore`
3. Write tests + fixture
4. `nix develop` → `uv pip install -e '.[dev]'`
5. Run the acceptance checks below

**Test:**
- `kp --version` prints `kp 0.0.1`
- `kp config show` prints defaults (no config file found)
- `kp config show --config tests/fixtures/kp.toml` prints the fixture's values
- `pytest -q` → 5 passed

**Done when:**
- [x] All four acceptance checks pass
- [x] Nix dev shell auto-creates and activates `.venv`
