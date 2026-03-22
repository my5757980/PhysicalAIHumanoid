"""POST /chat and POST /chat/selected — SSE streaming RAG endpoints."""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from api.middleware.rate_limit import limiter
from models.schemas import ChatRequest, StreamChunk
from services.rag_service import retrieve
from services.prompt_builder import build_messages, extract_citations
from services.openai_client import stream_chat

router = APIRouter()


async def _rag_stream(req: ChatRequest):
    """
    Core RAG + generation pipeline — shared by /chat and /chat/selected.

    Exceptions inside the stream are caught and emitted as SSE error events
    so the client always receives a well-formed response.
    """
    try:
        # 1. Retrieve top-k chunks from Qdrant
        chunks = await retrieve(
            question=req.question,
            selected_text=req.selected_text,
            page_url=req.page_url,
        )

        # 2. Build prompt with citation-enforcing system message
        messages = build_messages(
            chunks=chunks,
            question=req.question,
            history=req.history,
            selected_text=req.selected_text,
            user_level=req.user_level,
            translate_to=req.translate_to,
        )

        # 3. Stream generation tokens
        async for sse_line in stream_chat(messages):
            yield sse_line

        # 4. Emit citations after stream finishes
        citations = extract_citations(chunks)
        cite_event = StreamChunk(type="citations", citations=citations)
        yield f"data: {cite_event.model_dump_json()}\n\n"

        # 5. Done
        yield f"data: {StreamChunk(type='done').model_dump_json()}\n\n"

    except Exception as exc:
        import traceback
        traceback.print_exc()
        err = StreamChunk(type="error", error=str(exc))
        yield f"data: {err.model_dump_json()}\n\n"


@router.post("/chat")
async def chat(request: Request, body: ChatRequest) -> StreamingResponse:
    """
    General Q&A endpoint — retrieves from full book content.

    Streams SSE events:
      data: {"type":"delta","content":"..."}\n\n
      data: {"type":"citations","citations":[...]}\n\n
      data: {"type":"done"}\n\n
    """
    return StreamingResponse(
        _rag_stream(body),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable Nginx buffering (Railway)
        },
    )


@router.post("/chat/selected")
@limiter.limit("10/minute")
async def chat_selected(request: Request, body: ChatRequest) -> StreamingResponse:
    """
    Text-selection Q&A — retrieval weighted toward the chapter of selected text.
    Requires selected_text to be present and non-empty.
    """
    if not body.selected_text or not body.selected_text.strip():
        raise HTTPException(
            status_code=422,
            detail="selected_text is required and must be non-empty for /chat/selected",
        )
    return StreamingResponse(
        _rag_stream(body),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
