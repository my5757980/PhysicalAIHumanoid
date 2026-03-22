# E2E Test Checklist: RAG Chatbot

**Purpose**: Manual end-to-end validation before demo / deployment
**Feature**: RAG chatbot integrated into Docusaurus Physical AI textbook

---

## 1. Environment Setup

- [ ] `backend/.env` exists with `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`
- [ ] `backend/requirements.txt` dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] Ingestion script ran successfully (`python backend/scripts/ingest.py`)
- [ ] Qdrant collection `physical-ai-book` is populated (check Qdrant Cloud dashboard)
- [ ] Backend starts without error (`uvicorn backend.main:app --reload`)
- [ ] `GET /health` returns `{"status": "ok", "qdrant": "connected"}`
- [ ] Docusaurus dev server starts (`npm start`)

---

## 2. Chat Widget — Appearance

- [ ] Floating toggle button visible in bottom-right corner on every page
- [ ] Button shows 💬 when closed, ✕ when open
- [ ] Panel opens with slide-up animation when toggle is clicked
- [ ] Panel closes when ✕ in header or toggle button is clicked
- [ ] Panel is 380px wide on desktop, full-width on mobile (< 480px)
- [ ] Header shows "Physical AI Assistant" in black bar

---

## 3. General Q&A Mode

- [ ] Typing a question and pressing Enter sends the message
- [ ] Shift+Enter inserts a newline (does NOT send)
- [ ] User message bubble appears immediately (black, right-aligned)
- [ ] Streaming response appears token-by-token (blinking cursor ▌ visible)
- [ ] Response bubble is grey, left-aligned
- [ ] **Sources** section appears at end of assistant response with chapter/section citations
- [ ] Sending a follow-up question preserves conversation history (assistant recalls prior exchange)
- [ ] "Clear" (↺) button resets conversation history

---

## 4. Text Selection Mode

- [ ] Selecting text on a page captures it in the widget badge ("Asking about: …")
- [ ] Badge shows truncated preview (max ~80 chars) of selected text
- [ ] Sending a question while badge is visible sends `selected_text` to `/chat/selected`
- [ ] Response is contextually relevant to the selected passage
- [ ] Clicking ✕ on badge clears the selection context
- [ ] After sending with selected text, badge is cleared automatically

---

## 5. Personalization Bonus (T024)

- [ ] B / I / A buttons in header toggle level (active = white fill)
- [ ] Sending with "B" active produces a beginner-friendly explanation
- [ ] Sending with "A" active produces a more technical explanation
- [ ] Toggling same level off returns to default (no personalization modifier)

---

## 6. Urdu Translation Bonus (T025)

- [ ] EN button in header toggles to اردو (active = white fill)
- [ ] Sending a question with Urdu active returns response in Urdu script
- [ ] Toggling back to EN returns English responses

---

## 7. No Hallucination Enforcement

- [ ] Asking a question clearly outside the textbook scope returns "This topic is not covered in the current textbook content"
- [ ] Response never invents chapter/section references not present in the book
- [ ] All cited sources correspond to real chunks (verify manually against docs/)

---

## 8. Error States

- [ ] If backend is unreachable, error banner appears below message list
- [ ] Error banner is dismissible or clears on next successful send
- [ ] Rate limit (11th request in 1 minute) returns a user-friendly error message
- [ ] Empty question cannot be submitted (send button disabled)

---

## 9. Backend Unit Tests

- [ ] `pytest backend/tests/test_chat.py` — all 14 tests pass
- [ ] `pytest backend/tests/test_ingest.py` — all 8 tests pass
- [ ] `pytest backend/tests/test_rag_service.py` — all 8 tests pass

---

## 10. Deployment Readiness

- [ ] `backend/Dockerfile` builds without error (`docker build ./backend`)
- [ ] `backend/railway.toml` present with correct start command
- [ ] `CORS_ORIGINS` env var set to production frontend URL before deploy
- [ ] `src/components/ChatWidget/config.ts` `PROD_API_URL` points to Railway/Render URL
- [ ] Docusaurus static build succeeds (`npm run build`)
- [ ] No TypeScript errors (`npx tsc --noEmit`)

---

## Overall Status

| Category | Items | Pass | Fail |
|----------|-------|------|------|
| Environment Setup | 7 | | |
| Widget Appearance | 6 | | |
| General Q&A | 8 | | |
| Text Selection | 6 | | |
| Personalization | 4 | | |
| Urdu Translation | 3 | | |
| No Hallucination | 3 | | |
| Error States | 4 | | |
| Backend Tests | 3 | | |
| Deployment | 6 | | |
| **TOTAL** | **50** | | |
