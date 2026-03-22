# Tasks: Integrated RAG Chatbot

**Branch**: `001-rag-chatbot`
**Input**: `specs/001-rag-chatbot/` — spec.md · plan.md · research.md · data-model.md · contracts/openapi.yaml
**Created**: 2026-03-22
**Status**: ✅ Implementation Complete (T001–T023 + Bonus T024/T025/T026)

---

## Format Legend

- **[P]** — Parallelizable (no dependency on other in-flight task)
- **[Story]** — User story from spec.md (US1–US5)
- **Deps** — Task IDs that MUST be complete before starting
- **Files** — Exact paths to create or modify

---

## Dependency Graph

```
T001 ──► T002 ──► T003 ──► T004 ──► T010 ──► T012 ──► T024
          │        │        │                   │
          │        │        └──► T005           └──► T013
          │        │              │
          │        └──► T006 ──► T007 ──► T008 ──► T009
          │
          └──► T014 ──► T015 ──► T016 ──► T017 ──► T020 ──► T021
                                           │         │
                                           └─ T018 ──┘
                                           └─ T019 ──┘
                                           └─ T022 ──►T023

T010 + T011 ──► T012 ──► T025 ──► T026 ──► T027
T013 depends on T010 + T011
T024 depends on T012 + T013 + T007

Bonus (independent):
T028 ──┐
T029 ──┼──► (wire into T011 + T017 after T026)
T030 ──┘
```

---

## Phase 1: Setup & Configuration

**Purpose**: Scaffold all project infrastructure, environment, and service clients. No user-facing code yet.
**Blocking**: Every subsequent phase depends on this phase completing cleanly.

---

### [X] T001 — Backend Project Scaffold

**Phase**: 1 · **Priority**: P0 (blocking) · **Story**: Infrastructure · **[P]** after repo init

**Description**:
Create the complete `backend/` directory tree, `requirements.txt`, `.env.example`, and `Dockerfile`. This is the zero-to-one task — nothing else can run without it.

**Files to create**:
```
backend/
├── main.py                   (empty FastAPI app stub)
├── requirements.txt
├── .env.example
├── Dockerfile
├── api/
│   ├── __init__.py
│   └── routes/
│       ├── __init__.py
│       ├── chat.py           (stub)
│       ├── health.py         (stub)
│       └── ingest.py         (stub)
├── api/middleware/
│   ├── __init__.py
│   └── rate_limit.py         (stub)
├── services/
│   ├── __init__.py
│   ├── rag_service.py        (stub)
│   ├── openai_client.py      (stub)
│   ├── qdrant_client.py      (stub)
│   └── prompt_builder.py     (stub)
├── models/
│   ├── __init__.py
│   └── schemas.py            (stub)
├── scripts/
│   └── ingest.py             (stub)
└── tests/
    ├── conftest.py
    ├── test_chat.py          (stub)
    ├── test_rag_service.py   (stub)
    └── test_ingest.py        (stub)
```

**`requirements.txt`**:
```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
openai>=1.50.0
qdrant-client>=1.12.0
python-frontmatter>=1.1.0
tiktoken>=0.8.0
pydantic>=2.9.0
python-dotenv>=1.0.0
slowapi>=0.1.9
httpx>=0.27.0
rank-bm25>=0.2.2
pytest>=8.3.0
pytest-asyncio>=0.24.0
ruff>=0.8.0
```

**`.env.example`**:
```env
# LLM Provider — OpenAI (default) or Grok (set OPENAI_BASE_URL to switch)
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=
OPENAI_MODEL=gpt-4o-mini

# Embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# Qdrant Cloud Free Tier
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=physical-ai-book

# Neon Serverless Postgres (optional — future auth/personalization)
NEON_DB_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require

# Backend
BACKEND_PORT=8000
BACKEND_CORS_ORIGINS=http://localhost:3000,https://PHYSICAL-AI-HUMANOID-ROBOTICS.vercel.app
ADMIN_SECRET=change-me-in-production

# RAG Tuning
TOP_K=6
MAX_HISTORY_TURNS=6
MAX_CHUNK_TOKENS=800
CHUNK_OVERLAP_TOKENS=100
```

**`Dockerfile`**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Acceptance Criteria**:
- [ ] `backend/` directory exists with all subdirectories and `__init__.py` files
- [ ] `requirements.txt` contains all listed packages
- [ ] `.env.example` contains all 14+ env vars with comments
- [ ] `Dockerfile` builds without error: `docker build -t rag-chatbot ./backend`
- [ ] `python -m pytest backend/tests/ --collect-only` finds all test files (even if empty)

**Notes**: Create all stub `.py` files as empty modules with a single docstring — don't implement logic yet. Grok compatibility is handled purely via env vars (`OPENAI_BASE_URL`), no code changes needed.

**Deps**: None

---

### [X] T002 — FastAPI App Entry + Health Endpoint

**Phase**: 1 · **Priority**: P0 (blocking) · **Story**: Infrastructure · **Deps**: T001

**Description**:
Implement `backend/main.py` — create the FastAPI application, register CORS middleware, attach slowapi rate limiter, and wire the health endpoint. This is the first runnable state of the backend.

**Files to modify/create**:
- `backend/main.py` — full implementation
- `backend/api/routes/health.py` — full implementation
- `backend/api/middleware/rate_limit.py` — full implementation

**`main.py`** (full):
```python
"""Physical AI RAG Chatbot — FastAPI Application Entry Point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import os

from api.middleware.rate_limit import limiter
from api.routes.health import router as health_router
# from api.routes.chat import router as chat_router      # uncomment in T012
# from api.routes.ingest import router as ingest_router  # uncomment in T008

load_dotenv()

app = FastAPI(
    title="Physical AI RAG Chatbot API",
    version="1.0.0",
    description="RAG backend for Physical AI & Humanoid Robotics textbook",
)

# CORS
origins = [o.strip() for o in os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Admin-Secret"],
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Routers
app.include_router(health_router)
```

**`api/routes/health.py`** (full):
```python
from fastapi import APIRouter
from qdrant_client import QdrantClient
import os

router = APIRouter()

@router.get("/health")
async def health_check() -> dict:
    qdrant_ok = False
    try:
        client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"), timeout=3)
        client.get_collections()
        qdrant_ok = True
    except Exception:
        pass
    return {"status": "ok", "qdrant_connected": qdrant_ok, "version": "1.0.0"}
```

**`api/middleware/rate_limit.py`** (full):
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
```

**Acceptance Criteria**:
- [ ] `uvicorn main:app --reload` starts without errors (from `backend/` dir with `.env` populated)
- [ ] `GET http://localhost:8000/health` returns `{"status":"ok","qdrant_connected":true,"version":"1.0.0"}` (requires Qdrant URL in `.env`)
- [ ] `GET http://localhost:8000/health` returns `{"status":"ok","qdrant_connected":false}` gracefully when Qdrant is unreachable
- [ ] CORS headers present on OPTIONS preflight for `http://localhost:3000`
- [ ] `GET http://localhost:8000/docs` renders OpenAPI UI

**Notes**: Import the chat router commented out — it gets uncommented in T012. This prevents import errors before those modules exist.

**Deps**: T001

---

### [X] T003 — Pydantic v2 Schemas

**Phase**: 1 · **Priority**: P0 (blocking) · **Story**: Infrastructure · **Deps**: T001

**Description**:
Implement all Pydantic v2 request/response models in `backend/models/schemas.py`. This is the single source of truth for all API data shapes — both endpoints and tests import from here.

**Files to modify**:
- `backend/models/schemas.py` — full implementation

**Full implementation** (from data-model.md):
```python
"""Pydantic v2 schemas for RAG Chatbot API"""
from pydantic import BaseModel, Field
from typing import Literal

class Citation(BaseModel):
    chapter_num: int = Field(ge=0, le=10)
    chapter_title: str
    section_title: str

class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=4000)

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    history: list[HistoryMessage] = Field(default=[], max_length=12)
    selected_text: str | None = Field(default=None, max_length=1500)
    page_url: str | None = None
    # Bonus hooks — ignored if not populated
    user_level: Literal["beginner", "intermediate", "advanced"] | None = None
    translate_to: Literal["urdu"] | None = None

class StreamChunk(BaseModel):
    type: Literal["delta", "citations", "done", "error"]
    content: str | None = None
    citations: list[Citation] | None = None
    error: str | None = None

class IngestResponse(BaseModel):
    files_processed: int
    chunks_upserted: int
    duration_seconds: float
```

