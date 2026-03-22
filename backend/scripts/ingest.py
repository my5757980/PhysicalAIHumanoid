#!/usr/bin/env python3
"""
Ingestion script: chunk → embed → upsert all textbook chapters to Qdrant.

Usage (from repo root):
  python backend/scripts/ingest.py
  python backend/scripts/ingest.py --docs-dir docs/ --repo-root . --batch-size 100

Idempotent: running multiple times on the same content is safe.
Existing chunks are overwritten (UUID5 IDs are deterministic).

Manual prerequisites:
  1. Create Qdrant Cloud Free Tier cluster at https://cloud.qdrant.io
  2. Copy backend/.env.example to backend/.env
  3. Set QDRANT_URL, QDRANT_API_KEY, OPENAI_API_KEY in backend/.env
"""
import argparse
import os
import sys
import time
from pathlib import Path

# Allow running from repo root: `python backend/scripts/ingest.py`
_backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(_backend_dir))

from dotenv import load_dotenv

load_dotenv(_backend_dir / ".env")

from qdrant_client.models import PointStruct

from services.chunk_markdown import chunk_file
from services.openai_client import embed_texts
from services.qdrant_client import ensure_collection, upsert_points


def run_ingestion(
    docs_dir: str,
    repo_root: str,
    batch_size: int = 100,
) -> dict:
    """
    Run the full ingestion pipeline.

    Args:
        docs_dir: Path to the docs/ directory containing .md files
        repo_root: Absolute repo root (for relative path calculation in metadata)
        batch_size: Number of chunks to embed per API call

    Returns:
        Dict with files_processed, chunks_upserted, duration_seconds
    """
    start = time.time()

    print("[ingest] Ensuring Qdrant collection exists...")
    ensure_collection()

    docs_path = Path(docs_dir)
    md_files = sorted(docs_path.glob("**/*.md"))

    if not md_files:
        print(f"[ingest] WARNING: No .md files found in {docs_dir}")
        return {"files_processed": 0, "chunks_upserted": 0, "duration_seconds": 0.0}

    print(f"[ingest] Found {len(md_files)} markdown files in {docs_dir}")

    # ── Step 1: Chunk all files ───────────────────────────────────────────────
    all_chunks = []
    for md_file in md_files:
        try:
            file_chunks = chunk_file(str(md_file), repo_root)
            all_chunks.extend(file_chunks)
            rel = md_file.relative_to(docs_path.parent)
            print(f"[ingest]   {rel} -> {len(file_chunks)} chunk(s)")
        except Exception as exc:
            print(f"[ingest]   WARN: skipping {md_file.name}: {exc}")

    if not all_chunks:
        print("[ingest] No chunks produced — check docs/ content")
        return {"files_processed": len(md_files), "chunks_upserted": 0, "duration_seconds": round(time.time() - start, 1)}

    print(f"[ingest] Total chunks: {len(all_chunks)}")
    print(f"[ingest] Generating embeddings (model=text-embedding-3-small, batch_size={batch_size})...")

    # ── Step 2: Batch embed + upsert ─────────────────────────────────────────
    upserted = 0
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i : i + batch_size]
        texts = [c.text for c in batch]

        try:
            embeddings = embed_texts(texts)
        except Exception as exc:
            print(f"[ingest] ERROR: embedding batch {i // batch_size + 1} failed: {exc}")
            raise

        points = [
            PointStruct(
                id=chunk.id,
                vector=emb,
                payload={
                    "text": chunk.text,
                    "chapter_num": chunk.chapter_num,
                    "chapter_title": chunk.chapter_title,
                    "section_title": chunk.section_title,
                    "source_file": chunk.source_file,
                    "chunk_index": chunk.chunk_index,
                },
            )
            for chunk, emb in zip(batch, embeddings)
        ]

        upsert_points(points)
        upserted += len(points)
        batch_num = i // batch_size + 1
        total_batches = (len(all_chunks) + batch_size - 1) // batch_size
        print(f"[ingest]   Batch {batch_num}/{total_batches} upserted ({upserted}/{len(all_chunks)} chunks)")

    duration = round(time.time() - start, 1)
    print(f"[ingest] DONE: {len(md_files)} files | {upserted} chunks | {duration}s")

    return {
        "files_processed": len(md_files),
        "chunks_upserted": upserted,
        "duration_seconds": duration,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ingest Physical AI textbook chapters into Qdrant Cloud"
    )
    parser.add_argument(
        "--docs-dir",
        default=os.path.join(os.getcwd(), "docs"),
        help="Path to docs/ directory (default: ./docs)",
    )
    parser.add_argument(
        "--repo-root",
        default=os.getcwd(),
        help="Repo root for relative path calculation (default: cwd)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Chunks per embedding API call (default: 100)",
    )
    args = parser.parse_args()

    try:
        run_ingestion(
            docs_dir=args.docs_dir,
            repo_root=args.repo_root,
            batch_size=args.batch_size,
        )
    except Exception as e:
        print(f"[ingest] FATAL: {e}")
        sys.exit(1)
