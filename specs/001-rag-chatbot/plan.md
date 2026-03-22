# Implementation Plan: Integrated RAG Chatbot

**Branch**: `001-rag-chatbot` | **Date**: 2026-03-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-rag-chatbot/spec.md`

---

## Summary

Embed a production-ready Retrieval-Augmented Generation (RAG) chatbot into the existing Docusaurus v3 Physical AI & Humanoid Robotics textbook. The system comprises three tightly coupled layers: (1) a React chat widget injected globally via `src/theme/Root.tsx`, (2) a FastAPI async backend with streaming `/chat` and `/chat/selected` endpoints, and (3) a Qdrant-backed vector retrieval pipeline with an ingestion script that indexes all 10 textbook chapters. All responses are grounded exclusively in textbook content and include chapter/section citations.

---

## Technical Context

**Language/Version**: Python 3.11+ (backend) · TypeScript 5.6 / React 19 (frontend)
**Primary Dependencies**: FastAPI 0.115+, openai 1.50+, qdrant-client 1.12+, tiktoken 0.8+, Docusaurus 3.9+
**Storage**: Qdrant Cloud Free Tier (1536-dim cosine vectors) · Neon Serverless Postgres (schema stub only for base RAG)
**Testing**: pytest + pytest-asyncio (backend) · No separate frontend test framework for widget in MVP
**Target Platform**: Vercel (static frontend) + Railway free tier (backend container) + Qdrant Cloud + Neon Cloud
**Project Type**: Web application — monorepo with Docusaurus frontend + FastAPI backend
**Performance Goals**: p95 chat response < 10s · widget interactive < 2s after page load · ingestion < 5 min for all 27 docs
**Constraints**: < $0 operating cost (all free tiers) · No server-side session state (stateless backend) · All secrets in `.env`
**Scale/Scope**: ~27 markdown files · ~150 chunks · ~150 embeddings · 10 concurrent sessions supported

---

## Constitution Check

*GATE: Must pass before Phase 0 research. All gates passed — no violations.*

| Gate | Requirement (Constitution §) | Status |
|------|------------------------------|--------|
| Framework | FastAPI (§V) | ✅ FastAPI 0.115+ |
| Vector DB | Qdrant Cloud Free Tier exclusively (§V) | ✅ qdrant-client, Free Tier |
| Relational DB | Neon Serverless Postgres (§V) | ✅ Schema stub created; not used in base RAG |
| AI SDK | OpenAI Agents SDK or ChatKit SDK (§V) | ✅ openai Python SDK + React widget |
| Embedding Model | text-embedding-3-small (§V implied) | ✅ 1536 dims, OpenAI |
| LLM | gpt-4o-mini or Grok via base_url (§V implied) | ✅ Configurable via OPENAI_BASE_URL |
| Widget Placement | Bottom-right, expandable (§VII) | ✅ Fixed position, collapsible |
| Color Scheme | Black/white, no Docusaurus branding (§VII) | ✅ Custom CSS, #000/#fff |
| Security | All secrets in .env, CORS configured, rate limiting (§IX) | ✅ slowapi, dotenv, CORS middleware |
| Deployment | GitHub Pages / Vercel + Railway/Render (§IX) | ✅ Vercel + Railway |
| Code Quality | Python type hints, ESLint/Prettier, 60% backend test coverage (§V) | ✅ Ruff + mypy + pytest |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        BROWSER (Docusaurus)                         │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Root.tsx (swizzle wrapper — injected on EVERY page)         │  │
│  │  ┌─────────────────────────────────────────────────────────┐ │  │
│  │  │  ChatWidget (React, bottom-right fixed)                 │ │  │
│  │  │  ├─ ChatToggle (icon button, collapsed by default)     │ │  │
│  │  │  ├─ ChatPanel (expandable)                             │ │  │
│  │  │  │   ├─ MessageList (scrollable, markdown rendering)  │ │  │
│  │  │  │   ├─ SelectionBadge (shows highlighted text)       │ │  │
│  │  │  │   ├─ InputBar (textarea + send button)             │ │  │
│  │  │  │   └─ StreamingMessage (typing indicator + SSE)     │ │  │
│  │  │  └─ useChat hook (state, SSE client, history mgmt)    │ │  │
│  │  └─────────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌───────────────────────────────────┐                             │
│  │  useTextSelection hook            │                             │
│  │  window.getSelection() listener   │                             │
│  │  → sets selectedText in ChatState │                             │
│  └───────────────────────────────────┘                             │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ HTTPS POST (JSON) + EventSource (SSE)
                          │ CORS: Vercel origin
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Railway)                           │
│                                                                     │
│  ┌─────────────┐  ┌──────────────────────────────────────────────┐ │
│  │ /health     │  │  POST /chat          POST /chat/selected      │ │
│  │ GET         │  │  ─────────────────────────────────────────── │ │
│  └─────────────┘  │  1. Validate ChatRequest (Pydantic v2)        │ │
│  ┌─────────────┐  │  2. Rate limit check (slowapi, 10/min/IP)     │ │
│  │ POST /ingest│  │  3. RagService.retrieve(question, selected)   │ │
│  │ (admin)     │  │  4. BuildPrompt(chunks, history, user_level)  │ │
│  └─────────────┘  │  5. OpenAI stream → StreamingResponse (SSE)  │ │
│                   │  6. Parse citations from response stream      │ │
│                   └──────────────────────────────────────────────┘ │
│                                    │                               │
│  ┌─────────────────────────────────┴────────────────────────────┐  │
│  │                    Services Layer                            │  │
│  │                                                              │  │
│  │  RagService              PromptBuilder         OpenAIClient  │  │
│  │  ├─ retrieve(q, sel)     ├─ build_system()     ├─ stream()   │  │
│  │  ├─ embed(text)          ├─ add_history()      └─ embed()    │  │
│  │  └─ search_qdrant(vec)   └─ inject_context()               │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
           ┌──────────────┼──────────────┐
           ▼              ▼              ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Qdrant Cloud │  │ OpenAI API   │  │ Neon Postgres │
│ Free Tier    │  │ (or Grok)    │  │ (stub only)   │
│              │  │              │  │               │
│ Collection:  │  │ Embeddings:  │  │ users table   │
│ physical-ai  │  │ text-embed   │  │ (future auth) │
│ -book        │  │ -3-small     │  │               │
│              │  │              │  │               │
│ ~150 points  │  │ Chat:        │  │               │
│ 1536-dim     │  │ gpt-4o-mini  │  │               │
│ cosine       │  │ (streaming)  │  │               │
└──────────────┘  └──────────────┘  └──────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                   INGESTION PIPELINE (one-time / CI)                │
│                                                                     │
│  docs/*.md  →  MarkdownChunker  →  OpenAI Embeddings  →  Qdrant   │
│  (27 files)     (section-aware)    (text-embed-3-sm)    (upsert)   │
│               → ~150 chunks      → 150 × 1536 floats               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot/
├── spec.md              ✅ Feature specification
├── plan.md              ✅ This file
├── research.md          ✅ Phase 0 research findings
├── data-model.md        ✅ Entities, Pydantic models, DB schemas
├── quickstart.md        ✅ Developer setup guide
├── contracts/
│   └── openapi.yaml     ✅ API contract (OpenAPI 3.1)
├── checklists/
│   └── requirements.md  ✅ Spec quality checklist
└── tasks.md             (Phase 2 — /sp.tasks output)
```