**Acceptance Criteria**:
- [ ] `from models.schemas import ChatRequest, StreamChunk, Citation, HistoryMessage, IngestResponse` succeeds
- [ ] `ChatRequest(question="test")` instantiates with defaults (`history=[]`, all optionals None)
- [ ] `ChatRequest(question="x" * 1001)` raises `ValidationError` (max_length=1000)
- [ ] `ChatRequest(question="q", history=[{"role":"user","content":"hi"}])` accepts valid history
- [ ] `StreamChunk(type="delta", content="hello")` instantiates correctly
- [ ] `ruff check models/schemas.py` passes with zero violations

**Notes**: `user_level` and `translate_to` are the bonus hook fields — they flow through to PromptBuilder in T011. No extra conditional code needed in the schema itself.

**Deps**: T001

---

### [X] T004 — Qdrant Client Service

**Phase**: 1 · **Priority**: P0 (blocking) · **Story**: US5 (Ingestion) · **Deps**: T001

**Description**:
Implement `backend/services/qdrant_client.py` — a typed service class wrapping qdrant-client. Covers: collection existence check, collection creation, point upsert, vector search (full + chapter-filtered). All methods are async-compatible (run in executor for blocking SDK calls).

**Files to modify**:
- `backend/services/qdrant_client.py` — full implementation

**Full implementation**:
```python
"""Qdrant Cloud client service — collection management + vector search"""
import os
import asyncio
from functools import partial
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue,
)
from models.schemas import Citation

COLLECTION = os.getenv("QDRANT_COLLECTION", "physical-ai-book")
TOP_K = int(os.getenv("TOP_K", "6"))

def _get_client() -> QdrantClient:
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        timeout=30.0,
    )

def ensure_collection() -> None:
    """Create collection if it doesn't exist. Idempotent."""
    client = _get_client()
    existing = {c.name for c in client.get_collections().collections}
    if COLLECTION not in existing:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        print(f"[qdrant] Created collection '{COLLECTION}'")
    else:
        print(f"[qdrant] Collection '{COLLECTION}' already exists")

def upsert_points(points: list[PointStruct]) -> None:
    """Upsert points (idempotent — existing IDs are overwritten)."""
    client = _get_client()
    client.upsert(collection_name=COLLECTION, points=points, wait=True)

async def search(
    vector: list[float],
    top_k: int = TOP_K,
    chapter_filter: int | None = None,
    score_threshold: float = 0.45,
) -> list[dict]:
    """Async vector search with optional chapter filter."""
    def _search():
        client = _get_client()
        q_filter = None
        if chapter_filter is not None:
            q_filter = Filter(
                must=[FieldCondition(key="chapter_num", match=MatchValue(value=chapter_filter))]
            )
        results = client.search(
            collection_name=COLLECTION,
            query_vector=vector,
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
            for r in results
        ]
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _search)
```

**Acceptance Criteria**:
- [ ] `ensure_collection()` creates the collection on first run; second run is a no-op with no error
- [ ] `upsert_points([PointStruct(id=1, vector=[0.0]*1536, payload={"text":"test","chapter_num":1,"chapter_title":"Intro","section_title":"Basics","source_file":"docs/ch1.md"})])` runs without error
- [ ] `await search([0.0]*1536, top_k=3)` returns a list (empty if no data, ≤3 items if data present)
- [ ] `await search([0.0]*1536, chapter_filter=1)` only returns chunks where `chapter_num==1`
- [ ] All functions have Python type hints; `ruff check services/qdrant_client.py` passes

**Notes**: Using `run_in_executor` keeps FastAPI endpoints non-blocking despite the synchronous qdrant-client SDK. Score threshold of 0.45 is intentionally permissive for the initial retrieval — PromptBuilder enforces answer quality, not Qdrant filter.

**Manual prerequisite** ⚠️: Create a free Qdrant Cloud cluster at https://cloud.qdrant.io and add `QDRANT_URL` + `QDRANT_API_KEY` to your `.env` before running this task's tests.

**Deps**: T001

---

### [X] T005 — OpenAI Client Service

**Phase**: 1 · **Priority**: P0 (blocking) · **Story**: Infrastructure · **Deps**: T001 · **[P]** with T004

**Description**:
Implement `backend/services/openai_client.py` — wraps the OpenAI Python SDK for two operations: (1) text embedding (sync, for ingestion script) and (2) async streaming chat completion. Supports Grok switch via `OPENAI_BASE_URL` env var.

**Files to modify**:
- `backend/services/openai_client.py` — full implementation

**Full implementation**:
```python
"""OpenAI client service — embeddings + streaming chat (Grok-compatible)"""
import os
import json
import asyncio
from openai import OpenAI, AsyncOpenAI
from typing import AsyncGenerator
from models.schemas import StreamChunk, Citation

EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def _sync_client() -> OpenAI:
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL") or None,
    )

def _async_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL") or None,
    )

def embed_texts(texts: list[str]) -> list[list[float]]:
    """Synchronous batch embedding — used in ingestion script."""
    client = _sync_client()
    response = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]

async def embed_query(text: str) -> list[float]:
    """Async single embedding — used in /chat endpoint."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: embed_texts([text]))
    return result[0]

async def stream_chat(
    messages: list[dict],
) -> AsyncGenerator[str, None]:
    """
    Yield raw SSE lines from the OpenAI streaming chat completion.
    Each yielded value is a complete `data: {...}\n\n` SSE line.
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
```

**Acceptance Criteria**:
- [ ] `embed_texts(["hello world"])` returns a `list` of length 1, first element is `list[float]` of length 1536
- [ ] `await embed_query("test")` returns `list[float]` of length 1536
- [ ] `stream_chat([{"role":"user","content":"Say hi"}])` is an async generator yielding `data: {...}\n\n` strings
- [ ] Setting `OPENAI_BASE_URL=https://api.x.ai/v1` and an xAI key allows calls to route to Grok without code changes
- [ ] `ruff check services/openai_client.py` passes

**Notes**: `temperature=0.3` for reproducibility in a grounded-answer scenario. `max_tokens=1024` prevents runaway responses on free-tier rate limits.

**Deps**: T001

---

## Phase 2: Ingestion Pipeline

**Purpose**: Index all 10 textbook chapters into Qdrant. This is US5 from the spec and the prerequisite for any RAG retrieval.
**Blocking for Phase 3**: The `/chat` endpoint returns empty results until this phase is complete.

---

### [X] T006 — Markdown Chunker

**Phase**: 2 · **Priority**: P1 · **Story**: US5 (Ingestion) · **Deps**: T001

**Description**:
Implement `backend/services/chunk_markdown.py` — a heading-aware markdown chunker that splits documents on `##` and `###` headings, respects a token budget (via tiktoken), and produces chunks with full metadata extracted from the file path and frontmatter.

**Files to create**:
- `backend/services/chunk_markdown.py` — full implementation

**Full implementation**:
```python
"""Heading-aware markdown chunker with tiktoken token counting"""
import re
import uuid
import os
from pathlib import Path
from dataclasses import dataclass
import frontmatter
import tiktoken

ENCODER = tiktoken.get_encoding("cl100k_base")
MAX_TOKENS = int(os.getenv("MAX_CHUNK_TOKENS", "800"))
OVERLAP_TOKENS = int(os.getenv("CHUNK_OVERLAP_TOKENS", "100"))
NAMESPACE = uuid.NAMESPACE_DNS

@dataclass
class Chunk:
    id: str          # UUID5 deterministic
    text: str
    chapter_num: int
    chapter_title: str
    section_title: str
    source_file: str  # relative path from repo root
    chunk_index: int

def _token_count(text: str) -> int:
    return len(ENCODER.encode(text))

def _make_id(source_file: str, chunk_index: int) -> str:
    return str(uuid.uuid5(NAMESPACE, f"{source_file}::{chunk_index}"))

def _extract_chapter_meta(path: Path) -> tuple[int, str]:
    """Extract chapter number and title from directory name."""
    folder = path.parts[-2]  # e.g. "chapter-07-nvidia-isaac"
    match = re.match(r"chapter-(\d+)-(.+)", folder)
    if match:
        num = int(match.group(1))
        title = match.group(2).replace("-", " ").title()
        return num, title
    if folder == "intro":
        return 0, "Introduction"
    return 0, folder.title()

def chunk_file(filepath: str, repo_root: str) -> list[Chunk]:
    """
    Chunk a single markdown file into heading-bounded sections.
    Sections exceeding MAX_TOKENS are split with OVERLAP_TOKENS overlap.
    """
    abs_path = Path(filepath)
    rel_path = str(abs_path.relative_to(repo_root))
    chapter_num, chapter_title = _extract_chapter_meta(abs_path)

    post = frontmatter.load(filepath)
    content = post.content

    # Split on ## or ### headings (preserve the heading in each chunk)
    sections = re.split(r"(?=^#{2,3} )", content, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]

    chunks: list[Chunk] = []
    chunk_idx = 0

    for section in sections:
        # Extract section title from first heading line
        heading_match = re.match(r"^#{2,3} (.+)", section)
        section_title = heading_match.group(1).strip() if heading_match else "Overview"

        tokens = _token_count(section)
        if tokens <= MAX_TOKENS:
            chunks.append(Chunk(
                id=_make_id(rel_path, chunk_idx),
                text=section,
                chapter_num=chapter_num,
                chapter_title=chapter_title,
                section_title=section_title,
                source_file=rel_path,
                chunk_index=chunk_idx,
            ))
            chunk_idx += 1
        else:
            # Sub-chunk by words with overlap
            words = section.split()
            enc_words = ENCODER.encode(section)
            step = MAX_TOKENS - OVERLAP_TOKENS
            i = 0
            while i < len(enc_words):
                window = enc_words[i:i + MAX_TOKENS]
                sub_text = ENCODER.decode(window)
                chunks.append(Chunk(
                    id=_make_id(rel_path, chunk_idx),
                    text=sub_text,
                    chapter_num=chapter_num,
                    chapter_title=chapter_title,
                    section_title=f"{section_title} (part {chunk_idx})",
                    source_file=rel_path,
                    chunk_index=chunk_idx,
                ))
                chunk_idx += 1
                i += step

    return chunks
```

