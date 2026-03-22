"""GET /health — liveness and dependency check endpoint."""
import asyncio
import os
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """
    Returns service status and Qdrant connectivity.
    Used by Railway healthcheck and frontend warm-up ping.
    """
    qdrant_ok = False
    try:
        from qdrant_client import QdrantClient

        client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            timeout=3,
        )
        client.get_collections()
        qdrant_ok = True
    except Exception:
        pass

    return {
        "status": "ok",
        "qdrant_connected": qdrant_ok,
        "version": "1.0.0",
    }


async def _test_stream():
    yield "data: hello\n\n"
    await asyncio.sleep(0)
    yield "data: world\n\n"


@router.get("/health/stream-test")
async def stream_test():
    return StreamingResponse(_test_stream(), media_type="text/event-stream")
