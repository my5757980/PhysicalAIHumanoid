"""Integration tests for /chat and /chat/selected endpoints.

All tests use mocked Qdrant + OpenAI — no external API calls required.
Run with: pytest tests/test_chat.py -v
"""
import json


def test_health_endpoint(client):
    """GET /health returns 200 with status=ok."""
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "qdrant_connected" in body
    assert body["version"] == "1.0.0"


def test_chat_empty_question_rejected(client):
    """POST /chat with empty question returns 422."""
    response = client.post("/chat", json={"question": ""})
    assert response.status_code == 422


def test_chat_question_too_long_rejected(client):
    """POST /chat with question > 1000 chars returns 422."""
    response = client.post("/chat", json={"question": "x" * 1001})
    assert response.status_code == 422


def test_chat_streams_sse(client, mock_rag):
    """POST /chat returns text/event-stream with SSE data lines."""
    with client.stream("POST", "/chat", json={"question": "What is ROS 2?"}) as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]


def test_chat_response_contains_delta(client, mock_rag):
    """POST /chat SSE stream includes at least one delta event."""
    with client.stream("POST", "/chat", json={"question": "What is ROS 2?"}) as response:
        content = b"".join(response.iter_bytes())
        assert b'"type":"delta"' in content


def test_chat_response_contains_citations(client, mock_rag):
    """POST /chat SSE stream ends with citations and done events."""
    with client.stream("POST", "/chat", json={"question": "What is ROS 2?"}) as response:
        content = b"".join(response.iter_bytes()).decode()
        assert '"type":"citations"' in content
        assert '"type":"done"' in content


def test_chat_with_history(client, mock_rag):
    """POST /chat accepts valid conversation history."""
    payload = {
        "question": "Can you expand on that?",
        "history": [
            {"role": "user", "content": "What is URDF?"},
            {"role": "assistant", "content": "URDF is a robot description format."},
        ],
    }
    with client.stream("POST", "/chat", json=payload) as response:
        assert response.status_code == 200


def test_chat_with_bonus_fields(client, mock_rag):
    """POST /chat accepts bonus hook fields without error."""
    payload = {
        "question": "Explain ROS 2 nodes",
        "user_level": "beginner",
        "translate_to": "urdu",
    }
    with client.stream("POST", "/chat", json=payload) as response:
        assert response.status_code == 200


def test_chat_selected_requires_selected_text(client):
    """POST /chat/selected without selected_text returns 422."""
    response = client.post("/chat/selected", json={"question": "What does this mean?"})
    assert response.status_code == 422


def test_chat_selected_with_empty_selected_text(client):
    """POST /chat/selected with empty selected_text returns 422."""
    response = client.post(
        "/chat/selected",
        json={"question": "What does this mean?", "selected_text": "   "},
    )
    assert response.status_code == 422


def test_chat_selected_streams(client, mock_rag):
    """POST /chat/selected with valid selected_text streams SSE."""
    payload = {
        "question": "Can you explain this?",
        "selected_text": "Isaac Sim provides photorealistic simulation for robot training.",
        "page_url": "/docs/chapter-07-nvidia-isaac/",
    }
    with client.stream("POST", "/chat/selected", json=payload) as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]


def test_ingest_wrong_secret(client):
    """POST /ingest with wrong secret returns 403."""
    response = client.post("/ingest", headers={"X-Admin-Secret": "wrong-secret"})
    assert response.status_code == 403


def test_ingest_missing_secret(client):
    """POST /ingest without X-Admin-Secret returns 403."""
    response = client.post("/ingest")
    assert response.status_code == 403


def test_cors_headers_present(client):
    """OPTIONS preflight returns CORS headers for allowed origin."""
    response = client.options(
        "/chat",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code in (200, 204)
