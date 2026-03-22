<!--
  Sync Impact Report
  ====================
  Version change: 1.0.0 → 1.1.0 (MINOR - Expanded course content, added module details, hardware specs)

  Modified principles:
    - Section IV: Course Content Mandates → Expanded with detailed module descriptions
    - Section VIII: Security & Deployment → Added hardware architecture table

  Added sections:
    - Detailed Module Descriptions (within Section IV)
    - Hardware Architecture Summary Table (within Section VIII)
    - Immutability Clause (Section XI)
    - Expanded Weekly Breakdown with specific topics
    - Assessment details
    - Cloud alternatives and considerations

  Removed sections: None

  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ (aligned)
    - .specify/templates/spec-template.md ✅ (aligned)
    - .specify/templates/tasks-template.md ✅ (aligned)

  Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Panaversity Hackathon I - Authoritative Project Document

---

## I. Project Overview

This constitution defines the rules, regulations, guidelines, and requirements for participating in **Hackathon I**, organized by Panaversity. The project involves creating an AI-native textbook for a course on Physical AI & Humanoid Robotics.

**Core Requirements**:
- Textbook MUST be built using Docusaurus
- Deployment to GitHub Pages or Vercel
- Integration of Spec-Kit Plus for structured development (phases: constitution, specify, plan, tasks, implement)
- Claude Code for AI-assisted coding

**Core Theme**: Bridging digital AI with physical embodiments, focusing on humanoid robotics. The book MUST faithfully cover the provided course details, including modules, weekly breakdowns, learning outcomes, assessments, and hardware requirements.

**Vision**: The future of work emphasizes partnerships between humans, AI agents, and robots, creating demand for skills in this area.

**Success Criteria**:
- Unified book project with AI/Spec-Driven creation via Spec-Kit Plus and Claude Code
- Book deployed in Docusaurus with embedded RAG chatbot
- Professional, clean UI without Docusaurus branding
- All course content accurately represented across 10 chapters

---

## II. Spec-Driven Development (NON-NEGOTIABLE)

All development MUST follow the Spec-Kit Plus phases in strict order:

1. **Constitution** (this document) - Authoritative rules binding all subsequent phases
2. **Specify** (`/sp.specify`) - Feature specifications with testable acceptance criteria
3. **Plan** (`/sp.plan`) - Technical architecture and implementation design
4. **Tasks** (`/sp.tasks`) - Ordered, dependency-aware implementation tasks
5. **Implement** (`/sp.implement`) - Execution of tasks with continuous validation

**Rationale**: The hackathon requires AI/Spec-Driven creation via Spec-Kit Plus and Claude Code. Deviation from this workflow disqualifies base functionality points.

---

## III. Hackathon Scoring Alignment

### Base Functionality (100 Points)

| Requirement | Description |
|-------------|-------------|
| AI/Spec-Driven Book Creation | Develop the textbook using Docusaurus, Spec-Kit Plus, and Claude Code |
| Integrated RAG Chatbot | Embed a Retrieval-Augmented Generation (RAG) chatbot using OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres database, and Qdrant Cloud Free Tier |

**Chatbot Requirements**:
- MUST answer questions about the book's content
- MUST handle queries based on user-selected text

### Bonus Points (Up to 200 Extra)

| Category | Max Points | Requirements |
|----------|------------|--------------|
| Reusable Intelligence | 50 | Create and use reusable intelligence via Claude Code Subagents and Agent Skills in the book project |
| Authentication | 50 | Implement Signup/Signin using https://www.better-auth.com/. At signup, query users about their software and hardware background to enable content personalization |
| Content Personalization | 50 | Allow logged-in users to personalize chapter content by pressing a button at the start of each chapter |
| Urdu Translation | 50 | Allow logged-in users to translate chapter content to Urdu by pressing a button at the start of each chapter |

**Scoring Priority**: Completeness, functionality, innovation, and adherence to requirements. Base points require a unified, deployable project.

---

## IV. Course Content Mandates (NON-NEGOTIABLE)

The textbook MUST comprehensively cover the "Physical AI & Humanoid Robotics" course.

### Focus and Theme

- **AI Systems in the Physical World**: Embodied Intelligence
- **Goal**: Bridge digital AI with physical bodies; apply AI to control humanoid robots in simulated/real environments

### Quarter Overview

