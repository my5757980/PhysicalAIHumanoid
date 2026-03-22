"""Pytest configuration and shared fixtures for the RAG Chatbot test suite."""
import os
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

# Set test environment before importing app
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("QDRANT_URL", "http://localhost:6333")
os.environ.setdefault("QDRANT_API_KEY", "test-qdrant-key")
os.environ.setdefault("ADMIN_SECRET", "test-secret")
os.environ.setdefault("BACKEND_CORS_ORIGINS", "http://localhost:3000")

from main import app  # noqa: E402 — must come after env setup


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client (synchronous)."""
    return TestClient(app, raise_server_exceptions=True)


@pytest.fixture
def mock_rag():
    """
    Mock both retrieve() and stream_chat() to avoid real API calls in tests.
    Returns (mock_retrieve, mock_stream_chat) for assertion in tests.
    """
    with (
        patch("api.routes.chat.retrieve", new_callable=AsyncMock) as mock_retrieve,
        patch("api.routes.chat.stream_chat") as mock_stream,
    ):
        mock_retrieve.return_value = []  # Empty chunks = "not in textbook" response

        async def _fake_stream(messages):
            yield 'data: {"type":"delta","content":"Test answer from textbook."}\n\n'
            yield 'data: {"type":"done"}\n\n'

        mock_stream.side_effect = _fake_stream
        yield mock_retrieve, mock_stream
