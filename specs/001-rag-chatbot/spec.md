# Feature Specification: Integrated RAG Chatbot

**Feature Branch**: `001-rag-chatbot`
**Created**: 2026-03-22
**Status**: Draft
**Constitution Reference**: `.specify/memory/constitution.md` v1.1.0
**Input**: Add an integrated RAG chatbot to the existing Docusaurus-based Physical AI & Humanoid Robotics textbook.

---

## User Scenarios & Testing *(mandatory)*

<!--
  User stories are prioritized as independent, testable user journeys.
  Each story delivers standalone value even if only it is implemented.
-->

### User Story 1 — Ask the Book a Question (Priority: P1)

A student reading the Physical AI & Humanoid Robotics textbook wants a quick answer without leaving the page. They click the chat widget pinned to the bottom-right corner of any page, type their question (e.g., "What is URDF and why is it used in humanoid robots?"), and receive a concise, sourced answer drawn exclusively from the textbook's chapters — no external knowledge, no hallucinations. The widget stays open as they continue reading.

**Why this priority**: This is the core RAG chatbot function mandated by the hackathon constitution. Without it, all other chatbot features are moot. It directly drives the base-functionality score.

**Independent Test**: Can be fully tested by opening any textbook page, expanding the widget, submitting a question about a topic covered in any chapter, and verifying the response is relevant and cites a specific chapter/section.

**Acceptance Scenarios**:

1. **Given** a user is on any page of the textbook, **When** the page loads, **Then** a chat widget icon is visible in the bottom-right corner.
2. **Given** the widget is visible, **When** the user clicks it, **Then** a chat panel expands showing an input field, send button, and any prior messages from the current session.
3. **Given** the chat panel is open, **When** the user types a question and submits it, **Then** a loading indicator appears while the response is generated.
4. **Given** a question is submitted, **When** the response arrives (within 10 seconds), **Then** the answer is grounded in book content and includes at least one citation in the format "Chapter X — Section Title".
5. **Given** a question is unrelated to the book's content, **When** the system cannot find relevant content, **Then** the chatbot responds with a clear message indicating the topic is not covered in this textbook.
6. **Given** the user collapses the widget, **When** they navigate to a different chapter, **Then** the widget icon remains visible and the session messages are preserved within that browser session.

---

### User Story 2 — Ask About Highlighted Text (Priority: P2)

A reader is studying Chapter 7 (NVIDIA Isaac) and encounters a paragraph they do not fully understand. They select (highlight) the text with their cursor. A prompt appears (or they open the chat widget) asking "What would you like to know about this?" They type their question, and the system answers specifically about the highlighted text, using it as additional context on top of general book retrieval.

**Why this priority**: The hackathon constitution explicitly mandates support for user-selected-text queries alongside general Q&A. It elevates the chatbot from a generic assistant to a context-aware reading companion.

**Independent Test**: Can be fully tested by selecting a paragraph of text on any chapter page, submitting a question about it via the widget, and verifying the answer references the selected passage's topic directly.

**Acceptance Scenarios**:

1. **Given** a user selects text on any chapter page, **When** the selection is made, **Then** the chat widget input is pre-populated with a note indicating the selected text will be used as context (e.g., "Asking about: [first 60 chars of selection]…").
2. **Given** selected text is present as context, **When** the user submits a question, **Then** the response prioritizes retrieval from the chapter/section containing the selected text and directly addresses the selection.
3. **Given** the user clears the selection or navigates away, **When** they ask a new question, **Then** the system reverts to general Q&A mode without the text selection context.
4. **Given** a user selects text and asks a question, **When** the response arrives, **Then** the citation includes the specific section the selected text came from.

---

### User Story 3 — Multi-Turn Conversation (Priority: P3)

A student is exploring ROS 2 topics and asks a series of follow-up questions: "What are ROS 2 nodes?" → "How do topics differ from services?" → "Can you give an example from the book?". The chatbot maintains context across all three messages in the session, providing progressively deeper answers without the student needing to re-explain what they asked previously.

**Why this priority**: Multi-turn context is essential for a learning experience — isolated, one-shot answers force students to constantly repeat themselves and break the flow of understanding.

**Independent Test**: Can be fully tested by sending three related follow-up questions in sequence and verifying the third response correctly builds on the context of the first two without needing repetition.

**Acceptance Scenarios**:

1. **Given** a user has received a response, **When** they ask a follow-up question that references the prior answer (e.g., "Can you expand on that last point?"), **Then** the response correctly interprets the follow-up in context of the prior exchange.
2. **Given** a conversation with at least 5 exchanges, **When** the user asks a question referencing an earlier topic, **Then** the chatbot retrieves the appropriate context and answers coherently.
3. **Given** a user closes and reopens the chat widget within the same browser session, **When** they see the chat history, **Then** prior messages are visible and the next response uses them as context.
4. **Given** a user starts a completely new browser session, **When** they open the chat widget, **Then** the conversation history is empty (sessions do not persist across browser sessions by default).