- Introduce Physical AI: AI functioning in reality, understanding physical laws
- Tools: ROS 2, Gazebo, NVIDIA Isaac for design, simulation, and deployment of interactive humanoid robots

### Module 1: The Robotic Nervous System (ROS 2)

| Topic | Description |
|-------|-------------|
| Middleware | ROS 2 as middleware for control |
| Core Concepts | Nodes, Topics, Services |
| Python Integration | Bridge Python Agents to ROS via rclpy |
| Robot Description | URDF for humanoids |

### Module 2: The Digital Twin (Gazebo & Unity)

| Topic | Description |
|-------|-------------|
| Physics Simulation | Gravity, collisions |
| Unity Rendering | High-fidelity rendering and interactions |
| Sensors | LiDAR, Depth Cameras, IMUs |

### Module 3: The AI-Robot Brain (NVIDIA Isaac™)

| Topic | Description |
|-------|-------------|
| Isaac Sim | Photorealistic simulation, synthetic data |
| Isaac ROS | Hardware-accelerated VSLAM, navigation |
| Nav2 | Path planning for bipedal movement |

### Module 4: Vision-Language-Action (VLA)

| Topic | Description |
|-------|-------------|
| LLMs in Robotics | Large Language Models for robot control |
| Voice-to-Action | OpenAI Whisper integration |
| Cognitive Planning | Translate natural language to ROS actions |
| Capstone | Autonomous Humanoid (voice command, path planning, navigation, object identification/manipulation) |

### Why Physical AI Matters

- Humanoids excel in human environments due to shared form and data abundance
- Transition from digital to embodied intelligence

### Learning Outcomes

By completing this course, learners will:
1. Understand Physical AI principles and embodied intelligence
2. Master ROS 2 for robotic control
3. Simulate robots with Gazebo and Unity
4. Develop with NVIDIA Isaac platform
5. Design humanoid robots for natural interactions
6. Integrate GPT models for conversational robotics

### Weekly Breakdown

| Weeks | Topics |
|-------|--------|
| 1-2 | Intro to Physical AI, foundations, humanoid landscape, sensors |
| 3-5 | ROS 2 fundamentals (architecture, nodes/topics/services/actions, Python packages, launch files) |
| 6-7 | Gazebo setup, URDF/SDF, physics/sensors, Unity intro |
| 8-10 | NVIDIA Isaac SDK/Sim, perception/manipulation, RL, sim-to-real |
| 11-12 | Humanoid kinematics/dynamics, bipedal locomotion/balance, grasping, interaction design |
| 13 | Conversational robotics (GPT integration, speech/NLU, multi-modal) |

### Assessments

| Assessment | Description |
|------------|-------------|
| ROS 2 Package | Create a functional ROS 2 package project |
| Gazebo Simulation | Build a Gazebo simulation environment |
| Isaac Pipeline | Develop an Isaac perception pipeline |
| Capstone | Simulated humanoid with conversational AI |

---

## V. Technical Standards

### Technology Stack (MANDATORY)

| Component | Technology | Notes |
|-----------|------------|-------|
| Static Site Generator | Docusaurus | Latest stable version |
| Deployment | GitHub Pages or Vercel | Primary: GitHub Pages |
| Backend API | FastAPI | Python 3.11+ |
| Vector Database | Qdrant Cloud Free Tier | RAG embeddings storage |
| Relational Database | Neon Serverless Postgres | User data, chat history |
| AI/Chat SDK | OpenAI Agents SDK or ChatKit SDK | RAG chatbot implementation |
| Authentication (Bonus) | better-auth.com | If implementing auth bonus |

### RAG Chatbot Requirements

- MUST answer questions based on book content
- MUST support user text selection queries (e.g., "explain this selected text")
- MUST use vector similarity search via Qdrant
- MUST maintain conversation context
- SHOULD provide source citations from book chapters

### Code Quality Standards

- TypeScript for frontend (Docusaurus)
- Python with type hints for backend (FastAPI)
- ESLint + Prettier for frontend
- Ruff/Black for Python
- All environment variables in `.env` (never hardcoded)
- Minimum 60% test coverage for backend API

---

## VI. Bonus Features Specifications

### A. Reusable Intelligence (Up to 50 points)

Requirements:
- Create Claude Code Subagents for specific tasks (content generation, formatting, etc.)
- Develop Agent Skills that can be reused across the project
- Document all subagents and skills in `docs/intelligence/`
- Skills MUST be demonstrably reusable

