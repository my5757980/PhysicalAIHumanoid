# Implementation Plan: Physical AI & Humanoid Robotics — AI-Native Textbook

**Branch**: `001-physical-ai-textbook` | **Date**: 2025-12-08 | **Spec**: [specs/001-physical-ai-textbook/spec.md]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

A comprehensive AI-native textbook covering Physical AI, Humanoid Robotics, robotics foundations, AI for embodied intelligence, humanoid locomotion, manipulation, and autonomy. The textbook consists of 4 complete chapters with learning objectives, summaries, and real-world examples, formatted as Markdown for Docusaurus documentation system.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Markdown (MDX-compatible)
**Primary Dependencies**: Docusaurus documentation system
**Storage**: Files (Markdown documents)
**Testing**: Content review and validation processes
**Target Platform**: Web-based documentation (Docusaurus)
**Project Type**: Documentation/textbook - determines source structure
**Performance Goals**: Fast loading, accessible content, responsive design
**Constraints**: Educational quality, technical accuracy, student-friendly explanations
**Scale/Scope**: 4 comprehensive chapters, each with 4-6 sections, learning objectives, and summaries

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The textbook content should be technically accurate, pedagogically sound, and accessible to engineering students. Content must align with the Docusaurus documentation system requirements and be suitable for AI-native engineering education.

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Documentation Structure
docs/
├── intro.md
├── chapter-1/
│   ├── index.md
│   ├── what-is-physical-ai.md
│   ├── humanoid-robots.md
│   ├── embodiment-perception-learning-control.md
│   ├── interdisciplinary-foundations.md
│   └── real-world-examples.md
├── chapter-2/
│   ├── index.md
│   ├── kinematics-dynamics-dof.md
│   ├── sensors-actuators.md
│   ├── motor-control-torque-balance.md
│   ├── materials-structural-design.md
│   └── mechatronic-integration.md
├── chapter-3/
│   ├── index.md
│   ├── computer-vision-slam.md
│   ├── reinforcement-learning-control.md
│   ├── imitation-learning-teleoperation.md
│   ├── decision-making-planning.md
│   └── multimodal-models.md
└── chapter-4/
    ├── index.md
    ├── bipedal-walking-stability.md
    ├── grippers-hands-manipulation.md
    ├── whole-body-motion-control.md
    ├── human-robot-interaction-safety.md
    └── autonomous-task-execution.md

# Supporting files
├── docusaurus.config.js
├── package.json
├── src/
│   ├── components/
│   ├── pages/
│   └── css/
└── static/
    ├── img/
    └── diagrams/
```

**Structure Decision**: Documentation structure with 4 main chapters, each containing multiple sections as separate Markdown files for modularity and maintainability in the Docusaurus system.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |



## Objective
Extend the PhysicalAIHumanoid textbook project with a fully integrated RAG chatbot inside the existing Docusaurus site.

## High-Level Plan

### Phase 1 — Backend Architecture
1. Create `backend/` folder inside PhysicalAIHumanoid (if not present).
2. Add:
   - `main.py` (FastAPI server)
   - `ingest_docs.py` (embedding + ingestion)
   - `utils.py` (chunking, embeddings, retrieval)
3. Configure:
   - Qdrant Cloud (collection: youtube-embedding)
   - Cohere embeddings API
   - Neon Postgres (optional logging)
4. Implement endpoints:
   - POST /ask
   - POST /embed
   - GET /health

### Phase 2 — Document Ingestion
1. Read markdown files from `/docs`
2. Chunk them (300–1200 tokens)
3. Add overlap (80–200 tokens)
4. Generate embeddings (Cohere)
5. Insert into Qdrant

### Phase 3 — Frontend Integration
1. Add `src/components/ChatWidget.jsx`
2. Add styling + floating icon
3. Modify `src/theme/Root.js` to load the widget globally
4. Connect frontend to backend `/ask` endpoint
5. Support:
   - text selection → priority RAG mode
   - streaming

### Phase 4 — Testing
1. Validate retrieval accuracy
2. Confirm no hallucinations
3. Confirm every answer cites book chunks


