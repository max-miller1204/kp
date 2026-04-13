from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    vault_path: Path | None = None
    knowledge_repo_path: Path | None = None
    anki_deck: str = "KP::Inbox"
    claude_api_key_env: str = "ANTHROPIC_API_KEY"
    enabled_sources: list[str] = field(default_factory=lambda: ["markdown"])
    source_path: Path | None = None


def find_config_path(override: Path | None = None) -> Path | None:
    if override is not None:
        return override
    env = os.environ.get("KP_CONFIG")
    if env:
        return Path(env)
    cwd = Path.cwd() / "kp.toml"
    if cwd.exists():
        return cwd
    xdg = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    xdg_path = xdg / "kp" / "config.toml"
    if xdg_path.exists():
        return xdg_path
    return None


def load_config(override: Path | None = None) -> Config:
    path = find_config_path(override)
    if path is None:
        return Config()
    with open(path, "rb") as f:
        data = tomllib.load(f)

    cfg = Config(source_path=path)
    if "vault_path" in data:
        cfg.vault_path = Path(data["vault_path"]).expanduser()
    if "knowledge_repo_path" in data:
        cfg.knowledge_repo_path = Path(data["knowledge_repo_path"]).expanduser()
    if "anki_deck" in data:
        cfg.anki_deck = str(data["anki_deck"])
    if "claude_api_key_env" in data:
        cfg.claude_api_key_env = str(data["claude_api_key_env"])
    if "enabled_sources" in data:
        cfg.enabled_sources = [str(s) for s in data["enabled_sources"]]
    return cfg
