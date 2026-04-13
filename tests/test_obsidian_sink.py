from __future__ import annotations

import time
from types import SimpleNamespace

from kp.sinks.obsidian import write_note


def _source(tmp_path, name="note.md", content="source body\n"):
    p = tmp_path / name
    p.write_text(content)
    return p


def test_write_note_creates_file_with_frontmatter(tmp_path):
    vault = tmp_path / "vault"
    source = _source(tmp_path)
    cards = [SimpleNamespace(id="card-abc", media=[])]

    note_path = write_note(vault, source, "# Body\n\nhello\n", cards)

    assert note_path.exists()
    text = note_path.read_text()
    assert text.startswith("---\n")
    assert f"source: {source}" in text
    assert "cards: [card-abc]" in text
    assert "source_hash:" in text
    assert "generated_at:" in text
    assert "# Body" in text


def test_write_note_is_idempotent_on_same_body(tmp_path):
    vault = tmp_path / "vault"
    source = _source(tmp_path)
    cards = [SimpleNamespace(id="c1", media=[])]

    note_path = write_note(vault, source, "same body\n", cards)
    first_mtime = note_path.stat().st_mtime_ns
    first_text = note_path.read_text()

    time.sleep(0.01)
    write_note(vault, source, "same body\n", cards)

    assert note_path.stat().st_mtime_ns == first_mtime
    assert note_path.read_text() == first_text


def test_write_note_overwrites_on_different_body(tmp_path):
    vault = tmp_path / "vault"
    source = _source(tmp_path)
    cards = [SimpleNamespace(id="c1", media=[])]

    note_path = write_note(vault, source, "first body\n", cards)
    first_text = note_path.read_text()

    write_note(vault, source, "second body\n", cards)
    second_text = note_path.read_text()

    assert "first body" not in second_text
    assert "second body" in second_text
    assert second_text != first_text


def test_write_note_preserves_subdirectories_with_repo_root(tmp_path):
    repo = tmp_path / "knowledge"
    (repo / "topology").mkdir(parents=True)
    (repo / "algebra").mkdir(parents=True)
    topo = repo / "topology" / "basics.md"
    topo.write_text("topo source\n")
    alg = repo / "algebra" / "basics.md"
    alg.write_text("alg source\n")

    vault = tmp_path / "vault"
    cards = [SimpleNamespace(id="c1", media=[])]

    topo_note = write_note(vault, topo, "topo body\n", cards, repo_root=repo)
    alg_note = write_note(vault, alg, "alg body\n", cards, repo_root=repo)

    assert topo_note != alg_note
    assert topo_note == vault / "generated" / "topology" / "basics.md"
    assert alg_note == vault / "generated" / "algebra" / "basics.md"
    assert "topo body" in topo_note.read_text()
    assert "alg body" in alg_note.read_text()


def test_write_note_copies_media(tmp_path):
    vault = tmp_path / "vault"
    source = _source(tmp_path)
    media_src = tmp_path / "media_src"
    media_src.mkdir()
    (media_src / "foo.png").write_bytes(b"\x89PNG fake")

    cards = [SimpleNamespace(id="c1", media=["foo.png"])]

    write_note(vault, source, "body\n", cards, media_src_dir=media_src)

    copied = vault / "generated" / "media" / "foo.png"
    assert copied.exists()
    assert copied.read_bytes() == b"\x89PNG fake"