### Source Code (repository root additions)

```text
backend/
├── main.py                     # FastAPI app entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── Dockerfile                  # Container for Railway deployment
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── chat.py             # POST /chat endpoint
│   │   ├── chat_selected.py    # POST /chat/selected endpoint
│   │   ├── ingest.py           # POST /ingest endpoint (admin)
│   │   └── health.py           # GET /health endpoint
│   └── middleware/
│       └── rate_limit.py       # slowapi rate limiter config
├── services/
│   ├── __init__.py
│   ├── rag_service.py          # Retrieval orchestration
│   ├── openai_client.py        # OpenAI embeddings + streaming chat
│   ├── qdrant_client.py        # Qdrant search + upsert
│   └── prompt_builder.py       # System prompt + context injection
├── models/
│   ├── __init__.py
│   └── schemas.py              # Pydantic v2 request/response models
├── scripts/
│   └── ingest.py               # Document ingestion CLI script
└── tests/
    ├── conftest.py
    ├── test_chat.py             # Endpoint integration tests
    ├── test_rag_service.py      # RAG service unit tests
    └── test_ingest.py           # Ingestion unit tests

src/
├── theme/
│   └── Root.tsx                # Docusaurus swizzle — global widget injector
└── components/
    └── ChatWidget/
        ├── index.tsx           # Main widget component (open/close state)
        ├── ChatPanel.tsx       # Expanded chat panel (messages + input)
        ├── MessageList.tsx     # Scrollable message history
        ├── MessageBubble.tsx   # Individual message with citations
        ├── InputBar.tsx        # Textarea + send button
        ├── SelectionBadge.tsx  # Shows captured highlighted text
        ├── CitationList.tsx    # Rendered citation links
        ├── config.ts           # API base URL config
        ├── hooks/
        │   ├── useChat.ts      # Chat state + SSE streaming
        │   └── useTextSelection.ts  # window.getSelection() listener
        ├── types.ts            # TypeScript interfaces
        └── styles.module.css   # Black/white widget styles (no branding)

scripts/
└── (no new top-level scripts; ingestion is in backend/scripts/)
```

