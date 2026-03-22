"""Pydantic v2 schemas for RAG Chatbot API.

All request/response shapes for /chat, /chat/selected, /ingest, /health
are defined here. This is the single source of truth for data contracts.
"""
from pydantic import BaseModel, Field
from typing import Literal


class Citation(BaseModel):
    """A source citation referencing a chapter/section of the textbook."""

    chapter_num: int = Field(ge=0, le=10)
    chapter_title: str
    section_title: str


class HistoryMessage(BaseModel):
    """A single turn in a multi-turn conversation."""

    role: Literal["user", "assistant"]
    content: str = Field(max_length=4000)


class ChatRequest(BaseModel):
    """
    Request body for POST /chat and POST /chat/selected.

    Bonus hooks (ignored if not populated):
    - user_level: activates personalization prompt modifier (T024)
    - translate_to: activates Urdu translation (T025)
    """

    question: str = Field(min_length=1, max_length=1000)
    history: list[HistoryMessage] = Field(default=[], max_length=12)
    selected_text: str | None = Field(default=None, max_length=1500)
    page_url: str | None = None

    # ── Bonus hooks (wired in PromptBuilder; activate when populated) ──────────
    # Personalization: "beginner" | "intermediate" | "advanced"
    user_level: Literal["beginner", "intermediate", "advanced"] | None = None
    # Urdu translation: set to "urdu" to get response in Urdu
    translate_to: Literal["urdu"] | None = None
    # Auth hook: session token for future Neon Postgres user lookup (T026)
    session_token: str | None = None


class StreamChunk(BaseModel):
    """
    Single SSE event payload.

    Event lifecycle per request:
      delta* → citations → done
      OR
      error (on failure)
    """

    type: Literal["delta", "citations", "done", "error"]
    content: str | None = None        # Populated for type="delta"
    citations: list[Citation] | None = None  # Populated for type="citations"
    error: str | None = None          # Populated for type="error"


class IngestResponse(BaseModel):
    """Response body for POST /ingest."""

    files_processed: int
    chunks_upserted: int
    duration_seconds: float
