# Data Model: Integrated RAG Chatbot

**Feature**: `001-rag-chatbot`
**Date**: 2026-03-22

---

## Entity Map

```
┌─────────────────┐        ┌────────────────────┐
│   Conversation  │ 1────* │     Message        │
│─────────────────│        │────────────────────│
│ session_id: str │        │ role: "user"|"asst"│
│ created_at: dt  │        │ content: str       │
│ page_context:   │        │ citations: [Cite]  │
│   str|None      │        │ timestamp: dt      │
└─────────────────┘        └────────────────────┘
         │                          │
         │                          │ references
         │                 ┌────────────────────┐
         │                 │    Citation        │
         │                 │────────────────────│
         │                 │ chapter_num: int   │
         │                 │ chapter_title: str │
         │                 │ section_title: str │
         │                 └────────────────────┘

┌─────────────────────────────────────────┐
│            DocumentChunk                │  (Qdrant payload)
│─────────────────────────────────────────│
│ id: UUID5 (deterministic)               │
│ text: str           (raw markdown text) │
│ chapter_num: int    (1–10)              │
│ chapter_title: str  ("NVIDIA Isaac")    │
│ section_title: str  ("Isaac Sim Setup") │
│ source_file: str    (relative path)     │
│ chunk_index: int    (within file)       │
│ token_count: int    (approx)            │
│ vector: float[1536] (embedding)         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         SelectionContext (transient)     │
│─────────────────────────────────────────│
│ text: str           (highlighted text)  │
│ page_url: str       (origin page)       │
│ truncated: bool     (if >1500 chars)    │
└─────────────────────────────────────────┘
```

---

## Qdrant Vector Schema

**Collection**: `physical-ai-book`

```json
{
  "vectors": {
    "size": 1536,
    "distance": "Cosine"
  }
}
```

**Point payload schema**:
```json
{
  "text": "string (chunk raw text)",
  "chapter_num": "integer (1-10, or 0 for intro)",
  "chapter_title": "string",
  "section_title": "string",
  "source_file": "string (relative path, e.g. docs/chapter-07-nvidia-isaac/index.md)",
  "chunk_index": "integer (0-based within source_file)"
}
```

**Payload indices** (for filtered search):
- `chapter_num`: integer (filter retrieval to a specific chapter)
- `source_file`: keyword (filter to exact file for selected-text mode)

---

## Pydantic Request/Response Models (Backend)

### ChatRequest
```python
class Citation(BaseModel):
    chapter_num: int
    chapter_title: str
    section_title: str

class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    question: str                          # max 1000 chars
    history: list[HistoryMessage] = []    # last N turns (frontend manages)
    selected_text: str | None = None       # if text-selection mode
    page_url: str | None = None            # current page for context weighting
    # Bonus hooks (ignored if auth not implemented)
    user_level: Literal["beginner", "intermediate", "advanced"] | None = None
    translate_to: Literal["urdu"] | None = None

class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    mode: Literal["general", "selected"]   # which mode was used
    grounded: bool                         # False if no relevant chunks found
```

### StreamChunk (SSE payload)
```python
class StreamChunk(BaseModel):
    type: Literal["delta", "citations", "done", "error"]
    content: str | None = None            # for delta chunks
    citations: list[Citation] | None = None  # sent with "citations" event
    error: str | None = None              # for error events
```

---

## Frontend State Model (TypeScript)

```typescript
interface Citation {
  chapter_num: number;
  chapter_title: string;
  section_title: string;
}

interface Message {
  id: string;              // nanoid()
  role: 'user' | 'assistant';
  content: string;
  citations: Citation[];
  timestamp: Date;
  isStreaming?: boolean;   // true while response is arriving
}

interface ChatState {
  messages: Message[];
  isOpen: boolean;
  isLoading: boolean;
  selectedText: string;    // captured from window.getSelection()
  error: string | null;
}
```

---

## Neon Postgres Schema (Future — Minimal Stub)

```sql
-- Created but not used in base RAG MVP
-- Reserved for auth/personalization bonus features

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

---

## Chunk ID Derivation

Deterministic UUID5 ensures idempotent ingestion:

```python
import uuid
NAMESPACE = uuid.NAMESPACE_DNS

def make_chunk_id(source_file: str, chunk_index: int) -> str:
    key = f"{source_file}::{chunk_index}"
    return str(uuid.uuid5(NAMESPACE, key))
```

---

## Conversation Context Window Management

| Turn | Tokens (est) |
|------|-------------|
| System prompt | ~200 |
| Last 6 history turns | ~1,200 |
| Top-6 retrieved chunks (800 tokens each) | ~4,800 |
| User question | ~50 |
| **Total context** | **~6,250** |
| gpt-4o-mini limit | 128,000 |
| **Headroom** | **121,750** |

Frontend sends only the last 6 turns of history in the request body. If history grows beyond 12 turns in the widget, the oldest turns are dropped from what's sent (but still shown in the UI).