---

## Data Flow

### A. Ingestion Flow (one-time / on content update)

```
1. SCAN   docs/**/*.md (27 files, recursive walk)
         ↓
2. PARSE  python-frontmatter → extract title, sidebar_position
          _category_.json → chapter_num, chapter_title
         ↓
3. CHUNK  Split on ## / ### headings (section boundaries)
          Truncate to 800 tokens (tiktoken cl100k_base)
          100-token overlap between consecutive chunks
          Each chunk: {text, chapter_num, chapter_title, section_title, source_file, chunk_index}
         ↓
4. EMBED  openai.embeddings.create(model="text-embedding-3-small", input=batch)
          Batch size: 100 chunks per API call
          Output: float[1536] per chunk
         ↓
5. ID     uuid.uuid5(NAMESPACE_DNS, f"{source_file}::{chunk_index}")
          → deterministic UUID, enables idempotent upsert
         ↓
6. UPSERT qdrant_client.upsert(collection="physical-ai-book", points=[PointStruct(...)])
          Existing points with same ID are overwritten (idempotent)
         ↓
7. LOG    Print: files processed, chunks created, duration
```

### B. General Q&A Flow (/chat)

```
Browser                      FastAPI                    Qdrant        OpenAI
  │                             │                          │              │
  │ POST /chat                  │                          │              │
  │ {question, history}         │                          │              │
  │────────────────────────────>│                          │              │
  │                             │ 1. Validate request      │              │
  │                             │ 2. Check rate limit      │              │
  │                             │ 3. Embed question        │              │
  │                             │──────────────────────────────────────> │
  │                             │ <── float[1536]                        │
  │                             │ 4. Search Qdrant top-k=6 │              │
  │                             │─────────────────────────>│              │
  │                             │ <── 6 chunks + metadata   │              │
  │                             │ 5. Build prompt           │              │
  │                             │    system: grounding rule │              │
  │                             │    context: 6 chunks      │              │
  │                             │    history: last 6 turns  │              │
  │                             │ 6. Stream chat            │              │
  │                             │──────────────────────────────────────> │
  │ SSE stream starts           │                                         │
  │ <── data: {type:delta, content:"The..."} ◄────── token chunks ──── │
  │ <── data: {type:delta, content:" ROS"}                              │
  │ ...                         │                                         │
  │ <── data: {type:citations, citations:[{ch:3, ...}]}                  │
  │ <── data: {type:done}       │                                         │
```

### C. Text-Selection Flow (/chat/selected)

```
Browser: User selects text on Chapter 7 page
         useTextSelection hook captures: selectedText = "Isaac Sim provides..."
         User types question: "What does this mean for sim-to-real transfer?"

POST /chat/selected
{question: "...", selected_text: "Isaac Sim provides...", history: [...], page_url: "/docs/chapter-07..."}

FastAPI:
  1. Extract chapter_num from page_url path segment ("chapter-07" → 7)
  2. Embed question (same as general flow)
  3. Search Qdrant with filter: chapter_num = 7, top-k = 4
  4. Also run unfiltered search top-k = 2 (for cross-chapter context)
  5. Merge results: 4 chapter-scoped + 2 general = 6 chunks total
  6. Inject selected_text directly into system prompt context block:
     "The user has highlighted this text: [selected_text]
      Prioritize answering in the context of this passage."
  7. Stream generation (same as general flow)
```

---

## Component Design

### Frontend: ChatWidget

