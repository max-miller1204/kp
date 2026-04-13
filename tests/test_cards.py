from __future__ import annotations

import json
from pathlib import Path

import pytest

from kp.cards import SCHEMA_VERSION, Card, read_cards, write_cards


def _sample_cards() -> list[Card]:
    return [
        Card(
            id="a1",
            front="What is 2+2?",
            back="4",
            tags=["math", "easy"],
            source_path="notes/math.md",
            source_line=10,
            source_hash="deadbeef",
            media=[],
            card_type="basic",
            backlinks={"obsidian": "[[math]]", "source": "notes/math.md#L10"},
        ),
        Card(
            id="c1",
            front="The capital of {{c1::France}} is {{c2::Paris}}.",
            back="",
            tags=["geo"],
            source_path="notes/geo.md",
            source_line=None,
            source_hash="cafef00d",
            media=["img/france.png"],
            card_type="cloze",
            backlinks={"obsidian": None, "source": None},
        ),
        Card(
            id="o1",
            front="Label the diagram",
            back="see image",
            tags=[],
            source_path="notes/anatomy.md",
            source_line=42,
            source_hash="1234abcd",
            media=["img/anatomy.png", "img/anatomy.mask.png"],
            card_type="occlusion",
            backlinks={"obsidian": "[[anatomy]]", "source": None},
        ),
    ]


def test_round_trip(tmp_path: Path) -> None:
    cards = _sample_cards()
    path = tmp_path / "cards.jsonl"
    write_cards(path, cards)

    loaded = list(read_cards(path))
    assert loaded == cards


def test_every_field_present() -> None:
    card = _sample_cards()[0]
    expected = {
        "id",
        "front",
        "back",
        "tags",
        "source_path",
        "source_line",
        "source_hash",
        "media",
        "card_type",
        "backlinks",
        "schema_version",
    }
    assert set(card.__dataclass_fields__.keys()) == expected
    assert card.schema_version == SCHEMA_VERSION


def test_schema_version_mismatch(tmp_path: Path) -> None:
    path = tmp_path / "bad.jsonl"
    bad = {
        "id": "x",
        "front": "f",
        "back": "b",
        "tags": [],
        "source_path": "x.md",
        "source_line": None,
        "source_hash": "h",
        "media": [],
        "card_type": "basic",
        "backlinks": {"obsidian": None, "source": None},
        "schema_version": 999,
    }
    path.write_text(json.dumps(bad) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="schema_version"):
        list(read_cards(path))