---

### User Story 4 — Source-Cited Answers (Priority: P4)

After asking "What sensors are used in the Digital Twin simulation?", the student sees the answer followed by a citation: *"Source: Chapter 5 — Gazebo Setup, Section: Sensors (LiDAR, Depth Cameras, IMUs)"*. They click the citation link (or note it) to navigate directly to the relevant section for deeper reading.

**Why this priority**: Citations transform the chatbot from a black box into a trustworthy study tool. They reinforce the book's authoritative role and help students verify and deepen their understanding.

**Independent Test**: Can be fully tested by verifying that every chatbot response includes at least one citation formatted consistently, and that the cited chapter/section exists in the textbook.

**Acceptance Scenarios**:

1. **Given** the chatbot generates a response, **When** the response is based on retrieved content, **Then** it ends with one or more citations listing the chapter number, chapter title, and section title.
2. **Given** a citation is displayed, **When** the user reads it, **Then** the referenced chapter and section accurately correspond to where the cited information appears in the textbook.
3. **Given** the chatbot cannot find relevant content, **When** it responds, **Then** it does NOT fabricate a citation — it explicitly states the information was not found in the textbook.

---

### User Story 5 — Document Ingestion for Retrieval (Priority: P5)

Before the chatbot can function, all textbook chapter content must be indexed. An operator (developer or CI pipeline) runs the ingestion process, which reads all markdown chapter files, splits them into searchable chunks, creates vector embeddings, and stores them in the vector database. After ingestion, any question about the textbook can be retrieved against this index.

**Why this priority**: Without the ingestion pipeline, the chatbot has no content to retrieve. This is a prerequisite for all other stories but is an internal operational step rather than a user-facing story.

**Independent Test**: Can be tested independently by running the ingestion script and verifying the collection contains the expected number of document chunks, then querying one to confirm the content and metadata (chapter, section) are correctly stored.

**Acceptance Scenarios**:

1. **Given** the ingestion script is run, **When** it completes, **Then** all 10 chapters' markdown content is split into chunks, embedded, and stored in the vector database with metadata (chapter number, section title, source file path).
2. **Given** ingestion is complete, **When** an operator queries the vector database for a known topic (e.g., "bipedal locomotion"), **Then** at least one relevant chunk is returned.
3. **Given** the ingestion script runs on already-ingested content, **When** re-run, **Then** existing entries are updated/replaced rather than duplicated.
4. **Given** a chapter file is updated, **When** ingestion is re-run, **Then** the new content replaces the outdated embeddings for that chapter.

---

### Edge Cases

- What happens when the user submits an empty message? → System ignores the submit action and shows a hint to type a question.
- What happens when the backend is unreachable? → Widget shows a friendly error: "The assistant is temporarily unavailable. Please try again in a moment."
- What happens when the selected text is longer than the system's input limit? → System uses the first N characters of the selection with a truncation notice, or prompts the user to select a shorter passage.
- What happens when the user asks the same question twice in the same session? → System answers again using retrieval; it does not cache responses by default.
- What happens when a chapter has very little text (stub content)? → Retrieval returns the available content; the chatbot notes the chapter is still being developed if insufficient content is found.
- What happens when the widget overlaps page elements on mobile? → Widget is collapsible and collapses to a small icon that does not obscure reading content.

---

## Requirements *(mandatory)*

### Functional Requirements

**Chat Widget (Frontend)**

- **FR-001**: The system MUST display a persistent chat widget on every page of the textbook site without requiring page reload or navigation.
- **FR-002**: The widget MUST be expandable and collapsible, defaulting to collapsed (icon-only) state on first visit.
- **FR-003**: The widget MUST render within the textbook's black-and-white color scheme with no default Docusaurus branding.
- **FR-004**: The widget MUST display a message input field, a send button, and a scrollable message history panel when expanded.
- **FR-005**: The widget MUST show a visual loading indicator while awaiting a backend response.
- **FR-006**: The widget MUST detect when a user has selected (highlighted) text on the page and surface that selection as context for the next question.
- **FR-007**: The widget MUST display citations for each response in a consistent, readable format.
- **FR-008**: The widget MUST preserve conversation history within the same browser session across page navigations.

**General Q&A (Backend)**

- **FR-009**: The backend MUST expose an endpoint that accepts a user question and a conversation history, retrieves relevant book content chunks, and returns a grounded answer with citations.
- **FR-010**: The backend MUST NOT generate answers from knowledge outside the indexed textbook content; all responses must be grounded in retrieved chunks.
- **FR-011**: The backend MUST return structured responses including: the answer text, a list of source citations (chapter number, section title), and a confidence indicator when no relevant content is found.

**Text-Selection Q&A (Backend)**

