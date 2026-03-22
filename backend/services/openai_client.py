"""OpenAI-compatible client service — embeddings and streaming chat completion.

Embedding strategy:
  - Uses fastembed (local, no API key) for text embeddings.
  - Model: BAAI/bge-small-en-v1.5 (384-dim), downloaded once and cached.

LLM strategy:
  - Default: Groq (https://api.groq.com/openai/v1) via OPENAI_BASE_URL
  - Fallback: Any OpenAI-compatible provider (xAI Grok, OpenAI, etc.)
  - Model set via OPENAI_MODEL env var.
"""
import asyncio
import os
from functools import lru_cache
from typing import AsyncGenerator

from openai import AsyncOpenAI

from models.schemas import StreamChunk

CHAT_MODEL = os.getenv("OPENAI_MODEL", "llama-3.3-70b-versatile")
EMBED_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")


# ── Embeddings (fastembed, local) ─────────────────────────────────────────────

@lru_cache(maxsize=1)
def _get_fastembed():
    """Lazy-load fastembed TextEmbedding model (cached after first call)."""
    from fastembed import TextEmbedding
    return TextEmbedding(model_name=EMBED_MODEL_NAME)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Synchronous batch embedding using fastembed (local, no API key required).
    Returns list of 384-dim float vectors in the same order as input.
    Used by ingestion script.
    """
    model = _get_fastembed()
    embeddings = list(model.embed(texts))
    return [emb.tolist() for emb in embeddings]


async def embed_query(text: str) -> list[float]:
    """
    Async single-text embedding for chat endpoints.
    Wraps synchronous fastembed call in executor to avoid blocking.
    """
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, lambda: embed_texts([text]))
    return result[0]


# ── Chat (Groq / OpenAI-compatible, streaming) ───────────────────────────────

def _async_client() -> AsyncOpenAI:
    base_url = os.getenv("OPENAI_BASE_URL") or None
    return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=base_url)


async def stream_chat(
    messages: list[dict],
) -> AsyncGenerator[str, None]:
    """
    Async generator yielding SSE lines from a streaming chat completion.

    Each yielded value is a complete SSE line: `data: {...}\\n\\n`
    Event types emitted: delta, done (citations emitted by caller after stream ends).

    LLM settings:
      model: OPENAI_MODEL env var (default: llama-3.3-70b-versatile via Groq)
      temperature: 0.3
      max_tokens: 1024
    """
    client = _async_client()
    stream = await client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        stream=True,
        temperature=0.3,
        max_tokens=1024,
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            sc = StreamChunk(type="delta", content=delta)
            yield f"data: {sc.model_dump_json()}\n\n"

    done = StreamChunk(type="done")
    yield f"data: {done.model_dump_json()}\n\n"
