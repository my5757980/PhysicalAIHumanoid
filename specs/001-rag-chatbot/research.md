# Phase 0 Research: Integrated RAG Chatbot

**Feature**: `001-rag-chatbot`
**Date**: 2026-03-22

---

> **Research agent confirmation** (2026-03-22): All three background research agents completed and confirmed the decisions below. Key additions from agent findings are noted inline with ▶.

---

## 1. Docusaurus v3 Global Component Injection

**Decision**: Use `src/theme/Root.tsx` (swizzle wrapper pattern)

**Rationale**: Docusaurus v3 treats `src/theme/Root.tsx` as the outermost React wrapper — it wraps every page including docs, homepage, and 404. Creating this file does not require running `docusaurus swizzle` if placed directly; it is auto-detected. This is the canonical approach for injecting persistent UI (modals, banners, chat widgets) without modifying individual page templates.

**Pattern**:
```tsx
// src/theme/Root.tsx
import React from 'react';
import type {WrapperProps} from '@docusaurus/types';
import type RootType from '@theme/Root';
import ChatWidget from '@site/src/components/ChatWidget';

type Props = WrapperProps<typeof RootType>;

export default function Root({children}: Props): JSX.Element {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
```

**Route awareness**: Use `useLocation()` from `react-router-dom` (Docusaurus uses React Router v6 internally) inside `ChatWidget` to read `pathname`
▶ **Agent confirmation**: `src/theme/` directory does NOT yet exist in the project — it must be created. No existing swizzled components. Correct import is `from 'react-router-dom'` not `@docusaurus/router`. and extract the active chapter from the URL (e.g., `/docs/chapter-07-nvidia-isaac/` → chapter 7).

**Alternatives considered**:
- Custom Docusaurus plugin with `injectHtmlTags`: Limited to raw HTML; can't inject React components with state.
- Modifying each chapter page template: Requires swizzling `DocPage` — brittle across Docusaurus upgrades.

---

## 2. Text Selection Capture

**Decision**: `document.addEventListener('selectionchange', ...)` + `window.getSelection().toString()`

**Rationale**: Native browser API, no library needed. Register a single debounced listener in `ChatWidget` via `useEffect`. When selection is non-empty and at least 20 characters, store it in widget state. When the user focuses the chat input, pre-populate with the selection context indicator.

**Pattern**:
```ts
useEffect(() => {
  const handleSelection = () => {
    const selected = window.getSelection()?.toString().trim() ?? '';
    if (selected.length >= 20) setSelectedText(selected);
    else setSelectedText('');
  };
  document.addEventListener('selectionchange', handleSelection);
  return () => document.removeEventListener('selectionchange', handleSelection);
}, []);
```

**Selected text limit**: Truncate to 1500 characters client-side to stay within API payload limits.

---

## 3. Qdrant Collection & Hybrid Search

**Decision**: Dense vector search (cosine) with Qdrant Cloud Free Tier; BM25 sparse optional in Phase 2

**Rationale**: Qdrant Cloud Free Tier supports dense vector search fully. Hybrid search (Sparse + Dense) requires the `sparse_vectors` feature, available in Qdrant v1.7+ and on Free Tier collections via NamedSparseVector. However, BM25 sparse encoding requires `fastembed` library (≥0.2.0). For MVP, dense-only with top-k=6 is sufficient and simpler.

**Collection config**:
- Vector size: `1536` (OpenAI `text-embedding-3-small`)
- Distance: `Cosine`
- Collection name: `physical-ai-book`
- Payload fields: `text`, `chapter_num`, `chapter_title`, `section_title`, `source_file`, `chunk_index`

**Idempotent IDs**: Generate deterministic IDs using either UUID5 (`uuid.uuid5(NAMESPACE_DNS, f"{source_file}::{chunk_index}")`) or SHA-256 int (`int(sha256(key).hexdigest()[:16], 16) % 2**63`). Qdrant accepts both UUID strings and positive integers as point IDs.
▶ **Agent confirmation**: SHA-256 int IDs are slightly more efficient (Qdrant stores them as uint64 natively). UUID5 string IDs also work. Chose UUID5 in data-model.md for readability — either is valid.

**Chunk strategy**:
- Split on `##` and `###` markdown headings (section boundaries)
- Max chunk size: 800 tokens (~600 words), overlap: 100 tokens
- Each chunk retains its heading as prefix for context

**Embedding batching**: OpenAI allows 2048 inputs per batch; batch in groups of 100 for free-tier rate limits.

**Alternatives considered**:
- Pinecone: Paid tier required for production; Qdrant free tier is constitutionally mandated.
- ChromaDB (local): No cloud persistence, not suitable for deployed backend.
- Weaviate: More complex setup; Qdrant is simpler and constitutionally specified.

---

## 4. FastAPI Async RAG Endpoint

**Decision**: Stateless conversation history (passed in request body); Server-Sent Events for streaming

**Rationale**: For a free-tier backend (Railway/Render), storing session state in memory is risky (process restarts). Passing `history` as an array of `{role, content}` objects in the request body is stateless and horizontally scalable. The frontend (React state) holds the conversation history per session — no server-side session store needed for MVP.

