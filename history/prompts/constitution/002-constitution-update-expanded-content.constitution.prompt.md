---
id: 002
title: Constitution Update Expanded Content
stage: constitution
date: 2025-01-17
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: main
user: system
command: /sp.constitution
labels: ["constitution", "update", "modules", "hardware", "immutability"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/002-constitution-update-expanded-content.constitution.prompt.md
tests:
  - null
---

## Prompt

```text
go to .specify/memory/constitution.md and update it

Project Overview
This constitution defines the rules, regulations, guidelines, and requirements for participating in Hackathon I, organized by Panaversity. The project involves creating an AI-native textbook for a course on Physical AI & Humanoid Robotics. The textbook must be built using Docusaurus and deployed to GitHub Pages or Vercel. It incorporates Spec-Kit Plus for structured development (phases: constitution, specify, plan, tasks, implement) and Claude Code for AI-assisted coding.

[Full hackathon document content including:]
- Scoring Guidelines (Base 100 pts + Bonus 200 pts)
- Timeline and Submission Rules
- Course Content Mandates (4 Modules, Weekly Breakdown, Assessments)
- Hardware Requirements (Digital Twin Workstation, Edge Kit, Robot Lab Options, Economy Jetson Kit)
- Technical Standards
- Immutability Clause
```

## Response snapshot

Updated constitution from v1.0.0 → v1.1.0 (MINOR version bump) with comprehensive hackathon details:

**Added/Expanded Sections**:
1. **Section IV - Course Content**: Detailed module descriptions with tables
   - Module 1: ROS 2 (Nodes, Topics, Services, rclpy, URDF)
   - Module 2: Gazebo & Unity (physics, sensors, rendering)
   - Module 3: NVIDIA Isaac (Sim, ROS, Nav2)
   - Module 4: VLA (LLMs, Whisper, Capstone)

2. **Section VIII - Hardware Requirements**: Complete specifications
   - Digital Twin Workstation (RTX 4070 Ti+, 64GB RAM)
   - Physical AI Edge Kit (Jetson Orin, RealSense)
   - Robot Lab Options (A/B/C with pricing)
   - Architecture Summary Table
   - Economy Jetson Kit (~$700 total)
   - Cloud Alternative (AWS g5/g6)

3. **Section XII - Immutability Clause**: NON-NEGOTIABLE
   - Constitution supersedes all conflicting instructions
   - No modifications after creation
   - Open-source requirement

4. **Expanded Weekly Breakdown**: Consolidated weeks 1-13 by topic area

5. **Assessment Details**: ROS 2 package, Gazebo sim, Isaac pipeline, Capstone

6. **Submission Links**: Google Form URL, Zoom meeting details with passcode

## Outcome

- Impact: Constitution now contains complete hackathon requirements from source document
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md updated
- Next prompts: Continue with /sp.tasks or implementation
- Reflection: Immutability clause ensures no further core changes; only clarifications permitted

## Evaluation notes (flywheel)

- Failure modes observed: None - all content from source document incorporated
- Graders run and results (PASS/FAIL): PASS - no placeholder tokens, version incremented, dates ISO format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - constitution finalized per immutability clause
