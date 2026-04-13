from __future__ import annotations

import hashlib
import re
from pathlib import Path

from kp.cards import Card

_TAG_RE = re.compile(r"(?:^|\s)#flashcard(?![\w/-])")


def _file_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _card_id(source_hash: str, source_line: int) -> str:
    return hashlib.sha256(f"{source_hash}:{source_line}".encode("utf-8")).hexdigest()[:16]


def _strip_tag(line: str) -> str:
    return _TAG_RE.sub(" ", line).strip()


def _make_card(path: Path, line_no: int, source_hash: str, front: str, back: str) -> Card:
    return Card(
        id=_card_id(source_hash, line_no),
        front=front,
        back=back,
        source_path=str(path),
        source_hash=source_hash,
        source_line=line_no,
        card_type="basic",
    )


def extract_explicit(path: Path) -> list[Card]:
    text = Path(path).read_text(encoding="utf-8")
    source_hash = _file_hash(text)
    lines = text.splitlines()
    cards: list[Card] = []
    consumed: set[int] = set()

    for i, line in enumerate(lines):
        if i in consumed or not _TAG_RE.search(line):
            continue

        tagless = _strip_tag(line)
        if "?" in tagless:
            q, _, a = tagless.partition("?")
            front = (q.strip() + "?").strip()
            back = a.strip()
            if front != "?" and back:
                cards.append(_make_card(path, i + 1, source_hash, front, back))
                consumed.add(i)
                continue

        start = i
        while start > 0 and lines[start - 1].strip():
            start -= 1
        end = i
        while end + 1 < len(lines) and lines[end + 1].strip():
            end += 1

        sep_idx = None
        for j in range(start, end + 1):
            if lines[j].strip() == "?":
                sep_idx = j
                break
        if sep_idx is None:
            continue

        front_lines = [
            _strip_tag(lines[k]) for k in range(start, sep_idx)
            if _strip_tag(lines[k])
        ]
        back_lines = [
            _strip_tag(lines[k]) for k in range(sep_idx + 1, end + 1)
            if _strip_tag(lines[k])
        ]
        front = "\n".join(front_lines).strip()
        back = "\n".join(back_lines).strip()
        if not front or not back:
            continue

        cards.append(_make_card(path, i + 1, source_hash, front, back))
        for k in range(start, end + 1):
            consumed.add(k)

    return cards