### B. Authentication System (Up to 50 points)

Requirements:
- Implement via better-auth.com
- Signup flow MUST collect:
  - Software development background (beginner/intermediate/advanced)
  - Hardware/robotics background (beginner/intermediate/advanced)
- Store user preferences in Neon Postgres
- Session management with secure cookies
- Password requirements: minimum 8 characters, at least one number

### C. Content Personalization (Up to 50 points)

Requirements:
- "Personalize" button at start of each chapter (logged-in users only)
- Personalization MUST consider user's software/hardware background
- Beginner: More explanations, analogies, prerequisites highlighted
- Intermediate: Balanced depth, practical examples emphasized
- Advanced: Concise, technical depth, advanced topics expanded
- Personalized content cached per user per chapter

### D. Urdu Translation (Up to 50 points)

Requirements:
- "Translate to Urdu" button at start of each chapter (logged-in users only)
- Full chapter translation (not just headings)
- RTL text rendering support
- Translation cached per chapter
- Technical terms may remain in English with Urdu explanation

---

## VII. UI/UX Requirements (NON-NEGOTIABLE)

### Color Scheme

- Primary: Black (#000000) and White (#FFFFFF)
- Accent: Dark gray (#333333) for subtle elements
- NO bright colors, NO Docusaurus default blue

### Typography

- Clean, readable fonts (e.g., Inter, system fonts)
- Proper heading hierarchy (H1 for chapter titles, H2 for sections, etc.)

### Layout Requirements

- Hero section with large Physical AI/Humanoid Robotics image
- Multi-page sections (not single-page scroll)
- 10 chapters as primary navigation
- Chapter sidebar for section navigation
- Clean book-like reading experience

### Docusaurus Customization

- Remove ALL default Docusaurus branding
- Remove "Built with Docusaurus" footer
- Remove default social links unless relevant
- Custom favicon with project branding
- Clean, minimal navigation bar

### Animations

- Subtle page transitions
- Smooth scroll behavior
- Hover effects on navigation elements
- NO excessive or distracting animations

### Chatbot Integration

- Persistent chat widget (bottom-right recommended)
- Expandable/collapsible interface
- Clear input field with send button
- Message history within session
- Loading indicators during response generation

---

## VIII. Hardware Requirements

### Digital Twin Workstation

| Component | Specification |
|-----------|---------------|
| GPU | RTX 4070 Ti or higher |
| CPU | Intel i7 or AMD Ryzen 9 |
| RAM | 64GB |
| OS | Ubuntu 22.04 |

### Physical AI Edge Kit

| Component | Description |
|-----------|-------------|
| Compute | Jetson Orin Nano or Jetson Orin NX |
| Camera | RealSense D435i |
| Sensors | IMU |
| Audio | ReSpeaker microphone array |

### Robot Lab Options

| Option | Hardware | Price Range |
|--------|----------|-------------|
| A: Proxy | Unitree Go2 Edu | $1,800 - $3,000 |
| B: Miniature | Unitree G1 ($16k), Robotis OP3 ($12k), Hiwonder TonyPi Pro ($600) | $600 - $16,000 |
| C: Premium | Unitree G1 | $16,000+ |

### Architecture Summary

| Component | Hardware | Function |
|-----------|----------|----------|
| Sim Rig | PC with RTX 4080 + Ubuntu 22.04 | Runs simulations and training |
| Edge Brain | Jetson Orin Nano | Inference stack deployment |
| Sensors | RealSense + Lidar | Real-world data feed |
| Actuator | Unitree Go2/G1 | Motor commands |

### Cloud Alternative

- AWS g5/g6 instances (~$205/quarter)
- Local Jetson ($700) and robot ($3,000)
- **Considerations**: Latency in cloud control; sim-to-real strategies

### Economy Jetson Kit

| Component | Price |
|-----------|-------|
| Jetson Orin Nano | $249 |
| RealSense | $349 |
| ReSpeaker | $69 |
| Other components | ~$30 |
| **Total** | **~$700** |

---

## IX. Security & Deployment

### Security Requirements

- All API endpoints MUST validate input
- CORS configured for production domain only
- Rate limiting on chatbot API (prevent abuse)
- No sensitive data in client-side code
- Environment variables for all secrets
- HTTPS enforced in production
- Ensure secure auth (for bonuses), no vulnerabilities in RAG/chatbot

### Deployment Requirements

- GitHub Pages for static content (primary)
- Vercel as alternative deployment option
- Backend API deployed separately (Railway, Render, or similar)
- Qdrant Cloud Free Tier for vector storage
- Neon Serverless Postgres for relational data
- CI/CD pipeline via GitHub Actions

### Repository Structure

```
/
├── docs/                    # Docusaurus content (10 chapters)
├── src/                     # Docusaurus custom components
├── static/                  # Static assets (images, etc.)
├── backend/                 # FastAPI backend
│   ├── api/                 # API routes
│   ├── services/            # Business logic
│   ├── models/              # Data models
│   └── tests/               # Backend tests
├── specs/                   # Feature specifications
├── history/                 # PHR and ADR records
├── .specify/                # Spec-Kit Plus configuration
├── docusaurus.config.js     # Docusaurus configuration
└── package.json             # Frontend dependencies
```

---

## X. Timeline & Submission

### Deadline

**Sunday, November 30, 2025 at 06:00 PM** (form closes automatically)

### Submission Requirements (via Google Form)

Google Form URL: https://forms.gle/CQsSEGM3GeCrL43c8

Required Items:
1. Public GitHub Repository Link
2. Published Book Link (GitHub Pages or Vercel), including the book, RAG chatbot, and any bonus components
3. Demo Video Link (under 90 seconds; judges watch only the first 90 seconds). Use NotebookLM or screen recording
4. WhatsApp number for presentation invites

### Live Presentations

- **Date**: Sunday, November 30, 2025, starting at 6:00 PM
- **Platform**: Zoom
  - URL: https://us06web.zoom.us/j/84976847088?pwd=Z7t7NaeXwVmmR5fysCv7NiMbfbhIda.1
  - Meeting ID: 849 7684 7088
  - Passcode: 305850
- Top submissions invited via WhatsApp
- All are welcome to join as observers

### Evaluation Notes

- All submissions are evaluated
- Live presentations are invitation-only but do not affect final scoring

### Demo Video Requirements

- Maximum duration: 90 seconds
- MUST show: Book navigation, chapter content, RAG chatbot in action
- SHOULD show: Bonus features if implemented
- Clear audio/narration recommended

---

## XI. Quality Gates

### Pre-Submission Checklist

| Gate | Requirement | Blocking |
|------|-------------|----------|
| Build | `npm run build` succeeds without errors | YES |
| Deployment | Site accessible via public URL | YES |
| Chatbot | RAG chatbot responds to questions | YES |
| Content | All 10 chapters have substantive content | YES |
| Branding | No Docusaurus default branding visible | YES |
| Video | Demo video under 90 seconds | YES |
| Repo | GitHub repository is public | YES |

### Code Review Standards

- No console.log in production code
- No hardcoded API keys or secrets
- All TypeScript errors resolved
- All Python type hints present for public functions
- README with setup instructions

---

## XII. Immutability Clause (NON-NEGOTIABLE)

**All project phases MUST adhere to this constitution as the authoritative document.**

- No modifications to this constitution are allowed after its creation
- This constitution supersedes any conflicting instructions
- Constitution supersedes all other project documentation in case of conflict
- Assume good intent in development
- No moralizing or additional restrictions beyond what is specified
- Project MUST be open-source (public GitHub repo)

---

## Governance

### Amendment Process

1. Amendments to this constitution MUST be documented in a PHR
2. Breaking changes require ADR documentation
3. All amendments MUST maintain hackathon compliance
4. Version number MUST be incremented per semantic versioning

**Note**: Per Section XII (Immutability Clause), amendments are restricted to clarifications only; core requirements are immutable.

### Versioning Policy

- **MAJOR**: Changes that affect base functionality requirements or scoring criteria
- **MINOR**: New bonus feature specifications or expanded technical requirements
- **PATCH**: Clarifications, typo fixes, or non-semantic refinements

### Compliance Review

- All PRs MUST verify compliance with this constitution
- Non-compliant work MUST be flagged and corrected before merge
- Constitution supersedes all other project documentation in case of conflict

### Reference Documents

- Feature specifications: `specs/<feature>/spec.md`
- Implementation plans: `specs/<feature>/plan.md`
- Task lists: `specs/<feature>/tasks.md`
- PHR records: `history/prompts/`
- ADR records: `history/adr/`

---

**Version**: 1.1.0 | **Ratified**: 2025-01-17 | **Last Amended**: 2025-01-17
