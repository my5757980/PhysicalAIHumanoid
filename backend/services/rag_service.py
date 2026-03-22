"""RAG Service — retrieval orchestration.

Handles:
  - Embedding the user question via OpenAI
  - Querying Qdrant (full-collection or chapter-filtered)
  - Merging filtered + general results for text-selection mode
"""
import os
import re
from dataclasses import dataclass

from services import qdrant_client as qdrant
from services.openai_client import embed_query

TOP_K = int(os.getenv("TOP_K", "6"))


@dataclass
class DocumentChunk:
    """A retrieved document chunk with full metadata for citation generation."""

    text: str
    chapter_num: int
    chapter_title: str
    section_title: str
    source_file: str
    score: float


def _extract_chapter_num(page_url: str | None) -> int | None:
    """
    Parse chapter number from a Docusaurus URL.

    Examples:
      /docs/chapter-07-nvidia-isaac/isaac-sim  →  7
      /docs/chapter-01-introduction/           →  1
      /docs/intro                              →  None
    """
    if not page_url:
        return None
    match = re.search(r"chapter-(\d+)", page_url)
    return int(match.group(1)) if match else None


async def retrieve(
    question: str,
    selected_text: str | None = None,
    page_url: str | None = None,
) -> list[DocumentChunk]:
    """
    Retrieve top-k relevant chunks from Qdrant.

    General mode (selected_text is None):
      → Full-collection search, top_k results

    Text-selection mode (selected_text provided):
      → (top_k - 2) chapter-scoped results + 2 general results
      → Deduped and merged for comprehensive context
    """
    vector = await embed_query(question)

    # Determine chapter filter (only relevant in text-selection mode)
    chapter_filter = _extract_chapter_num(page_url) if selected_text else None

    if selected_text and chapter_filter is not None:
        # Text-selection mode: prioritize chapter context + add 2 general results
        scoped = await qdrant.search(
            vector,
            top_k=max(TOP_K - 2, 1),
            chapter_filter=chapter_filter,
        )
        general = await qdrant.search(vector, top_k=2)

        # Deduplicate: prefer scoped results, add non-duplicate general results
        seen = {(r["source_file"], r["section_title"]) for r in scoped}
        merged = scoped + [r for r in general if (r["source_file"], r["section_title"]) not in seen]
        raw = merged[:TOP_K]
    else:
        # General Q&A mode: full-collection search
        raw = await qdrant.search(vector, top_k=TOP_K)

    return [
        DocumentChunk(
            text=r["text"],
            chapter_num=r["chapter_num"],
            chapter_title=r["chapter_title"],
            section_title=r["section_title"],
            source_file=r["source_file"],
            score=r["score"],
        )
        for r in raw
    ]