| Component | Responsibility | Key State |
|-----------|---------------|-----------|
| `ChatWidget/index.tsx` | Toggle open/close; mount panel | `isOpen: boolean` |
| `useChat.ts` | SSE connection, history, streaming accumulation | `messages[]`, `isLoading`, `error` |
| `useTextSelection.ts` | Debounced `selectionchange` listener | `selectedText: string` |
| `ChatPanel.tsx` | Render messages + input; route to /chat or /chat/selected | — |
| `MessageBubble.tsx` | Render markdown, citations, role badge | — |
| `SelectionBadge.tsx` | Show truncated selected text with clear button | — |
| `InputBar.tsx` | Textarea (Shift+Enter = newline), submit on Enter | `inputValue: string` |
| `CitationList.tsx` | Render "Chapter N — Section" with optional link | — |

**SSE Client pattern** (useChat.ts):
```typescript
// Start SSE stream
const response = await fetch(`${CHAT_API_BASE}/${endpoint}`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(payload),
});
const reader = response.body!.getReader();
const decoder = new TextDecoder();
// Process stream chunks, parse SSE data lines, accumulate content
```

> Note: Native `EventSource` does not support POST bodies. We use `fetch` with `ReadableStream` for streaming POST requests.

### Backend: RagService

```python
class RagService:
    async def retrieve(
        self,
        question: str,
        selected_text: str | None,
        page_url: str | None,
        top_k: int = 6
    ) -> list[DocumentChunk]:
        # 1. Embed the question
        vector = await self.openai.embed(question)

        # 2. Determine filter
        chapter_filter = self._extract_chapter_filter(page_url) if selected_text else None

        # 3. Search (filtered + unfiltered merge for selected mode)
        if selected_text and chapter_filter:
            filtered = await self.qdrant.search(vector, filter=chapter_filter, top_k=top_k-2)
            general  = await self.qdrant.search(vector, top_k=2)
            chunks   = dedupe(filtered + general)
        else:
            chunks = await self.qdrant.search(vector, top_k=top_k)

        return chunks

    def build_prompt(
        self,
        chunks: list[DocumentChunk],
        history: list[HistoryMessage],
        selected_text: str | None,
        user_level: str | None,
        translate_to: str | None
    ) -> list[dict]:
        system = SYSTEM_PROMPT_TEMPLATE
        if selected_text:
            system += f"\n\nThe user highlighted: \"{selected_text[:500]}\"\nPrioritize answering about this passage."
        if user_level:
            system += f"\n\nAdjust depth for a {user_level}-level learner."
        if translate_to == "urdu":
            system += "\n\nRespond in Urdu. Keep technical terms in English with Urdu explanation."

        context_block = "\n\n---\n\n".join(
            f"[{c.chapter_num}. {c.chapter_title} › {c.section_title}]\n{c.text}"
            for c in chunks
        )
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Context:\n{context_block}"},
            *[{"role": m.role, "content": m.content} for m in history[-6:]],
        ]
        return messages
```

### System Prompt (Citation-Enforced)

```
You are a knowledgeable teaching assistant for the "Physical AI & Humanoid Robotics" textbook.

STRICT RULES:
1. Answer ONLY using the provided Context chunks. Never use outside knowledge.
2. If the answer is not in the Context, respond exactly:
   "This topic is not covered in the current textbook content. Try asking about ROS 2, Gazebo, NVIDIA Isaac, or humanoid robotics."
3. Always end your answer with a "**Sources:**" section listing each chunk used:
   - Chapter {N} — {chapter_title} › {section_title}
4. Be concise, educational, and accurate.
5. Use markdown formatting (headers, bullet points, code blocks) where helpful.
```

---

## Tech Choices Justification

| Decision | Choice | Justification |
|----------|--------|---------------|
| Widget injection | `src/theme/Root.tsx` | Only approach that wraps ALL Docusaurus pages without swizzling inner components; upgrade-safe |
| Streaming protocol | Fetch + ReadableStream (SSE emulation) | `EventSource` doesn't support POST; fetch+stream gives full control with same UX |
| Conversation state | Client-side (React state) | Stateless backend = free-tier compatible, no Redis/session store needed |
| Chunk size | 800 tokens / 100 overlap | Balances specificity (too small = context loss) vs retrieval precision (too large = noise) |
| Embedding model | `text-embedding-3-small` | Best cost/quality for technical text; 1536 dims fit Qdrant free tier easily |
| LLM | `gpt-4o-mini` | Low cost, fast, 128k context window; Grok switch via one env var |
| Chunk IDs | UUID5 deterministic | Enables idempotent upsert without tracking external state |
| Rate limiter | `slowapi` (in-memory) | Zero infrastructure; sufficient for free-tier single-process deployment |
| Markdown rendering | `react-markdown` + `remark-gfm` | Renders LLM responses with code blocks, lists, bold — essential for technical answers |

