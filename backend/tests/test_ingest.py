"""Tests for the ingestion pipeline (chunk_markdown module).

These are unit tests — they do NOT require a Qdrant or OpenAI connection.
Run with: pytest tests/test_ingest.py -v
"""
import os
from pathlib import Path

import pytest

# Resolve repo root (two levels up from tests/)
REPO_ROOT = str(Path(__file__).parent.parent.parent)
SAMPLE_FILE = os.path.join(REPO_ROOT, "docs", "chapter-01-introduction", "index.md")
INTRO_FILE = os.path.join(REPO_ROOT, "docs", "intro.md")

# Only run file-dependent tests if the files exist
requires_sample = pytest.mark.skipif(
    not os.path.exists(SAMPLE_FILE),
    reason=f"Sample file not found: {SAMPLE_FILE}",
)


def test_chunk_file_imports():
    """chunk_markdown module imports without error."""
    from services.chunk_markdown import chunk_file, _make_id  # noqa: F401

    assert callable(chunk_file)
    assert callable(_make_id)


def test_make_id_deterministic():
    """UUID5 IDs are the same for the same input on repeated calls."""
    from services.chunk_markdown import _make_id

    id1 = _make_id("docs/chapter-01/index.md", 0)
    id2 = _make_id("docs/chapter-01/index.md", 0)
    assert id1 == id2


def test_make_id_unique_across_inputs():
    """Different file or index produces a different ID."""
    from services.chunk_markdown import _make_id

    id_a = _make_id("docs/chapter-01/index.md", 0)
    id_b = _make_id("docs/chapter-01/index.md", 1)  # different index
    id_c = _make_id("docs/chapter-02/index.md", 0)  # different file

    assert id_a != id_b
    assert id_a != id_c
    assert id_b != id_c


@requires_sample
def test_chunk_file_returns_chunks():
    """Chunking a real chapter file produces at least one chunk."""
    from services.chunk_markdown import chunk_file

    chunks = chunk_file(SAMPLE_FILE, REPO_ROOT)
    assert len(chunks) > 0


@requires_sample
def test_chunk_metadata_chapter_num():
    """Chapter 1 file produces chunks with chapter_num=1."""
    from services.chunk_markdown import chunk_file

    chunks = chunk_file(SAMPLE_FILE, REPO_ROOT)
    assert all(c.chapter_num == 1 for c in chunks)


@requires_sample
def test_chunk_metadata_source_file():
    """source_file field is a relative path starting with docs/."""
    from services.chunk_markdown import chunk_file

    chunks = chunk_file(SAMPLE_FILE, REPO_ROOT)
    assert all(c.source_file.startswith("docs/") for c in chunks)


@requires_sample
def test_chunk_ids_deterministic_on_repeat():
    """Running chunk_file twice on the same file produces identical IDs."""
    from services.chunk_markdown import chunk_file

    chunks1 = chunk_file(SAMPLE_FILE, REPO_ROOT)
    chunks2 = chunk_file(SAMPLE_FILE, REPO_ROOT)
    assert [c.id for c in chunks1] == [c.id for c in chunks2]


@requires_sample
def test_chunk_token_budget():
    """No chunk exceeds MAX_CHUNK_TOKENS (default 800)."""
    import tiktoken
    from services.chunk_markdown import chunk_file

    encoder = tiktoken.get_encoding("cl100k_base")
    max_tokens = int(os.getenv("MAX_CHUNK_TOKENS", "800"))
    chunks = chunk_file(SAMPLE_FILE, REPO_ROOT)

    for chunk in chunks:
        token_count = len(encoder.encode(chunk.text))
        assert token_count <= max_tokens, (
            f"Chunk '{chunk.section_title}' has {token_count} tokens (max={max_tokens})"
        )
