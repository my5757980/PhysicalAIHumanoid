"""Unit tests for RAG service and prompt builder.

No external API calls — all Qdrant/OpenAI calls are mocked.
Run with: pytest tests/test_rag_service.py -v
"""
from unittest.mock import AsyncMock, patch

import pytest

from models.schemas import HistoryMessage


# ── RAG service tests ─────────────────────────────────────────────────────────

def test_extract_chapter_num_from_url():
    """Chapter number is correctly extracted from Docusaurus URL."""
    from services.rag_service import _extract_chapter_num

    assert _extract_chapter_num("/docs/chapter-07-nvidia-isaac/") == 7
    assert _extract_chapter_num("/docs/chapter-01-introduction/what-is-physical-ai") == 1
    assert _extract_chapter_num("/docs/intro") is None
    assert _extract_chapter_num(None) is None
    assert _extract_chapter_num("") is None


@pytest.mark.asyncio
async def test_retrieve_general_mode():
    """retrieve() calls qdrant.search without chapter filter in general mode."""
    with (
        patch("services.rag_service.embed_query", new_callable=AsyncMock) as mock_embed,
        patch("services.rag_service.qdrant.search", new_callable=AsyncMock) as mock_search,
    ):
        mock_embed.return_value = [0.0] * 1536
        mock_search.return_value = []

        from services.rag_service import retrieve

        await retrieve("What is ROS 2?")

        mock_embed.assert_called_once_with("What is ROS 2?")
        mock_search.assert_called_once()
        # General mode: no chapter_filter
        call_kwargs = mock_search.call_args[1]
        assert call_kwargs.get("chapter_filter") is None


@pytest.mark.asyncio
async def test_retrieve_selected_text_mode():
    """retrieve() uses chapter-filtered search when selected_text + page_url provided."""
    with (
        patch("services.rag_service.embed_query", new_callable=AsyncMock) as mock_embed,
        patch("services.rag_service.qdrant.search", new_callable=AsyncMock) as mock_search,
    ):
        mock_embed.return_value = [0.0] * 1536
        mock_search.return_value = []

        from services.rag_service import retrieve

        await retrieve(
            question="What does this mean?",
            selected_text="Isaac Sim provides photorealistic simulation",
            page_url="/docs/chapter-07-nvidia-isaac/",
        )

        # Should call search twice: once filtered, once general
        assert mock_search.call_count == 2


# ── Prompt builder tests ──────────────────────────────────────────────────────

def test_build_messages_base_structure():
    """build_messages returns system + context + ack + question (minimum 4 messages)."""
    from services.prompt_builder import build_messages

    messages = build_messages(chunks=[], question="What is ROS 2?", history=[])
    assert len(messages) >= 4
    assert messages[0]["role"] == "system"
    assert messages[-1]["role"] == "user"
    assert "What is ROS 2?" in messages[-1]["content"]


def test_build_messages_includes_context():
    """build_messages includes chunk text in the context message."""
    from services.prompt_builder import build_messages
    from services.rag_service import DocumentChunk

    chunk = DocumentChunk(
        text="ROS 2 is a robotics middleware.",
        chapter_num=3,
        chapter_title="ROS 2 Basics",
        section_title="What is ROS 2",
        source_file="docs/chapter-03/index.md",
        score=0.9,
    )
    messages = build_messages(chunks=[chunk], question="test", history=[])
    context_msg = next(m for m in messages if m["role"] == "user" and "CONTEXT:" in m["content"])
    assert "ROS 2 is a robotics middleware" in context_msg["content"]


def test_build_messages_history_capped():
    """History is capped at MAX_HISTORY_TURNS (default 6)."""
    import os
    from services.prompt_builder import build_messages

    # Create 10 history turns
    history = [
        HistoryMessage(role="user", content=f"Q{i}") if i % 2 == 0
        else HistoryMessage(role="assistant", content=f"A{i}")
        for i in range(10)
    ]
    max_turns = int(os.getenv("MAX_HISTORY_TURNS", "6"))
    messages = build_messages(chunks=[], question="test", history=history)

    # Count actual history messages (exclude system, context, ack, question)
    history_in_messages = [m for m in messages if m["content"] in [h.content for h in history]]
    assert len(history_in_messages) <= max_turns


def test_build_messages_personalization_hook():
    """user_level='beginner' adds personalization text to system prompt."""
    from services.prompt_builder import build_messages

    messages = build_messages(chunks=[], question="test", history=[], user_level="beginner")
    system_content = messages[0]["content"]
    assert "beginner" in system_content.lower()


def test_build_messages_urdu_hook():
    """translate_to='urdu' adds Urdu instruction to system prompt."""
    from services.prompt_builder import build_messages

    messages = build_messages(chunks=[], question="test", history=[], translate_to="urdu")
    system_content = messages[0]["content"]
    assert "Urdu" in system_content


def test_extract_citations_deduplication():
    """extract_citations removes duplicate chapter+section entries."""
    from services.prompt_builder import extract_citations
    from services.rag_service import DocumentChunk

    # Two chunks from same chapter+section
    chunks = [
        DocumentChunk("text1", 3, "ROS 2 Basics", "Nodes", "f.md", 0.9),
        DocumentChunk("text2", 3, "ROS 2 Basics", "Nodes", "f.md", 0.8),  # duplicate
        DocumentChunk("text3", 7, "NVIDIA Isaac", "Isaac Sim", "g.md", 0.7),
    ]
    citations = extract_citations(chunks)
    assert len(citations) == 2  # deduplicated
    chapter_nums = {c.chapter_num for c in citations}
    assert chapter_nums == {3, 7}