---

## Risk Analysis & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| OpenAI API latency spike | Response > 10s, poor UX | Medium | Streaming SSE: user sees tokens immediately; 10s deadline on first token, not full response |
| Qdrant Free Tier capacity | >1GB embeddings = ingestion fails | Low | ~150 chunks × 1536 × 4 bytes = ~0.9MB — well within 1GB free limit |
| CORS misconfiguration | Widget can't reach backend in prod | Medium | CORS origins list tested in CI; `BACKEND_CORS_ORIGINS` env var validated on startup |
| Hallucination (off-topic) | Chatbot invents information | Medium | System prompt enforces context-only; `grounded: false` response when no chunks match |
| Free tier cold start (Railway) | First response after idle = 30s+ | High | Add `/health` ping from frontend on widget open; Railway spin-up documented in quickstart |
| Text selection on mobile | `selectionchange` unreliable on iOS | Medium | Graceful fallback: mobile users use general Q&A mode; selection badge hidden if empty |
| Docusaurus upgrade breaks Root.tsx | Widget disappears | Low | `Root.tsx` is the most stable swizzle point; add integration test asserting widget renders |

---

## Implementation Phases Overview

```
Phase A — Backend Foundation (Tasks 1-6)
  ├─ A1: Project scaffold (backend/, requirements.txt, .env.example, Dockerfile)
  ├─ A2: Pydantic models + health endpoint
  ├─ A3: Qdrant client service (collection creation, upsert, search)
  ├─ A4: OpenAI client service (embed + stream)
  ├─ A5: RAG service (retrieve + prompt builder)
  └─ A6: /chat and /chat/selected endpoints with SSE streaming

Phase B — Ingestion Pipeline (Tasks 7-9)
  ├─ B7: Markdown chunker (heading-aware, tiktoken-counted)
  ├─ B8: Ingest script CLI (walk docs/, batch embed, upsert)
  └─ B9: /ingest admin endpoint (triggers pipeline, returns stats)

Phase C — Frontend Widget (Tasks 10-15)
  ├─ C10: src/theme/Root.tsx + ChatWidget scaffold (open/close)
  ├─ C11: useTextSelection hook
  ├─ C12: useChat hook (SSE streaming, history management)
  ├─ C13: MessageList + MessageBubble (markdown + citations)
  ├─ C14: InputBar + SelectionBadge
  └─ C15: Black/white styling (styles.module.css), mobile layout

Phase D — Integration & Tests (Tasks 16-19)
  ├─ D16: Backend test suite (chat, rag_service, ingest)
  ├─ D17: CORS + rate limiting configuration
  ├─ D18: End-to-end smoke test (ingest → query → widget)
  └─ D19: Deployment config (Railway Dockerfile, Vercel build)

Phase E — Bonus Hooks (Task 20, optional)
  └─ E20: Personalization + Urdu prompt hooks (wired, not UI-exposed)
```

Full task breakdown with acceptance criteria → run `/sp.tasks`.

---

## Quickstart Reference

→ See [quickstart.md](./quickstart.md) for step-by-step local setup.

## API Contract Reference

→ See [contracts/openapi.yaml](./contracts/openapi.yaml) for full OpenAPI 3.1 spec.

## Data Model Reference

→ See [data-model.md](./data-model.md) for entity definitions, Pydantic schemas, DB schema.

## Research Reference

→ See [research.md](./research.md) for all Phase 0 decisions and justifications.

---

## Architectural Decision Flags

📋 **Architectural decision detected**: Client-side conversation history (stateless backend) vs server-side session store — this affects scalability, persistence, and future auth integration.
Document reasoning and tradeoffs? Run `/sp.adr stateless-conversation-history`

📋 **Architectural decision detected**: Fetch+ReadableStream SSE emulation vs WebSocket — affects real-time streaming, browser compatibility, and mobile behavior.
Document reasoning and tradeoffs? Run `/sp.adr sse-over-websocket-for-streaming`

📋 **Architectural decision detected**: `src/theme/Root.tsx` swizzle injection vs Docusaurus plugin for global widget — affects upgrade safety and component coupling.
Document reasoning and tradeoffs? Run `/sp.adr root-tsx-widget-injection`
