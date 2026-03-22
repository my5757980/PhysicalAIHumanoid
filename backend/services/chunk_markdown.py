"""Heading-aware Markdown chunker with tiktoken token counting.

Chunking strategy:
  1. Split on ## and ### headings (section boundaries)
  2. Sections within MAX_CHUNK_TOKENS are kept as-is
  3. Oversized sections are sub-chunked with CHUNK_OVERLAP_TOKENS overlap
  4. Each chunk carries full metadata (chapter_num, chapter_title, section_title)
  5. Chunk IDs are UUID5 (deterministic from source_file + chunk_index)
     — ensures idempotent upsert on re-ingestion
"""
import os
import re
import uuid
from dataclasses import dataclass
from pathlib import Path

import frontmatter
import tiktoken

ENCODER = tiktoken.get_encoding("cl100k_base")
MAX_TOKENS = int(os.getenv("MAX_CHUNK_TOKENS", "800"))
OVERLAP_TOKENS = int(os.getenv("CHUNK_OVERLAP_TOKENS", "100"))
# UUID5 namespace — deterministic, no randomness
_NAMESPACE = uuid.NAMESPACE_DNS


@dataclass
class Chunk:
    """A single indexable unit of textbook content."""

    id: str           # UUID5 — deterministic from source_file + chunk_index
    text: str         # Raw markdown text of the chunk
    chapter_num: int  # 0 = intro, 1–10 = chapters
    chapter_title: str
    section_title: str
    source_file: str  # Relative path from repo root (e.g. docs/chapter-07-nvidia-isaac/index.md)
    chunk_index: int  # 0-based position within this file


def _token_count(text: str) -> int:
    return len(ENCODER.encode(text))


def _make_id(source_file: str, chunk_index: int) -> str:
    """Generate a deterministic UUID5 from file path + chunk index."""
    key = f"{source_file}::{chunk_index}"
    return str(uuid.uuid5(_NAMESPACE, key))


def _extract_chapter_meta(path: Path) -> tuple[int, str]:
    """
    Extract chapter number and title from the parent directory name.

    Patterns:
      chapter-07-nvidia-isaac  →  (7, "Nvidia Isaac")
      chapter-01-introduction  →  (1, "Introduction")
      intro                    →  (0, "Introduction")
    """
    folder = path.parts[-2]
    match = re.match(r"chapter-(\d+)-(.+)", folder)
    if match:
        num = int(match.group(1))
        title = match.group(2).replace("-", " ").title()
        return num, title
    if folder in ("intro", "introduction"):
        return 0, "Introduction"
    return 0, folder.replace("-", " ").title()


def chunk_file(filepath: str, repo_root: str) -> list[Chunk]:
    """
    Chunk a single markdown file into heading-bounded sections.

    Args:
        filepath: Absolute path to the markdown file
        repo_root: Absolute path to the repository root (for relative path calculation)

    Returns:
        List of Chunk objects ready for embedding and upsert
    """
    abs_path = Path(filepath)
    rel_path = str(abs_path.relative_to(repo_root)).replace("\\", "/")
    chapter_num, chapter_title = _extract_chapter_meta(abs_path)

    # Parse frontmatter (ignore metadata; use content only)
    try:
        post = frontmatter.load(filepath)
        content = post.content
    except Exception:
        # Fallback: read raw if frontmatter parse fails
        content = abs_path.read_text(encoding="utf-8")

    if not content.strip():
        return []

    # Split on ## or ### headings — preserve the heading in each chunk
    sections = re.split(r"(?=^#{2,3} )", content, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]

    # If no ## headings found, treat the whole file as one section
    if not sections:
        sections = [content.strip()]

    chunks: list[Chunk] = []
    chunk_idx = 0

    for section in sections:
        # Extract section title from the leading heading line
        heading_match = re.match(r"^#{2,3} (.+)", section)
        section_title = heading_match.group(1).strip() if heading_match else "Overview"

        tokens = _token_count(section)

        if tokens <= MAX_TOKENS:
            # Section fits within token budget — keep as-is
            chunks.append(
                Chunk(
                    id=_make_id(rel_path, chunk_idx),
                    text=section,
                    chapter_num=chapter_num,
                    chapter_title=chapter_title,
                    section_title=section_title,
                    source_file=rel_path,
                    chunk_index=chunk_idx,
                )
            )
            chunk_idx += 1
        else:
            # Section exceeds token budget — sub-chunk with overlap
            encoded = ENCODER.encode(section)
            step = MAX_TOKENS - OVERLAP_TOKENS
            i = 0
            part = 0
            while i < len(encoded):
                window = encoded[i : i + MAX_TOKENS]
                sub_text = ENCODER.decode(window)
                sub_title = section_title if part == 0 else f"{section_title} (cont. {part + 1})"
                chunks.append(
                    Chunk(
                        id=_make_id(rel_path, chunk_idx),
                        text=sub_text,
                        chapter_num=chapter_num,
                        chapter_title=chapter_title,
                        section_title=sub_title,
                        source_file=rel_path,
                        chunk_index=chunk_idx,
                    )
                )
                chunk_idx += 1
                part += 1
                i += step

    return chunks