**Acceptance Criteria**:
- [ ] `chunk_file("docs/chapter-07-nvidia-isaac/index.md", repo_root)` returns a non-empty list of `Chunk` objects
- [ ] Each `Chunk` has `chapter_num=7`, `chapter_title="Nvidia Isaac"`, non-empty `section_title`
- [ ] All chunks have `_token_count(chunk.text) <= MAX_TOKENS` (800)
- [ ] Two calls on the same file produce identical `id` values (UUID5 determinism)
- [ ] `chunk_file` on a stub file with only frontmatter returns an empty list (no error)
- [ ] `ruff check services/chunk_markdown.py` passes

**Deps**: T001

---

### [X] T007 — Ingestion CLI Script

**Phase**: 2 · **Priority**: P1 · **Story**: US5 · **Deps**: T004, T005, T006

**Description**:
Implement `backend/scripts/ingest.py` — the CLI ingestion script. Walks `docs/` recursively, chunks every `.md` file, batch-embeds with OpenAI, and upserts to Qdrant. Idempotent via UUID5 IDs. Reports statistics on completion.

**Files to create/modify**:
- `backend/scripts/ingest.py` — full implementation

**Full implementation**:
```python
#!/usr/bin/env python3
"""
Ingestion script: chunk → embed → upsert all textbook chapters to Qdrant.
Usage: python backend/scripts/ingest.py [--docs-dir docs/] [--batch-size 100]
Idempotent: safe to re-run; existing chunks are overwritten by UUID5 ID.
"""
import argparse
import time
import sys
import os
from pathlib import Path

# Add backend to path when run from repo root
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from services.chunk_markdown import chunk_file
from services.openai_client import embed_texts
from services.qdrant_client import ensure_collection, upsert_points
from qdrant_client.models import PointStruct

def run_ingestion(docs_dir: str, repo_root: str, batch_size: int = 100) -> dict:
    start = time.time()
    ensure_collection()

    md_files = list(Path(docs_dir).glob("**/*.md"))
    print(f"[ingest] Found {len(md_files)} markdown files")

    all_chunks = []
    for md_file in md_files:
        try:
            chunks = chunk_file(str(md_file), repo_root)
            all_chunks.extend(chunks)
            print(f"[ingest]   {md_file.relative_to(repo_root)} → {len(chunks)} chunks")
        except Exception as e:
            print(f"[ingest]   WARN: skipping {md_file}: {e}")

    print(f"[ingest] Total chunks: {len(all_chunks)}")
    print(f"[ingest] Generating embeddings (batch_size={batch_size})...")

    upserted = 0
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        texts = [c.text for c in batch]
        embeddings = embed_texts(texts)

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
        print(f"[ingest]   Upserted batch {i // batch_size + 1} ({upserted}/{len(all_chunks)})")

    duration = round(time.time() - start, 1)
    print(f"[ingest] ✓ Complete: {len(md_files)} files, {upserted} chunks, {duration}s")
    return {"files_processed": len(md_files), "chunks_upserted": upserted, "duration_seconds": duration}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", default="docs")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()
    run_ingestion(args.docs_dir, args.repo_root, args.batch_size)
```

**Acceptance Criteria**:
- [ ] `python backend/scripts/ingest.py --docs-dir docs/ --repo-root .` runs to completion with non-zero chunks upserted
- [ ] Running it twice produces the same chunk count in Qdrant (no duplicates)
- [ ] Qdrant Cloud dashboard shows points in `physical-ai-book` collection after run
- [ ] Script exits with code 0 on success, non-zero on connection failure
- [ ] Chapter 7 content is retrievable: running a test query for "Isaac Sim" returns ≥1 result from chapter 7
- [ ] Console output shows per-file chunk counts

**Notes**: Run from repo root: `python backend/scripts/ingest.py`. The script adds `backend/` to `sys.path` automatically. This must succeed before testing any chat endpoints.

**Manual prerequisite** ⚠️: Ensure `.env` has valid `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY` before running.

**Deps**: T004, T005, T006

---

### [X] T008 — Admin `/ingest` Endpoint

**Phase**: 2 · **Priority**: P2 · **Story**: US5 · **Deps**: T007, T002

**Description**:
Implement `backend/api/routes/ingest.py` — a protected `POST /ingest` endpoint that triggers the ingestion pipeline. Protected by `X-Admin-Secret` header. Register the router in `main.py`. Useful for CI/CD re-indexing without SSH access.

**Files to modify/create**:
- `backend/api/routes/ingest.py` — full implementation
- `backend/main.py` — uncomment ingest router import

**`api/routes/ingest.py`**:
```python
"""Admin endpoint to trigger document ingestion"""
import os
from fastapi import APIRouter, HTTPException, Header
from models.schemas import IngestResponse
from scripts.ingest import run_ingestion

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
async def trigger_ingest(x_admin_secret: str | None = Header(default=None)) -> IngestResponse:
    if x_admin_secret != os.getenv("ADMIN_SECRET"):
        raise HTTPException(status_code=403, detail="Invalid admin secret")
    result = run_ingestion(docs_dir="docs", repo_root=os.getenv("REPO_ROOT", "."))
    return IngestResponse(**result)
```

**Acceptance Criteria**:
- [ ] `POST /ingest` without `X-Admin-Secret` returns `403 Forbidden`
- [ ] `POST /ingest` with wrong secret returns `403 Forbidden`
- [ ] `POST /ingest` with correct secret runs ingestion and returns `IngestResponse` JSON
- [ ] Response includes `files_processed`, `chunks_upserted`, `duration_seconds` with correct types

**Deps**: T007, T002

---

### [X] T009 — Ingestion Verification Test

**Phase**: 2 · **Priority**: P1 · **Story**: US5 · **Deps**: T007

**Description**:
Write `backend/tests/test_ingest.py` — unit tests for the chunker and integration test for the full ingestion pipeline. Verify chunk ID determinism, metadata extraction accuracy, and Qdrant query returns relevant results.

**Files to modify**:
- `backend/tests/test_ingest.py` — full test suite

```python
"""Tests for ingestion pipeline"""
import pytest
from pathlib import Path
from services.chunk_markdown import chunk_file, _make_id

REPO_ROOT = str(Path(__file__).parent.parent.parent)
SAMPLE_FILE = f"{REPO_ROOT}/docs/chapter-01-introduction/index.md"

def test_chunk_file_returns_chunks():
    chunks = chunk_file(SAMPLE_FILE, REPO_ROOT)
    assert len(chunks) > 0

def test_chunk_metadata_correct():
    chunks = chunk_file(SAMPLE_FILE, REPO_ROOT)
    assert chunks[0].chapter_num == 1
    assert "Introduction" in chunks[0].chapter_title or "introduction" in chunks[0].chapter_title.lower()
    assert chunks[0].source_file.startswith("docs/")

def test_chunk_ids_deterministic():
    chunks1 = chunk_file(SAMPLE_FILE, REPO_ROOT)
    chunks2 = chunk_file(SAMPLE_FILE, REPO_ROOT)
    assert [c.id for c in chunks1] == [c.id for c in chunks2]

def test_make_id_different_for_different_inputs():
    id1 = _make_id("docs/ch1.md", 0)
    id2 = _make_id("docs/ch1.md", 1)
    id3 = _make_id("docs/ch2.md", 0)
    assert id1 != id2 != id3
```

**Acceptance Criteria**:
- [ ] `pytest backend/tests/test_ingest.py -v` passes all 4 tests
- [ ] Tests run without requiring Qdrant connection (unit tests only)
- [ ] Zero failing assertions

