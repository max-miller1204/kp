from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Iterator, Literal


SCHEMA_VERSION = 1


@dataclass
class Card:
    id: str
    front: str
    back: str
    source_path: str
    source_hash: str
    source_line: int | None = None
    tags: list[str] = field(default_factory=list)
    media: list[str] = field(default_factory=list)
    card_type: Literal["basic", "cloze", "occlusion"] = "basic"
    backlinks: dict = field(default_factory=lambda: {"obsidian": None, "source": None})
    schema_version: int = SCHEMA_VERSION


def write_cards(path: Path | str, cards: Iterable[Card]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for card in cards:
            f.write(json.dumps(asdict(card), ensure_ascii=False))
            f.write("\n")


def read_cards(path: Path | str) -> Iterator[Card]:
    path = Path(path)
    with open(path, "r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            raw = raw.strip()
            if not raw:
                continue
            data = json.loads(raw)
            version = data.get("schema_version")
            if version != SCHEMA_VERSION:
                raise ValueError(
                    f"{path}:{lineno}: unknown schema_version {version!r} "
                    f"(expected {SCHEMA_VERSION})"
                )
            yield Card(**data)
