---
id: 001
title: Hackathon Constitution Creation
stage: constitution
date: 2025-01-17
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: main
user: system
command: /sp.constitution
labels: ["constitution", "hackathon", "physical-ai", "robotics", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-hackathon-constitution-creation.constitution.prompt.md
tests:
  - null
---

## Prompt

```text
strict location
go to .specify/memory/constitution.md

You are an expert in using Spec-Kit Plus to define project constitutions. Create a comprehensive constitution.md file for Hackathon I: Create a Textbook for Teaching Physical AI & Humanoid Robotics Course. This constitution must encapsulate all rules, regulations, requirements, and guidelines from the provided hackathon document.

Key elements to include:
- **Project Overview**: The goal is to create an AI-native textbook on Physical AI & Humanoid Robotics using Docusaurus, deployed to GitHub Pages. Integrate a RAG chatbot using OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud Free Tier. The chatbot must answer questions on book content, including user-selected text.
- **Base Functionality (100 Points)**: Unified book project with AI/Spec-Driven creation via Spec-Kit Plus and Claude Code. Book in Docusaurus with embedded RAG chatbot.
- **Bonus Points**:
  - Up to 50: Create and use reusable intelligence via Claude Code Subagents and Agent Skills.
  - Up to 50: Implement Signup/Signin with better-auth.com, asking users about software/hardware background at signup for content personalization.
  - Up to 50: Logged-in users can personalize chapter content via a button at the start of each chapter.
  - Up to 50: Logged-in users can translate chapter content to Urdu via a button at the start of each chapter.
- **Timeline and Submission**:
  - Deadline: Sunday, Nov 30, 2025 at 06:00 PM.
  - Submit via Google Form: Public GitHub Repo Link, Published Book Link (GitHub Pages or Vercel), Demo Video (under 90 seconds), WhatsApp number.
  - Live Presentations: Invited via WhatsApp, on Zoom (Meeting ID: 849 7684 7088, Passcode: 305850) starting at 6:00 PM on Nov 30, 2025.
- **Course Details Integration**: The book must cover the Physical AI & Humanoid Robotics course exactly as specified, including:
  - Focus: AI Systems in the Physical World, Embodied Intelligence.
  - Modules: 1 (ROS 2), 2 (Gazebo & Unity), 3 (NVIDIA Isaac), 4 (VLA).
  - Weekly Breakdown: Weeks 1-13 as detailed.
  - Learning Outcomes, Assessments, Hardware Requirements (Digital Twin Workstation, Edge Kit, Robot Lab options, Economy Jetson Kit).
  - Why Physical AI Matters, Quarter Overview.
- **Technical Constraints**: Use Spec-Kit Plus phases (constitution, specify, plan, tasks, implement). Book UI/UX must be professional: Black-white color scheme, decent animations, multipage sections, 10 chapters (expanded from modules/weeks), hero section with a big image of Physical AI humanoid robotics. Remove default Docusaurus UI elements for a clean, book-like experience. No mentions of Docusaurus branding in final output.
- **General Rules**: Assume good intent, no moralizing. Ensure project is deployable, secure, and follows best practices. All phases must reference this constitution. Prioritize hackathon scoring for bonuses.

Structure the constitution.md as a Markdown file with sections: Project Rules, Scoring Guidelines, Timeline, Course Content Mandates, Technical Standards, Bonus Features Specs. Make it authoritative and binding for all subsequent phases.
```

## Response snapshot

Created comprehensive constitution at `.specify/memory/constitution.md` (Version 1.0.0) with 10 authoritative sections:

1. **Mission Statement (I)**: AI-native textbook on Physical AI & Humanoid Robotics using Docusaurus + RAG chatbot
2. **Spec-Driven Development (II)**: Mandatory Spec-Kit Plus phases (constitution -> specify -> plan -> tasks -> implement)
3. **Hackathon Scoring Alignment (III)**: Base 100 points + up to 200 bonus points breakdown
4. **Course Content Mandates (IV)**: 4 modules mapped to 10 chapters, Weeks 1-13 breakdown, hardware requirements
5. **Technical Standards (V)**: Technology stack (Docusaurus, FastAPI, Qdrant, Neon Postgres, OpenAI SDKs)
6. **Bonus Features Specifications (VI)**: Detailed requirements for Reusable Intelligence, Auth, Personalization, Urdu Translation
7. **UI/UX Requirements (VII)**: Black-white scheme, no Docusaurus branding, hero section, animations
8. **Security & Deployment (VIII)**: CORS, rate limiting, GitHub Pages/Vercel, CI/CD
9. **Timeline & Submission (IX)**: Nov 30, 2025 deadline, Google Form requirements, Zoom presentation details
10. **Quality Gates (X)**: Pre-submission checklist with blocking requirements

## Outcome

- Impact: Established authoritative project constitution for hackathon compliance
- Tests: N/A (documentation artifact)
- Files: .specify/memory/constitution.md (created), history/prompts/constitution/ (created)
- Next prompts: /sp.specify for feature specifications, /sp.plan for implementation planning
- Reflection: Constitution provides comprehensive binding rules for all subsequent Spec-Kit Plus phases

## Evaluation notes (flywheel)

- Failure modes observed: None - template placeholders fully replaced
- Graders run and results (PASS/FAIL): Manual validation PASS - no unresolved placeholders, version line matches, dates ISO format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - initial constitution creation complete