**Deps**: T006

---

## Phase 3: Backend API & RAG Logic

**Purpose**: Implement the full RAG pipeline — retrieval, prompt building, and streaming chat generation. Delivers US1 (General Q&A) and US4 (Source Citations) in backend form.
**Note**: The frontend in Phase 4 will call these endpoints. You can test them directly with `curl` or the OpenAPI UI at `/docs`.

---

### [X] T010 — RAG Service: Retrieve

**Phase**: 3 · **Priority**: P1 · **Story**: US1, US2 · **Deps**: T004, T005

**Description**:
Implement the retrieval half of `backend/services/rag_service.py`. Takes a question (and optional chapter filter), embeds it, queries Qdrant, and returns ranked `DocumentChunk` results for use by the prompt builder.

**Files to modify**:
- `backend/services/rag_service.py` — retrieval portion

```python
"""RAG Service — retrieval and generation orchestration"""
import os
import re
from dataclasses import dataclass
from services.openai_client import embed_query
from services import qdrant_client as qdrant

TOP_K = int(os.getenv("TOP_K", "6"))

@dataclass
class DocumentChunk:
    text: str
    chapter_num: int
    chapter_title: str
    section_title: str
    source_file: str
    score: float

def _extract_chapter_num(page_url: str | None) -> int | None:
    """Parse chapter number from a URL like /docs/chapter-07-nvidia-isaac/..."""
    if not page_url:
        return None
    match = re.search(r"chapter-(\d+)", page_url)
    return int(match.group(1)) if match else None

async def retrieve(
    question: str,
    selected_text: str | None = None,
    page_url: str | None = None,
) -> list[DocumentChunk]:
    """Retrieve top-k relevant chunks from Qdrant."""
    vector = await embed_query(question)
    chapter_filter = _extract_chapter_num(page_url) if selected_text else None

    if selected_text and chapter_filter:
        # Text-selection mode: 4 chapter-scoped + 2 general
        scoped = await qdrant.search(vector, top_k=TOP_K - 2, chapter_filter=chapter_filter)
        general = await qdrant.search(vector, top_k=2)
        seen_ids = {r["source_file"] + r["section_title"] for r in scoped}
        merged = scoped + [r for r in general if r["source_file"] + r["section_title"] not in seen_ids]
        raw = merged[:TOP_K]
    else:
        raw = await qdrant.search(vector, top_k=TOP_K)

    return [DocumentChunk(**{k: v for k, v in r.items() if k != "score"}, score=r["score"]) for r in raw]
```

**Acceptance Criteria**:
- [ ] `await retrieve("What is ROS 2?")` returns a non-empty list after ingestion completes (T007)
- [ ] `await retrieve("What is Isaac Sim?", selected_text="x", page_url="/docs/chapter-07-nvidia-isaac/")` returns chunks with `chapter_num=7` in majority
- [ ] `await retrieve("unrelated nonsense qxzqz")` returns an empty list or list with low-score chunks — no error
- [ ] Return type is `list[DocumentChunk]` with all fields populated

**Deps**: T004, T005

---

### [X] T011 — Prompt Builder

**Phase**: 3 · **Priority**: P1 · **Story**: US1, US4 · **Deps**: T010

**Description**:
Implement `backend/services/prompt_builder.py` — builds the full OpenAI message list from retrieved chunks, conversation history, and the citation-enforcing system prompt. Includes bonus hooks for `user_level` and `translate_to`.

**Files to modify**:
- `backend/services/prompt_builder.py` — full implementation

```python
"""Prompt builder — citation-enforced RAG generation prompts"""
from models.schemas import HistoryMessage, Citation
from services.rag_service import DocumentChunk

SYSTEM_PROMPT = """You are a knowledgeable teaching assistant for the "Physical AI & Humanoid Robotics" textbook by Panaversity.

STRICT RULES:
1. Answer ONLY using the provided Context chunks. NEVER use outside knowledge.
2. If the answer cannot be found in the Context, respond EXACTLY:
   "This topic is not covered in the current textbook content. Try asking about ROS 2, Gazebo, NVIDIA Isaac, or humanoid robotics."
3. End EVERY answer with a "**Sources:**" section listing each chunk used:
   - Chapter {N} — {chapter_title} › {section_title}
4. Use markdown formatting (headers, bullet points, code blocks) where it aids clarity.
5. Be concise and educational. Aim for 2–4 paragraphs maximum."""

def build_messages(
    chunks: list[DocumentChunk],
    question: str,
    history: list[HistoryMessage],
    selected_text: str | None = None,
    user_level: str | None = None,
    translate_to: str | None = None,
) -> list[dict]:
    """Build the full message list for OpenAI chat completion."""
    system = SYSTEM_PROMPT

    # Bonus: personalization hook
    if user_level:
        system += f"\n\nThe learner has a **{user_level}** background. Adjust explanation depth accordingly: {'use analogies and avoid jargon' if user_level == 'beginner' else 'balance depth with practical examples' if user_level == 'intermediate' else 'use technical depth, skip basics'}."

    # Bonus: Urdu translation hook
    if translate_to == "urdu":
        system += "\n\nRespond in **Urdu**. Keep technical terms (ROS 2, URDF, Gazebo, etc.) in English with Urdu explanations in parentheses."

    # Build context block from retrieved chunks
    if chunks:
        context_parts = [
            f"[Chapter {c.chapter_num} — {c.chapter_title} › {c.section_title}]\n{c.text}"
            for c in chunks
        ]
        context_block = "\n\n---\n\n".join(context_parts)
    else:
        context_block = "(No relevant content found in the textbook for this query.)"

    messages: list[dict] = [{"role": "system", "content": system}]

    # Inject context as a system-level user message (keeps it out of visible history)
    messages.append({"role": "user", "content": f"CONTEXT:\n{context_block}"})
    messages.append({"role": "assistant", "content": "Understood. I will answer only from this context."})

    # Add conversation history (last MAX_HISTORY_TURNS turns)
    import os
    max_turns = int(os.getenv("MAX_HISTORY_TURNS", "6"))
    for msg in history[-max_turns:]:
        messages.append({"role": msg.role, "content": msg.content})

    # Selected text injection
    if selected_text:
        question = f'[Regarding the highlighted text: "{selected_text[:300]}..."]\n\n{question}'

    messages.append({"role": "user", "content": question})
    return messages

def extract_citations(chunks: list[DocumentChunk]) -> list[Citation]:
    """Convert retrieved chunks to Citation objects for the response."""
    seen = set()
    citations = []
    for c in chunks:
        key = (c.chapter_num, c.chapter_title, c.section_title)
        if key not in seen:
            seen.add(key)
            citations.append(Citation(
                chapter_num=c.chapter_num,
                chapter_title=c.chapter_title,
                section_title=c.section_title,
            ))
    return citations
```

**Acceptance Criteria**:
- [ ] `build_messages(chunks=[], question="test", history=[])` returns a message list with at least system + context + question (3 messages)
- [ ] `build_messages(chunks=[...], ...)` includes all chunk texts in the context message
- [ ] `build_messages(..., user_level="beginner")` adds personalization text to system prompt
- [ ] `build_messages(..., translate_to="urdu")` adds Urdu instruction to system prompt
- [ ] `extract_citations(chunks)` returns deduplicated `Citation` objects (no duplicate chapter+section)
- [ ] History is capped at `MAX_HISTORY_TURNS` (default 6) — longer histories are truncated from the front

**Deps**: T003, T010

---

### [X] T012 — `/chat` General Q&A Endpoint

**Phase**: 3 · **Priority**: P1 · **Story**: US1, US4 · **Deps**: T011, T005, T002

**Description**:
Implement `backend/api/routes/chat.py` — the `POST /chat` SSE streaming endpoint for general Q&A. Orchestrates: validate → retrieve → build prompt → stream → emit citations event. Register router in `main.py`.

**Files to modify/create**:
- `backend/api/routes/chat.py` — full implementation
- `backend/main.py` — uncomment `from api.routes.chat import router as chat_router`

