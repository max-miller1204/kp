from pathlib import Path

from kp.config import Config, load_config


FIXTURE = Path(__file__).parent / "fixtures" / "kp.toml"


def test_defaults_when_no_file(tmp_path, monkeypatch):
    monkeypatch.delenv("KP_CONFIG", raising=False)
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    monkeypatch.chdir(tmp_path)

    cfg = load_config()

    assert cfg == Config()
    assert cfg.anki_deck == "KP::Inbox"
    assert cfg.enabled_sources == ["markdown"]
    assert cfg.source_path is None


def test_loads_from_override():
    cfg = load_config(FIXTURE)

    assert cfg.source_path == FIXTURE
    assert cfg.vault_path == Path("~/ObsidianVault").expanduser()
    assert cfg.knowledge_repo_path == Path("~/knowledge").expanduser()
    assert cfg.anki_deck == "KP::Fixture"
    assert cfg.claude_api_key_env == "FIXTURE_API_KEY"
    assert cfg.enabled_sources == ["markdown", "image"]


def test_env_var_is_used(tmp_path, monkeypatch):
    monkeypatch.setenv("KP_CONFIG", str(FIXTURE))
    monkeypatch.chdir(tmp_path)

    cfg = load_config()

    assert cfg.source_path == FIXTURE
    assert cfg.anki_deck == "KP::Fixture"


def test_cwd_kp_toml_is_found(tmp_path, monkeypatch):
    monkeypatch.delenv("KP_CONFIG", raising=False)
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    local = tmp_path / "kp.toml"
    local.write_text('anki_deck = "KP::Local"\n')
    monkeypatch.chdir(tmp_path)

    cfg = load_config()

    assert cfg.source_path == local
    assert cfg.anki_deck == "KP::Local"
