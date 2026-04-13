from __future__ import annotations

import hashlib
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def _get(card: Any, key: str, default: Any = None) -> Any:
    if isinstance(card, dict):
        return card.get(key, default)
    return getattr(card, key, default)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _note_rel_path(source_path: Path, repo_root: Path | None = None) -> Path:
    if repo_root is not None:
        base = source_path.resolve().relative_to(Path(repo_root).resolve())
    elif source_path.is_absolute():
        base = Path(source_path.name)
    else:
        base = source_path
    return base.with_suffix(".md")


def _build_frontmatter(
    source: str, source_hash: str, card_ids: list[str], generated_at: str
) -> str:
    cards_yaml = "[" + ", ".join(card_ids) + "]"
    return (
        "---\n"
        f"source: {source}\n"
        f"source_hash: {source_hash}\n"
        f"cards: {cards_yaml}\n"
        f"generated_at: {generated_at}\n"
        "---\n"
    )


_GENERATED_AT_RE = re.compile(r"^generated_at: .*$", re.MULTILINE)
_PLACEHOLDER = "generated_at: <ignored>"


def _normalize(content: str) -> str:
    return _GENERATED_AT_RE.sub(_PLACEHOLDER, content, count=1)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_note(
    vault_path: Path | str,
    source_path: Path | str,
    body: str,
    cards: Iterable[Any],
    *,
    media_src_dir: Path | str | None = None,
    repo_root: Path | str | None = None,
) -> Path:
    vault_path = Path(vault_path)
    source_path = Path(source_path)
    root = Path(repo_root) if repo_root is not None else None

    note_path = vault_path / "generated" / _note_rel_path(source_path, root)
    note_path.parent.mkdir(parents=True, exist_ok=True)

    cards_list = list(cards)
    card_ids = [str(_get(c, "id")) for c in cards_list]
    source_hash = _sha256_file(source_path) if source_path.exists() else ""
    body_norm = body if body.endswith("\n") else body + "\n"

    def compose(generated_at: str) -> str:
        return (
            _build_frontmatter(str(source_path), source_hash, card_ids, generated_at)
            + "\n"
            + body_norm
        )

    candidate = compose("<placeholder>")
    if note_path.exists():
        existing = note_path.read_text()
        if _normalize(existing) == _normalize(candidate):
            pass  # idempotent no-op
        else:
            note_path.write_text(compose(_now_iso()))
    else:
        note_path.write_text(compose(_now_iso()))

    media_files: list[str] = []
    seen: set[str] = set()
    for c in cards_list:
        for m in _get(c, "media", []) or []:
            if m not in seen:
                seen.add(m)
                media_files.append(m)

    if media_files:
        src_dir = Path(media_src_dir) if media_src_dir is not None else Path("generated") / "media"
        media_dest = vault_path / "generated" / "media"
        media_dest.mkdir(parents=True, exist_ok=True)
        for name in media_files:
            src = src_dir / name
            if src.exists():
                shutil.copy2(src, media_dest / name)

    return note_path