```python
"""POST /chat — General Q&A SSE streaming endpoint"""
import json
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from api.middleware.rate_limit import limiter
from models.schemas import ChatRequest, StreamChunk
from services.rag_service import retrieve
from services.prompt_builder import build_messages, extract_citations
from services.openai_client import stream_chat

router = APIRouter()

async def _rag_stream(req: ChatRequest):
    """Core RAG + generation stream — shared by /chat and /chat/selected"""
    # 1. Retrieve
    chunks = await retrieve(
        question=req.question,
        selected_text=req.selected_text,
        page_url=req.page_url,
    )

    # 2. Build prompt
    messages = build_messages(
        chunks=chunks,
        question=req.question,
        history=req.history,
        selected_text=req.selected_text,
        user_level=req.user_level,
        translate_to=req.translate_to,
    )

    # 3. Stream generation
    async for sse_line in stream_chat(messages):
        yield sse_line

    # 4. Emit citations after stream completes
    citations = extract_citations(chunks)
    cite_chunk = StreamChunk(type="citations", citations=citations)
    yield f"data: {cite_chunk.model_dump_json()}\n\n"

@router.post("/chat")
@limiter.limit("10/minute")
async def chat(request: Request, body: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        _rag_stream(body),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

**Acceptance Criteria**:
- [ ] `POST /chat {"question":"What is ROS 2?"}` streams `data: {"type":"delta","content":"..."}` lines followed by `data: {"type":"citations",...}` then `data: {"type":"done",...}`
- [ ] Response `Content-Type` header is `text/event-stream`
- [ ] Response headers include `X-Accel-Buffering: no`
- [ ] 11th request within 60 seconds from the same IP returns `429 Too Many Requests`
- [ ] `POST /chat {"question":""}` returns `422 Unprocessable Entity`
- [ ] Asking an off-topic question returns a stream containing "not covered in the current textbook"

**Deps**: T011, T005, T002

---

### [X] T013 — `/chat/selected` Text-Selection Endpoint

**Phase**: 3 · **Priority**: P2 · **Story**: US2 · **Deps**: T012

**Description**:
Implement `POST /chat/selected` — routes to the same `_rag_stream` helper (in T012) since `selected_text` is already part of `ChatRequest`. Add a dedicated route that validates `selected_text` is present and non-empty.

**Files to modify**:
- `backend/api/routes/chat.py` — add `/chat/selected` route

```python
@router.post("/chat/selected")
@limiter.limit("10/minute")
async def chat_selected(request: Request, body: ChatRequest) -> StreamingResponse:
    if not body.selected_text or not body.selected_text.strip():
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="selected_text is required for /chat/selected")
    return StreamingResponse(
        _rag_stream(body),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

**Acceptance Criteria**:
- [ ] `POST /chat/selected {"question":"What does this mean?","selected_text":"Isaac Sim provides photorealistic simulation"}` returns streaming response citing Chapter 7
- [ ] `POST /chat/selected {"question":"test"}` (no `selected_text`) returns `422 Unprocessable Entity`
- [ ] Response prioritizes chapter-scoped chunks when `page_url` includes a chapter path
- [ ] Citations in response reference the chapter matching the `page_url`

**Deps**: T012

---

### [X] T014 — Backend Test Suite

**Phase**: 3 · **Priority**: P2 · **Story**: All · **Deps**: T012, T013, T009

**Description**:
Implement `backend/tests/test_chat.py` and `backend/tests/test_rag_service.py` — integration tests using FastAPI's `TestClient` and unit tests for the RAG service. Target ≥60% coverage as per constitution §V.

**Files to modify**:
- `backend/tests/test_chat.py`
- `backend/tests/test_rag_service.py`
- `backend/tests/conftest.py`

**`conftest.py`**:
```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_rag():
    with patch("api.routes.chat.retrieve", new_callable=AsyncMock) as mock_retrieve, \
         patch("api.routes.chat.stream_chat") as mock_stream:
        mock_retrieve.return_value = []
        async def _fake_stream(messages):
            yield 'data: {"type":"delta","content":"Test answer"}\n\n'
            yield 'data: {"type":"done"}\n\n'
        mock_stream.side_effect = _fake_stream
        yield mock_retrieve, mock_stream
```

**`test_chat.py`**:
```python
def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_chat_empty_question(client):
    r = client.post("/chat", json={"question": ""})
    assert r.status_code == 422

def test_chat_question_too_long(client):
    r = client.post("/chat", json={"question": "x" * 1001})
    assert r.status_code == 422

def test_chat_streams(client, mock_rag):
    with client.stream("POST", "/chat", json={"question": "What is ROS 2?"}) as r:
        assert r.status_code == 200
        assert "text/event-stream" in r.headers["content-type"]

def test_chat_selected_missing_text(client):
    r = client.post("/chat/selected", json={"question": "What does this mean?"})
    assert r.status_code == 422

def test_ingest_wrong_secret(client):
    r = client.post("/ingest", headers={"X-Admin-Secret": "wrong"})
    assert r.status_code == 403
```

**Acceptance Criteria**:
- [ ] `pytest backend/tests/ -v` passes all tests
- [ ] `pytest backend/tests/ --cov=backend --cov-report=term` shows ≥60% coverage
- [ ] Tests run without real Qdrant/OpenAI connections (mocked)
- [ ] CI can run tests offline (no external API calls)

**Deps**: T012, T013, T009

---

## Phase 4: Frontend Chat Widget

**Purpose**: Build and integrate the React chat widget into Docusaurus. Delivers the frontend half of US1 (General Q&A), US3 (Multi-turn), and the widget infrastructure for US2 and US4.

---

### [X] T015 — TypeScript Types + Config

**Phase**: 4 · **Priority**: P1 · **Story**: US1 · **Deps**: T001 · **[P]** with T012

**Description**:
Create `src/components/ChatWidget/types.ts` and `src/components/ChatWidget/config.ts` — shared TypeScript interfaces and the API base URL configuration. These are the foundation that all other widget components import from.

**Files to create**:
- `src/components/ChatWidget/types.ts`
- `src/components/ChatWidget/config.ts`

**`types.ts`**:
```typescript
export interface Citation {
  chapter_num: number;
  chapter_title: string;
  section_title: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations: Citation[];
  timestamp: Date;
  isStreaming?: boolean;
}

export interface ChatState {
  messages: Message[];
  isOpen: boolean;
  isLoading: boolean;
  selectedText: string;
  error: string | null;
}
```

**`config.ts`**:
```typescript
// Use docusaurus customFields or environment-based URL
const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';

export const CHAT_API_BASE = isDev
  ? 'http://localhost:8000'
  : (process.env.CHAT_API_BASE ?? 'https://your-backend.railway.app');
```

**Acceptance Criteria**:
- [ ] `import type { Message, Citation, ChatState } from './types'` compiles without error
- [ ] `import { CHAT_API_BASE } from './config'` compiles without error
- [ ] `npm run typecheck` passes with zero errors for these files
- [ ] `CHAT_API_BASE` resolves to `http://localhost:8000` in dev mode

**Deps**: None (pure TypeScript, no external dependencies)

---

### [X] T016 — `useTextSelection` Hook

**Phase**: 4 · **Priority**: P2 · **Story**: US2 · **[P]** with T017

**Description**:
Create `src/components/ChatWidget/hooks/useTextSelection.ts` — a React hook that listens for `selectionchange` events and stores selected text. Debounced (300ms), minimum 20 characters, maximum 1500 characters.

**Files to create**:
- `src/components/ChatWidget/hooks/useTextSelection.ts`

```typescript
import { useState, useEffect } from 'react';

export function useTextSelection(): [string, () => void] {
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    let debounceTimer: ReturnType<typeof setTimeout>;

    const handleSelection = () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        const selection = window.getSelection()?.toString().trim() ?? '';
        if (selection.length >= 20) {
          setSelectedText(selection.slice(0, 1500));
        } else {
          setSelectedText('');
        }
      }, 300);
    };

    document.addEventListener('selectionchange', handleSelection);
    return () => {
      document.removeEventListener('selectionchange', handleSelection);
      clearTimeout(debounceTimer);
    };
  }, []);

  const clearSelection = () => setSelectedText('');

  return [selectedText, clearSelection];
}
```

**Acceptance Criteria**:
- [ ] Hook returns `[selectedText: string, clearSelection: () => void]`
- [ ] Selecting ≥20 characters on a page sets `selectedText` to that text (after 300ms debounce)
- [ ] Selecting <20 characters sets `selectedText` to empty string
- [ ] Text longer than 1500 characters is truncated at 1500
- [ ] Calling `clearSelection()` resets `selectedText` to empty string
- [ ] `npm run typecheck` passes

**Deps**: T015

---

### [X] T017 — `useChat` Hook

**Phase**: 4 · **Priority**: P1 · **Story**: US1, US3 · **Deps**: T015

**Description**:
Create `src/components/ChatWidget/hooks/useChat.ts` — the core state management hook. Handles: sending messages via Fetch+ReadableStream (SSE POST), accumulating streamed content, managing multi-turn history, and extracting citations from the `citations` SSE event.

**Files to create**:
- `src/components/ChatWidget/hooks/useChat.ts`

```typescript
import { useState, useCallback } from 'react';
import { Message, Citation } from '../types';
import { CHAT_API_BASE } from '../config';

function nanoid(): string {
  return Math.random().toString(36).slice(2, 10);
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(async (
    question: string,
    selectedText?: string,
    pageUrl?: string,
  ) => {
    if (!question.trim() || isLoading) return;

    const userMsg: Message = {
      id: nanoid(), role: 'user', content: question,
      citations: [], timestamp: new Date(),
    };
    const assistantId = nanoid();
    const assistantMsg: Message = {
      id: assistantId, role: 'assistant', content: '',
      citations: [], timestamp: new Date(), isStreaming: true,
    };

    setMessages(prev => [...prev, userMsg, assistantMsg]);
    setIsLoading(true);
    setError(null);

    // Build history from prior messages (last 12, exclude the just-added ones)
    const history = messages.slice(-12).map(m => ({
      role: m.role,
      content: m.content,
    }));

    const endpoint = selectedText ? '/chat/selected' : '/chat';
    const body = {
      question,
      history,
      selected_text: selectedText || undefined,
      page_url: pageUrl || (typeof window !== 'undefined' ? window.location.pathname : undefined),
    };

    try {
      const response = await fetch(`${CHAT_API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      if (!response.body) throw new Error('No response body');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() ?? '';

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          try {
            const chunk = JSON.parse(line.slice(6));
            if (chunk.type === 'delta') {
              setMessages(prev => prev.map(m =>
                m.id === assistantId
                  ? { ...m, content: m.content + chunk.content }
                  : m
              ));
            } else if (chunk.type === 'citations') {
              setMessages(prev => prev.map(m =>
                m.id === assistantId
                  ? { ...m, citations: chunk.citations ?? [], isStreaming: false }
                  : m
              ));
            } else if (chunk.type === 'error') {
              throw new Error(chunk.error ?? 'Unknown error');
            }
          } catch {}
        }
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Connection failed');
      setMessages(prev => prev.map(m =>
        m.id === assistantId
          ? { ...m, content: 'Sorry, I encountered an error. Please try again.', isStreaming: false }
          : m
      ));
    } finally {
      setIsLoading(false);
      setMessages(prev => prev.map(m =>
        m.id === assistantId ? { ...m, isStreaming: false } : m
      ));
    }
  }, [messages, isLoading]);

  const clearHistory = useCallback(() => setMessages([]), []);

  return { messages, isLoading, error, sendMessage, clearHistory };
}
```

**Acceptance Criteria**:
- [ ] `sendMessage("What is ROS 2?")` appends a user message and an assistant message to `messages`
- [ ] While streaming, the assistant message has `isStreaming: true`; after completion it's `false`
- [ ] `messages` contains up to 12 history turns sent to the backend (window sliding)
- [ ] On network error, `error` is set and the assistant message shows an error fallback
- [ ] `clearHistory()` resets `messages` to empty array
- [ ] `npm run typecheck` passes

**Deps**: T015

---

### [X] T018 — MessageBubble + CitationList Components

**Phase**: 4 · **Priority**: P1 · **Story**: US1, US4 · **Deps**: T015

**Description**:
Create `MessageBubble.tsx` (renders a single message with markdown and streaming cursor) and `CitationList.tsx` (renders source citations). Install `react-markdown` and `remark-gfm` for markdown rendering.

**Files to create**:
- `src/components/ChatWidget/MessageBubble.tsx`
- `src/components/ChatWidget/CitationList.tsx`

**Install dependency** (add to `package.json`):
```bash
npm install react-markdown remark-gfm
```

**`MessageBubble.tsx`**:
```tsx
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Message } from './types';
import CitationList from './CitationList';
import styles from './styles.module.css';

