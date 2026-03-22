"""Qdrant Cloud client service.

Responsibilities:
  - Collection existence check and creation
  - Idempotent point upsert (UUID5 deterministic IDs)
  - Async vector search (full-collection + chapter-filtered)

All blocking qdrant-client SDK calls are wrapped in run_in_executor
to keep FastAPI endpoints non-blocking.
"""
import asyncio
import os
from functools import partial

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

COLLECTION = os.getenv("QDRANT_COLLECTION", "physical-ai-book")
TOP_K = int(os.getenv("TOP_K", "6"))


def _get_client() -> QdrantClient:
    """Create a Qdrant client from environment variables."""
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        timeout=30.0,
    )


def ensure_collection() -> None:
    """
    Create the Qdrant collection if it doesn't exist.
    Idempotent — calling multiple times is safe.

    Vector config:
      size=384 (BAAI/bge-small-en-v1.5 via fastembed)
      distance=Cosine (standard for semantic similarity)
    """
    client = _get_client()
    existing = {c.name for c in client.get_collections().collections}
    if COLLECTION not in existing:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"[qdrant] Created collection '{COLLECTION}'")
    else:
        print(f"[qdrant] Collection '{COLLECTION}' already exists — skipping creation")


def upsert_points(points: list[PointStruct]) -> None:
    """
    Upsert points into Qdrant collection.
    Existing points with the same ID are overwritten (idempotent).
    """
    client = _get_client()
    client.upsert(collection_name=COLLECTION, points=points, wait=True)


async def search(
    vector: list[float],
    top_k: int = TOP_K,
    chapter_filter: int | None = None,
    score_threshold: float = 0.45,
) -> list[dict]:
    """
    Async vector similarity search.

    Args:
        vector: 1536-dim query embedding
        top_k: Maximum number of results to return
        chapter_filter: If set, restrict results to this chapter number
        score_threshold: Minimum cosine similarity score (0–1)

    Returns:
        List of chunk dicts with text, metadata, and score fields
    """

    def _do_search() -> list[dict]:
        client = _get_client()
        q_filter: Filter | None = None
        if chapter_filter is not None:
            q_filter = Filter(
                must=[
                    FieldCondition(
                        key="chapter_num",
                        match=MatchValue(value=chapter_filter),
                    )
                ]
            )
        response = client.query_points(
            collection_name=COLLECTION,
            query=vector,
            query_filter=q_filter,
            limit=top_k,
            score_threshold=score_threshold,
            with_payload=True,
        )
        return [
            {
                "text": r.payload.get("text", ""),
                "chapter_num": r.payload.get("chapter_num", 0),
                "chapter_title": r.payload.get("chapter_title", ""),
                "section_title": r.payload.get("section_title", ""),
                "source_file": r.payload.get("source_file", ""),
                "score": r.score,
            }
            for r in response.points
        ]

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _do_search)
