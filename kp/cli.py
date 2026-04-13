from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .config import Config, load_config
from .state import StateDB, default_db_path


def _print_config(cfg: Config) -> None:
    source = cfg.source_path if cfg.source_path else "<defaults (no config file found)>"
    print(f"source:              {source}")
    print(f"vault_path:          {cfg.vault_path}")
    print(f"knowledge_repo_path: {cfg.knowledge_repo_path}")
    print(f"anki_deck:           {cfg.anki_deck}")
    print(f"claude_api_key_env:  {cfg.claude_api_key_env}")
    print(f"enabled_sources:     {cfg.enabled_sources}")


_CONFIG_HELP = "path to kp.toml (overrides $KP_CONFIG / ./kp.toml / ~/.config/kp/config.toml)"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kp")
    parser.add_argument("--version", action="version", version=f"kp {__version__}")

    sub = parser.add_subparsers(dest="command")
    config_parser = sub.add_parser("config", help="config commands")
    config_sub = config_parser.add_subparsers(dest="config_command")
    show_parser = config_sub.add_parser("show", help="print the loaded config")
    show_parser.add_argument("--config", type=Path, default=None, help=_CONFIG_HELP)

    orphans_parser = sub.add_parser(
        "orphans", help="list state entries whose source file no longer exists"
    )
    orphans_parser.add_argument(
        "--db",
        type=Path,
        default=None,
        help="path to state.db (defaults to $XDG_DATA_HOME/kp/state.db)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "config" and args.config_command == "show":
        cfg = load_config(args.config)
        _print_config(cfg)
        return 0

    if args.command == "orphans":
        db_path = args.db if args.db is not None else default_db_path()
        with StateDB(db_path) as db:
            rows = db.orphans()
        if not rows:
            print("no orphans")
            return 0
        for row in rows:
            ids = ",".join(row.card_ids) if row.card_ids else "-"
            print(f"{row.path}\t{ids}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