export default function MessageBubble({ message }: { message: Message }) {
  return (
    <div className={`${styles.bubble} ${styles[message.role]}`}>
      <div className={styles.bubbleRole}>{message.role === 'user' ? 'You' : 'Assistant'}</div>
      <div className={styles.bubbleContent}>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {message.content + (message.isStreaming ? '▌' : '')}
        </ReactMarkdown>
      </div>
      {message.citations.length > 0 && <CitationList citations={message.citations} />}
    </div>
  );
}
```

**`CitationList.tsx`**:
```tsx
import React from 'react';
import { Citation } from './types';
import styles from './styles.module.css';

export default function CitationList({ citations }: { citations: Citation[] }) {
  return (
    <div className={styles.citations}>
      <span className={styles.citationsLabel}>Sources:</span>
      {citations.map((c, i) => (
        <span key={i} className={styles.citation}>
          Ch.{c.chapter_num} — {c.chapter_title} › {c.section_title}
        </span>
      ))}
    </div>
  );
}
```

**Acceptance Criteria**:
- [ ] `MessageBubble` renders without error for both `user` and `assistant` roles
- [ ] Markdown in assistant messages is rendered (bold, code blocks, lists)
- [ ] `▌` streaming cursor appears when `message.isStreaming === true`
- [ ] `CitationList` renders all citations with chapter number and section title
- [ ] `npm run typecheck` passes for both components

**Deps**: T015

---

### [X] T019 — InputBar + SelectionBadge Components

**Phase**: 4 · **Priority**: P1 · **Story**: US1, US2 · **Deps**: T015

**Description**:
Create `InputBar.tsx` (textarea with Enter-to-send, Shift+Enter for newline) and `SelectionBadge.tsx` (shows the highlighted text context with a dismiss button).

**Files to create**:
- `src/components/ChatWidget/InputBar.tsx`
- `src/components/ChatWidget/SelectionBadge.tsx`

**`InputBar.tsx`**:
```tsx
import React, { useState, useRef, KeyboardEvent } from 'react';
import styles from './styles.module.css';

interface Props {
  onSend: (text: string) => void;
  disabled: boolean;
  placeholder?: string;
}

export default function InputBar({ onSend, disabled, placeholder = 'Ask about the textbook...' }: Props) {
  const [value, setValue] = useState('');
  const ref = useRef<HTMLTextAreaElement>(null);

  const handleKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (value.trim() && !disabled) {
        onSend(value.trim());
        setValue('');
      }
    }
  };

  return (
    <div className={styles.inputBar}>
      <textarea
        ref={ref}
        value={value}
        onChange={e => setValue(e.target.value)}
        onKeyDown={handleKey}
        disabled={disabled}
        placeholder={placeholder}
        rows={1}
        className={styles.textarea}
        aria-label="Chat input"
      />
      <button
        onClick={() => { if (value.trim() && !disabled) { onSend(value.trim()); setValue(''); } }}
        disabled={disabled || !value.trim()}
        className={styles.sendButton}
        aria-label="Send message"
      >→</button>
    </div>
  );
}
```

**`SelectionBadge.tsx`**:
```tsx
import React from 'react';
import styles from './styles.module.css';

interface Props {
  text: string;
  onClear: () => void;
}