- **FR-012**: The backend MUST expose a separate endpoint (or mode) that accepts a user question, the selected text passage, and conversation history, then prioritizes retrieval from the chapter/section the selected text belongs to.
- **FR-013**: The selected text MUST be used as additional context for the LLM generation step, not merely as a search query.

**Document Ingestion**

- **FR-014**: The system MUST provide an ingestion script that reads all chapter markdown files from the docs directory, chunks them into semantically meaningful segments (paragraphs or heading-bounded sections), and stores each chunk with its metadata (chapter number, section title, file path) in the vector database.
- **FR-015**: The ingestion script MUST be idempotent — running it multiple times on the same content must not create duplicate entries.
- **FR-016**: The ingestion script MUST embed each chunk using a text embedding model and store the embedding alongside the raw text and metadata in the vector collection.

**Conversation Management**

- **FR-017**: The system MUST maintain conversation context across multiple turns within a session (minimum 10 exchanges).
- **FR-018**: Conversation context MUST be scoped to the browser session; it does NOT persist across sessions (persistence is a future enhancement).

### Key Entities

- **Message**: A single exchange unit with a role (user or assistant), content text, timestamp, and any associated citation list.
- **Conversation**: An ordered sequence of Messages within a browser session, identified by a session ID. Carries context for multi-turn retrieval.
- **DocumentChunk**: A segment of textbook content (typically a section or paragraph) with its raw text, chapter number, section title, source file path, and vector embedding.
- **Citation**: A reference to a DocumentChunk that informed a response, containing chapter number, chapter title, and section title.
- **SelectionContext**: The highlighted text passed from the frontend to the backend to scope retrieval and generation to a specific passage.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users receive a relevant, cited answer to a textbook-related question within 10 seconds of submission under normal network conditions.
- **SC-002**: 90% or more of chatbot responses include at least one valid citation referencing an actual chapter and section of the textbook.
- **SC-003**: Users can successfully highlight text on any chapter page and submit a question about it; the response demonstrably addresses the highlighted passage.
- **SC-004**: Multi-turn conversations of up to 10 exchanges maintain coherent context — a follow-up question is answered correctly without the user re-stating prior context.
- **SC-005**: The chat widget is visible and functional on every one of the 10 chapters and all sub-pages of the textbook site.
- **SC-006**: Zero responses are generated from knowledge outside the textbook — when a topic is not covered, the chatbot explicitly states this rather than hallucinating.
- **SC-007**: The chat widget becomes interactive within 2 seconds of any page load.
- **SC-008**: The ingestion pipeline successfully indexes all 10 chapters with correct metadata; a test query for any chapter's key topic returns at least one relevant chunk.
- **SC-009**: The system handles at least 10 concurrent chat sessions without visible degradation in response time.
- **SC-010**: The widget is usable on both desktop and mobile viewports without obscuring primary reading content.

---

## Constraints & Non-Goals

### Constraints (Mandated by Constitution)

- The chatbot backend MUST use FastAPI (Python 3.11+).
- Vector storage MUST use Qdrant Cloud Free Tier exclusively.
- The embedding model MUST be OpenAI `text-embedding-3-small` (or equivalent compatible model).
- The generation model MUST be OpenAI `gpt-4o-mini` (or Grok-compatible via base URL switch).
- Relational data (user metadata, future auth) MUST use Neon Serverless Postgres.
- The frontend widget MUST be a React component integrated into Docusaurus.
- All secrets (API keys, DB credentials) MUST be stored in `.env` files, never hardcoded.
- The chatbot MUST answer ONLY from retrieved textbook content — external knowledge generation is prohibited.

### Non-Goals (Out of Scope for this Feature)

- User authentication and personalized chat history (covered by the separate Authentication bonus feature).
- Urdu translation of chatbot responses (covered by the Urdu Translation bonus feature).
- Content personalization based on user background (covered by the Content Personalization bonus feature).
- Voice input or speech-to-text for chat queries.
- Admin dashboard for monitoring chat usage.
- Moderation or filtering of user messages beyond input validation.

### Assumptions

- All 10 chapter markdown files exist in the `docs/` directory and contain substantive content at the time of ingestion.
- The Docusaurus frontend is already deployed and functional (as per the `001-docusaurus-textbook` feature).
- The operator running ingestion has valid API keys for the embedding model and Qdrant Cloud access configured via `.env`.
- A Qdrant Cloud collection named after this feature (e.g., `textbook-rag`) is pre-created or will be created by the ingestion script.
- Network latency between the Docusaurus frontend, FastAPI backend, Qdrant Cloud, and the LLM API is within typical production ranges (< 500ms each hop).
- The widget must be hooks-compatible for future personalization (Urdu mode, auth-gated features) without a full rewrite.

---

**Prepared for**: `/sp.plan` — Architecture and implementation design phase
**Next Step**: Run `/sp.plan` to define the technical architecture, API contracts, and component design.