**Streaming**: Use `StreamingResponse` with `text/event-stream` content type for real-time token delivery. OpenAI's `stream=True` returns chunks; yield each as `data: {chunk}\n\n`.
▶ **Agent confirmation**: Must add response header `"X-Accel-Buffering": "no"` to disable Nginx/proxy buffering in production (Railway uses Nginx). Without this, tokens batch up and streaming appears broken.

**CORS**: Allow origin matching `https://*.vercel.app` and `https://PHYSICAL-AI-HUMANOID-ROBOTICS.vercel.app`. In development, allow `http://localhost:3000`.

**Rate limiting**: `slowapi` (wraps `limits` library) with `10/minute` per IP. No Redis required — uses in-memory storage (suitable for single-instance free tier).

**Alternatives considered**:
- Server-side session store (Redis): Requires additional infrastructure; not available on free tiers without cost.
- WebSocket: More complex; SSE is simpler for unidirectional streaming.
- LangChain: Heavy dependency; direct OpenAI + Qdrant calls are simpler and more maintainable.

---

## 5. LLM Generation & Citation Enforcement

**Decision**: OpenAI `gpt-4o-mini` with structured system prompt; Grok fallback via `base_url` env var

**System prompt** (enforces grounding + citation):
```
You are a helpful teaching assistant for the Physical AI & Humanoid Robotics textbook.
Answer ONLY using the provided context chunks. Do not use outside knowledge.
After your answer, always add a "Sources:" section listing each chunk used as:
  "Chapter {N} — {chapter_title} › {section_title}"
If the answer is not found in the context, respond with:
  "This topic is not covered in the current textbook content."
Keep answers concise and educational. Maintain conversation continuity using the provided history.
```

**Grok fallback**: Set `OPENAI_BASE_URL=https://api.x.ai/v1` and `OPENAI_API_KEY=xai-...` in `.env`. The OpenAI Python SDK respects `base_url` parameter, enabling a drop-in switch.

**Context window management**: For top-6 chunks at ~800 tokens each = ~4800 context tokens + history (last 6 turns ≈ 1200 tokens) + system prompt (200 tokens) = ~6200 tokens total. Well within `gpt-4o-mini`'s 128k context window.

---

## 6. Ingestion Pipeline

**Decision**: `backend/scripts/ingest.py` — markdown-aware chunking with `python-markdown-it` + heading extraction

**Flow**:
1. Walk `docs/` recursively, collect all `.md` files
2. Parse each file: extract frontmatter (title, sidebar_position) with `python-frontmatter`
3. Split on `##`/`###` headings → section chunks
4. Truncate/overlap chunks exceeding 800 tokens (tiktoken `cl100k_base` for count)
5. Batch embed with `openai.embeddings.create(model="text-embedding-3-small")`
6. Upsert to Qdrant with deterministic UUID5 IDs
7. Log: files processed, chunks created, embeddings generated

**Chapter metadata extraction**:
- From `_category_.json`: `label` (chapter title), `position` (chapter number)
- From file path: `chapter-07-nvidia-isaac` → `chapter_num=7`, `chapter_title="NVIDIA Isaac"`
- From heading: `## Isaac Sim Setup` → `section_title="Isaac Sim Setup"`

---

## 7. Deployment Architecture

**Decision**: Vercel (frontend) + Railway (backend) + Qdrant Cloud Free + Neon Free

**Rationale**: Vercel provides free static hosting with good CDN. Railway offers 500 hours/month free for backend containers. Qdrant Cloud Free Tier: 1GB storage, 1 collection, sufficient for ~50k 1536-dim vectors. Neon Free: 0.5GB Postgres, sufficient for future user metadata.

**CORS origin in production**: `https://PHYSICAL-AI-HUMANOID-ROBOTICS.vercel.app`

**Environment variables required**:
```
OPENAI_API_KEY=sk-...            # or xAI key
OPENAI_BASE_URL=                 # blank for OpenAI, or https://api.x.ai/v1 for Grok
QDRANT_URL=https://xyz.qdrant.io
QDRANT_API_KEY=...
QDRANT_COLLECTION=physical-ai-book
NEON_DB_URL=postgresql://...     # optional for base RAG
BACKEND_CORS_ORIGINS=https://PHYSICAL-AI-HUMANOID-ROBOTICS.vercel.app,http://localhost:3000
```

---

## 8. Bonus Hooks (Future-Proofing)

**Personalization hook**: Add optional `user_context: {level: "beginner|intermediate|advanced"}` field to `ChatRequest`. If present, append to system prompt: `"The user has a {level} background — adjust explanation depth accordingly."` Backend reads from JWT claims or frontend localStorage if auth is implemented later.

**Urdu translation hook**: Add optional `translate_to: "urdu"` field. If present, append to system prompt: `"Translate your answer to Urdu. Keep technical terms (ROS 2, URDF, etc.) in English with Urdu explanation in parentheses."` Can be triggered from the widget language toggle.

**Auth hook**: `ChatRequest` accepts an optional `session_token` field. When present, backend validates against Neon Postgres `users` table and logs conversation to `conversations` table for history persistence across sessions.
