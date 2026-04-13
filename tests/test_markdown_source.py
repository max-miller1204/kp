from pathlib import Path

from kp.sources.markdown import extract_explicit

FIXTURES = Path(__file__).parent / "fixtures"


def test_extracts_two_explicit_cards():
    cards = extract_explicit(FIXTURES / "md_two_cards.md")
    assert len(cards) == 2

    single, multi = cards
    assert single.front == "What is the capital of France?"
    assert single.back == "Paris"
    assert single.card_type == "basic"
    assert single.media == []
    assert single.backlinks == {"obsidian": None, "source": None}

    assert multi.front == "What is the speed of light in vacuum"
    assert multi.back == "Approximately 299,792,458 m/s"


def test_no_flashcard_tags_returns_empty():
    assert extract_explicit(FIXTURES / "md_no_cards.md") == []


def test_extraction_is_idempotent():
    path = FIXTURES / "md_two_cards.md"
    first = extract_explicit(path)
    second = extract_explicit(path)
    assert [c.id for c in first] == [c.id for c in second]
    assert first == second


def test_source_line_points_at_flashcard_line():
    cards = extract_explicit(FIXTURES / "md_two_cards.md")
    text = (FIXTURES / "md_two_cards.md").read_text().splitlines()
    for card in cards:
        assert card.source_line is not None
        assert "#flashcard" in text[card.source_line - 1]