export default function SelectionBadge({ text, onClear }: Props) {
  if (!text) return null;
  const preview = text.length > 80 ? text.slice(0, 80) + '…' : text;
  return (
    <div className={styles.selectionBadge}>
      <span className={styles.selectionLabel}>Asking about: </span>
      <span className={styles.selectionPreview}>"{preview}"</span>
      <button onClick={onClear} className={styles.selectionClear} aria-label="Clear selection">✕</button>
    </div>
  );
}
```

**Acceptance Criteria**:
- [ ] Pressing Enter in `InputBar` calls `onSend` and clears the input
- [ ] Pressing Shift+Enter adds a newline without sending
- [ ] Send button is disabled when input is empty or `disabled=true`
- [ ] `SelectionBadge` renders when `text` is non-empty, hidden when empty
- [ ] `SelectionBadge` truncates text to 80 chars with ellipsis
- [ ] Clicking ✕ in `SelectionBadge` calls `onClear`

**Deps**: T015

---

### [X] T020 — ChatPanel + ChatWidget Assembly

**Phase**: 4 · **Priority**: P1 · **Story**: US1, US2, US3 · **Deps**: T017, T018, T019, T016

**Description**:
Assemble `ChatPanel.tsx` (the expanded chat UI), `MessageList.tsx` (scrollable message container), and the top-level `ChatWidget/index.tsx` with open/close toggle. Create the full `styles.module.css` in black-and-white per constitution §VII.

**Files to create**:
- `src/components/ChatWidget/MessageList.tsx`
- `src/components/ChatWidget/ChatPanel.tsx`
- `src/components/ChatWidget/index.tsx`
- `src/components/ChatWidget/styles.module.css`

**`index.tsx`** (top-level toggle):
```tsx
import React, { useState } from 'react';
import ChatPanel from './ChatPanel';
import styles from './styles.module.css';
import { useTextSelection } from './hooks/useTextSelection';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedText, clearSelection] = useTextSelection();

  return (
    <div className={styles.container}>
      {isOpen && (
        <ChatPanel
          onClose={() => setIsOpen(false)}
          selectedText={selectedText}
          onClearSelection={clearSelection}
        />
      )}
      <button
        className={styles.toggleButton}
        onClick={() => setIsOpen(o => !o)}
        aria-label={isOpen ? 'Close chat' : 'Open chat assistant'}
      >
        {isOpen ? '✕' : '💬'}
      </button>
    </div>
  );
}
```

**`styles.module.css`** key rules (black/white, no Docusaurus branding):
```css
.container { position: fixed; bottom: 24px; right: 24px; z-index: 9999; display: flex; flex-direction: column; align-items: flex-end; }
.toggleButton { width: 52px; height: 52px; border-radius: 50%; background: #000; color: #fff; border: none; cursor: pointer; font-size: 22px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); transition: transform 0.15s; }
.toggleButton:hover { transform: scale(1.08); }
.panel { width: 360px; max-height: 520px; background: #fff; border: 1px solid #000; border-radius: 8px; display: flex; flex-direction: column; margin-bottom: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.15); }
.panelHeader { padding: 12px 16px; border-bottom: 1px solid #000; font-weight: 600; font-size: 14px; display: flex; justify-content: space-between; align-items: center; background: #000; color: #fff; border-radius: 8px 8px 0 0; }
.messages { flex: 1; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 12px; }
.bubble { max-width: 90%; padding: 8px 12px; border-radius: 6px; font-size: 14px; line-height: 1.5; }
.user { background: #000; color: #fff; align-self: flex-end; }
.assistant { background: #f5f5f5; color: #000; border: 1px solid #e0e0e0; align-self: flex-start; }
.bubbleRole { font-size: 11px; opacity: 0.6; margin-bottom: 4px; }
.citations { margin-top: 8px; padding-top: 8px; border-top: 1px solid #e0e0e0; font-size: 11px; }
.citationsLabel { font-weight: 600; display: block; margin-bottom: 4px; }
.citation { display: block; color: #555; padding: 1px 0; }
.selectionBadge { margin: 8px 12px 0; padding: 6px 10px; background: #f0f0f0; border-left: 3px solid #000; font-size: 12px; border-radius: 0 4px 4px 0; display: flex; align-items: center; gap: 6px; }
.selectionClear { background: none; border: none; cursor: pointer; color: #999; font-size: 14px; padding: 0; }
.inputBar { padding: 8px 12px; border-top: 1px solid #e0e0e0; display: flex; gap: 8px; }
.textarea { flex: 1; resize: none; border: 1px solid #ccc; border-radius: 4px; padding: 8px; font-size: 13px; font-family: inherit; outline: none; }
.textarea:focus { border-color: #000; }
.sendButton { background: #000; color: #fff; border: none; border-radius: 4px; padding: 0 14px; cursor: pointer; font-size: 18px; }
.sendButton:disabled { background: #ccc; cursor: default; }
@media (max-width: 480px) { .panel { width: calc(100vw - 48px); } }
```

**Acceptance Criteria**:
- [ ] Chat icon visible in bottom-right on any Docusaurus page
- [ ] Clicking icon opens panel; clicking again closes it
- [ ] Panel header shows "Physical AI Assistant" in black background / white text (no Docusaurus blue)
- [ ] Messages render in the panel with correct user (black) / assistant (light grey) bubbles
- [ ] Mobile: panel width does not overflow viewport on 375px screens
- [ ] `npm run typecheck` passes for all widget files

**Deps**: T017, T018, T019, T016

---

### [X] T021 — `src/theme/Root.tsx` — Global Widget Injection

**Phase**: 4 · **Priority**: P1 · **Story**: US1 · **Deps**: T020

**Description**:
Create `src/theme/Root.tsx` — the Docusaurus swizzle entry point that wraps every page with the `ChatWidget`. Uses `useLocation()` from `react-router-dom` to make current pathname available for chapter context.

**Files to create**:
- `src/theme/Root.tsx`

```tsx
import React, { type ReactNode } from 'react';
import { useLocation } from 'react-router-dom';
import ChatWidget from '@site/src/components/ChatWidget';

export default function Root({ children }: { children: ReactNode }): JSX.Element {
  // useLocation available because Docusaurus wraps all content in React Router
  const location = useLocation();
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
```

**Acceptance Criteria**:
- [ ] `npm start` starts without TypeScript errors
- [ ] Chat widget icon is visible on the homepage (`/`)
- [ ] Chat widget icon is visible on any chapter page (`/docs/chapter-01-introduction/`)
- [ ] Chat widget icon is visible on `/docs/intro` and all sub-pages
- [ ] `npm run build` completes without errors (SSR-safe — no `window` access in Root.tsx itself)
- [ ] No Docusaurus default branding is introduced or visible

**Notes**: `ChatWidget` uses `useEffect` for `window.getSelection()` — it's SSR-safe because the effect only runs in the browser. Root.tsx itself is kept minimal.

**Deps**: T020

---

## Phase 5: Testing, Polish & Deployment

**Purpose**: Validate end-to-end flow, configure deployment, and ensure hackathon submission quality.

---

### [X] T022 — End-to-End Smoke Test

**Phase**: 5 · **Priority**: P1 · **Story**: All · **Deps**: T021, T014

**Description**:
Manually verify the complete flow: ingestion → backend running → Docusaurus running → widget visible → general Q&A works → text selection works → citations render. Document test results in `specs/001-rag-chatbot/checklists/e2e-test.md`.

**Files to create**:
- `specs/001-rag-chatbot/checklists/e2e-test.md`

**Test script**:
```markdown
# E2E Smoke Test Checklist

## Setup
- [ ] .env populated with real OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY
- [ ] Ingestion ran: `python backend/scripts/ingest.py` exits 0
- [ ] Backend started: `uvicorn main:app` (from backend/)
- [ ] Frontend started: `npm start` (from repo root)

## General Q&A (US1)
- [ ] Visit http://localhost:3000 → chat icon visible bottom-right
- [ ] Click icon → panel opens with "Physical AI Assistant" header
- [ ] Type "What is ROS 2?" → response streams in, cites Chapter 3
- [ ] Type "What is URDF?" → response streams, cites Chapter 3 or 4
- [ ] Type "What is the capital of France?" → response says topic not covered

## Multi-turn (US3)
- [ ] Ask "What is a ROS 2 node?" → get response
- [ ] Follow up "Can you give an example?" → response references prior context

## Text Selection (US2)
- [ ] Navigate to /docs/chapter-07-nvidia-isaac/
- [ ] Select 30+ chars of text
- [ ] Selection badge appears in widget
- [ ] Ask "What does this mean?" → response scoped to Ch. 7

## Citations (US4)
- [ ] Every assistant response ends with "**Sources:**" section
- [ ] Citations list chapter number and section title
- [ ] No response claims sources that don't exist

## Off-topic (US1 negative)
- [ ] "Who won the 2024 Super Bowl?" → "not covered in textbook content"

## Performance
- [ ] First response token appears within 5 seconds
- [ ] Widget opens within 1 second on page load
```

**Acceptance Criteria**:
- [ ] All checklist items above pass
- [ ] No console errors in browser DevTools
- [ ] Backend logs show no unhandled exceptions during test

**Deps**: T021, T007

---

### [X] T023 — Deployment Configuration

**Phase**: 5 · **Priority**: P2 · **Story**: Infrastructure · **Deps**: T022

**Description**:
Configure Railway deployment for the backend and Vercel/GitHub Pages for the frontend. Update `docusaurus.config.ts` `customFields` with the production backend URL. Add `railway.toml` and GitHub Actions CI workflow.

**Files to create/modify**:
- `backend/railway.toml`
- `.github/workflows/ci.yml`
- `docusaurus.config.ts` — add `customFields.chatApiBase`

**`backend/railway.toml`**:
```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 30
restartPolicyType = "ON_FAILURE"
```

**`.github/workflows/ci.yml`**:
```yaml
name: CI
on: [push, pull_request]
jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r backend/requirements.txt
      - run: cd backend && pytest tests/ -v
  frontend-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm run typecheck
      - run: npm run build
```

**`docusaurus.config.ts`** addition:
```typescript
customFields: {
  chatApiBase: process.env.CHAT_API_BASE ?? 'http://localhost:8000',
},
```

**Acceptance Criteria**:
- [ ] `docker build -t rag-backend ./backend` succeeds
- [ ] `railway up` deploys backend; `GET /health` returns `200` on production URL
- [ ] `npm run build` produces `build/` directory without errors
- [ ] GitHub Actions CI passes on push (backend tests + frontend build)
- [ ] CORS in production: frontend origin added to `BACKEND_CORS_ORIGINS` env var in Railway dashboard

**Deps**: T022

---

## Phase 6: Bonus Hooks (Optional — Hackathon Bonus Points)

**Purpose**: Wire the bonus feature hooks that were scaffolded in the prompt builder and schemas. These connect to future auth/personalization/Urdu features without requiring them to be fully implemented.
**Note**: These tasks are wired and functional — they activate when the bonus features (auth, personalization) pass data to the widget.

---

### [X] T024 — Personalization Hook: User Level Prompt Modifier

**Phase**: 6 (Bonus) · **Priority**: P3 · **Story**: Bonus · **Deps**: T011, T020

**Description**:
Expose `user_level` in the frontend widget — add a toggle in `ChatPanel.tsx` that lets users self-select their background level (Beginner / Intermediate / Advanced). Pass this through `useChat.sendMessage()` to `ChatRequest.user_level`. The PromptBuilder already handles it (T011).

**Files to modify**:
- `src/components/ChatWidget/ChatPanel.tsx` — add level selector
- `src/components/ChatWidget/hooks/useChat.ts` — accept `userLevel` param

**Acceptance Criteria**:
- [ ] Level selector (B/I/A buttons) appears in `ChatPanel` header area
- [ ] Selected level is sent as `user_level` in every subsequent chat request
- [ ] A "Beginner" request includes "analogies and avoid jargon" instruction in the backend prompt (verifiable in backend logs)
- [ ] Default is no level selected (standard prompt)
- [ ] Level preference stored in `localStorage` and restored on next visit

**Deps**: T011, T020

---

### [X] T025 — Urdu Translation Hook: Language Toggle

**Phase**: 6 (Bonus) · **Priority**: P3 · **Story**: Bonus · **Deps**: T011, T020

**Description**:
Add a language toggle button (EN / اردو) to `ChatPanel.tsx`. When Urdu is active, `translate_to: "urdu"` is sent in `ChatRequest`. The PromptBuilder already handles the system prompt injection (T011).

**Files to modify**:
- `src/components/ChatWidget/ChatPanel.tsx` — add language toggle
- `src/components/ChatWidget/hooks/useChat.ts` — accept `translateTo` param

**Acceptance Criteria**:
- [ ] EN/اردو toggle visible in chat panel header
- [ ] When اردو active, `translate_to: "urdu"` sent in request body
- [ ] Assistant responses come back in Urdu with English technical terms
- [ ] Toggle state persists per session (React state, not localStorage)
- [ ] RTL text in Urdu responses renders correctly (CSS `dir="auto"` on bubble content)

**Deps**: T011, T020

---

### [X] T026 — Auth Hook: Neon Postgres Schema + Session Token Field

**Phase**: 6 (Bonus) · **Priority**: P3 · **Story**: Bonus · **Deps**: T001

**Description**:
Create the Neon Postgres schema migration file and the `backend/services/neon_client.py` stub. Wire the optional `session_token` field in the chat endpoint to look up user preferences. This is a passive hook — no UI changes; activates when the Auth bonus feature is implemented.

**Files to create**:
- `backend/services/neon_client.py`
- `backend/migrations/001_initial_schema.sql`

**`backend/migrations/001_initial_schema.sql`**:
```sql
-- Neon Serverless Postgres schema for auth + personalization bonus
CREATE TABLE IF NOT EXISTS users (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email       TEXT UNIQUE NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  sw_level    TEXT CHECK (sw_level IN ('beginner','intermediate','advanced')),
  hw_level    TEXT CHECK (hw_level IN ('beginner','intermediate','advanced'))
);

CREATE TABLE IF NOT EXISTS conversations (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
  session_id  TEXT NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chat_messages (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  role            TEXT NOT NULL,
  content         TEXT NOT NULL,
  citations       JSONB,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

**`backend/services/neon_client.py`** (stub):
```python
"""Neon Postgres client — stub for future auth/personalization integration"""
import os
# To activate: pip install asyncpg
# NEON_DB_URL must be set in .env

async def get_user_level(session_token: str) -> str | None:
    """Returns user's sw_level from DB if session valid. Stub — returns None."""
    return None  # TODO: implement when auth bonus is built

async def log_message(conversation_id: str, role: str, content: str, citations: list) -> None:
    """Log a chat message to Neon Postgres. Stub."""
    pass  # TODO: implement when auth bonus is built
```

**Acceptance Criteria**:
- [ ] `001_initial_schema.sql` runs on a Neon Postgres database without errors
- [ ] `from services.neon_client import get_user_level` imports without error
- [ ] `await get_user_level("any-token")` returns `None` (stub behavior)
- [ ] No runtime errors when `NEON_DB_URL` is unset (stub doesn't connect)

**Deps**: T001

---

## Quick Validation Steps

Run these commands to validate each phase is complete:

```bash
# Phase 1 — Infrastructure
cd backend && uvicorn main:app --reload &
curl http://localhost:8000/health
# Expected: {"status":"ok","qdrant_connected":true,"version":"1.0.0"}

# Phase 2 — Ingestion
python backend/scripts/ingest.py --docs-dir docs/ --repo-root .
# Expected: "✓ Complete: 27 files, N chunks, Xs"

# Phase 3 — Backend RAG
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What is ROS 2?"}' -N
# Expected: stream of SSE data lines ending with citations event

# Phase 4 — Frontend
npm start
# Expected: localhost:3000 opens, chat icon visible bottom-right

# Phase 5 — Tests
cd backend && pytest tests/ -v --cov=. --cov-report=term-missing
# Expected: all tests pass, ≥60% coverage

# Phase 6 — Bonus (optional)
# Verify user_level is sent in request when level selector used
# Verify translate_to=urdu in request when toggle active
```

---

## Task Summary Table

| ID | Phase | Story | Description | Deps | Priority |
|----|-------|-------|-------------|------|----------|
| T001 | 1 | Infra | Backend scaffold, requirements, .env.example, Dockerfile | — | P0 |
| T002 | 1 | Infra | FastAPI app, CORS, rate limit, health endpoint | T001 | P0 |
| T003 | 1 | Infra | Pydantic v2 schemas (ChatRequest, StreamChunk, Citation) | T001 | P0 |
| T004 | 1 | US5 | Qdrant client service (collection, upsert, search) | T001 | P0 |
| T005 | 1 | Infra | OpenAI client service (embed + streaming, Grok switch) | T001 | P0 |
| T006 | 2 | US5 | Markdown chunker (heading-aware, tiktoken) | T001 | P1 |
| T007 | 2 | US5 | Ingestion CLI script (walk, chunk, embed, upsert) | T004,T005,T006 | P1 |
| T008 | 2 | US5 | Admin `/ingest` endpoint | T007,T002 | P2 |
| T009 | 2 | US5 | Ingestion unit tests | T006 | P1 |
| T010 | 3 | US1,US2 | RAG service: retrieve (embed + Qdrant search) | T004,T005 | P1 |
| T011 | 3 | US1,US4 | Prompt builder (system prompt, context, citation extraction) | T003,T010 | P1 |
| T012 | 3 | US1,US4 | `/chat` SSE streaming endpoint | T011,T005,T002 | P1 |
| T013 | 3 | US2 | `/chat/selected` endpoint (text-selection mode) | T012 | P2 |
| T014 | 3 | All | Backend test suite (pytest, mocked, ≥60% coverage) | T012,T013,T009 | P2 |
| T015 | 4 | US1 | TypeScript types + API config | — | P1 |
| T016 | 4 | US2 | `useTextSelection` hook | T015 | P2 |
| T017 | 4 | US1,US3 | `useChat` hook (SSE streaming, multi-turn history) | T015 | P1 |
| T018 | 4 | US1,US4 | `MessageBubble` + `CitationList` components | T015 | P1 |
| T019 | 4 | US1,US2 | `InputBar` + `SelectionBadge` components | T015 | P1 |
| T020 | 4 | US1-3 | `ChatPanel` + `ChatWidget` assembly + black/white CSS | T017,T018,T019,T016 | P1 |
| T021 | 4 | US1 | `src/theme/Root.tsx` global widget injection | T020 | P1 |
| T022 | 5 | All | End-to-end smoke test + E2E checklist | T021,T007 | P1 |
| T023 | 5 | Infra | Deployment: Railway + Vercel/GitHub Pages + CI | T022 | P2 |
| T024 | 6 | Bonus | Personalization hook: user-level UI + API param | T011,T020 | P3 |
| T025 | 6 | Bonus | Urdu hook: language toggle + translate_to param | T011,T020 | P3 |
| T026 | 6 | Bonus | Neon Postgres schema + client stub for auth | T001 | P3 |

**Total tasks**: 26 (20 base + 6 bonus)
**Estimated phases**: 5 base phases, 1 bonus phase
**Hackathon base score coverage**: T001–T023 cover 100% of base RAG requirements
**Bonus point hooks**: T024 (personalization, 50pts), T025 (Urdu, 50pts), T026 (auth prep, 50pts)
