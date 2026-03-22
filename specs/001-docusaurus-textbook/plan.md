# Implementation Plan: Physical AI & Humanoid Robotics Textbook

**Branch**: `001-docusaurus-textbook` | **Date**: 2025-01-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-docusaurus-textbook/spec.md`
**Constitution**: `.specify/memory/constitution.md` v1.0.0

---

## Summary

Create a 10-chapter AI-native textbook on Physical AI & Humanoid Robotics using Docusaurus, with a professional black-white UI, hero section, multi-page navigation, and preparation hooks for Phase 2 RAG chatbot integration. Deploy to GitHub Pages for hackathon submission.

---

## Technical Context

**Language/Version**: TypeScript 5.x (Docusaurus), Markdown for content
**Primary Dependencies**: Docusaurus 3.x, React 18, Node.js 18+
**Storage**: N/A (static site, file-based content)
**Testing**: Manual testing, Lighthouse audits, visual QA
**Target Platform**: Web (GitHub Pages), responsive for mobile
**Project Type**: Web application (static site generator)
**Performance Goals**: Page load < 3 seconds, Lighthouse score > 80
**Constraints**: Black-white color scheme only, no Docusaurus branding
**Scale/Scope**: 10 chapters, ~50 section pages, 4 supplementary pages

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Status |
|------|-------------|--------|
| II. Spec-Driven Development | Follow Spec-Kit Plus phases | PASS - Following /sp.specify → /sp.plan → /sp.tasks |
| III. Hackathon Scoring | Base functionality (100pts) prioritized | PASS - Phase 1 focuses on base requirements |
| IV. Course Content | 10 chapters, 4 modules, weeks 1-13 | PASS - All mapped in data-model.md |
| V. Technical Standards | Docusaurus, GitHub Pages | PASS - Using mandated stack |
| VII. UI/UX Requirements | Black-white, no branding, hero section | PASS - Documented in research.md |
| VIII. Security & Deployment | GitHub Pages primary, CI/CD | PASS - GitHub Actions workflow planned |
| X. Quality Gates | Build succeeds, all chapters present | PENDING - Verified at deployment |

**Result**: All gates PASS. Proceed with implementation.

---

## High-Level Plan

### Milestone 1: Project Setup
Initialize Docusaurus project with TypeScript template, configure for GitHub Pages deployment.

### Milestone 2: UI/UX Customization
Remove default Docusaurus branding, apply black-white color scheme, configure typography and animations.

### Milestone 3: Hero Section & Navigation
Create custom homepage with hero section, configure chapter navigation with sidebar.

### Milestone 4: Content Structure
Create 10 chapter folders with proper structure, add supplementary sections (Hardware, Quarter Overview, etc.).

### Milestone 5: Chapter Content
Write substantive content for all 10 chapters with learning outcomes and sections.

### Milestone 6: Chatbot Placeholder
Add floating chat widget placeholder for Phase 2 integration.

### Milestone 7: Deployment
Configure GitHub Actions, deploy to GitHub Pages, validate all success criteria.

---

## Detailed Steps

### Milestone 1: Project Setup

**Objective**: Initialize Docusaurus project ready for customization

| Step | Task | Output |
|------|------|--------|
| 1.1 | Run `npx create-docusaurus@latest physical-ai-textbook classic --typescript` | Project scaffold |
| 1.2 | Remove default blog folder (not needed) | Clean structure |
| 1.3 | Update `docusaurus.config.ts` with project metadata | Configured site |
| 1.4 | Test with `npm start` | Dev server running |

**Acceptance**: Site runs locally at `localhost:3000`

---

### Milestone 2: UI/UX Customization

**Objective**: Apply constitution-mandated styling, remove all default branding

| Step | Task | Output |
|------|------|--------|
| 2.1 | Override CSS variables in `src/css/custom.css` (black #000, white #FFF) | Color scheme applied |
| 2.2 | Remove default footer branding (swizzle if needed) | Clean footer |
| 2.3 | Update navbar configuration (remove default items) | Minimal navbar |
| 2.4 | Add smooth scroll and page transition animations | Subtle animations |
| 2.5 | Set Inter font or system fonts | Typography configured |
| 2.6 | Verify no blue (#2E8555) visible anywhere | No default colors |

**Acceptance**: Site uses only black-white palette, no Docusaurus branding visible

---

### Milestone 3: Hero Section & Navigation

**Objective**: Create visually striking homepage with hero section

| Step | Task | Output |
|------|------|--------|
| 3.1 | Create `src/components/HeroSection/` component | Hero component |
| 3.2 | Create `src/pages/index.tsx` custom homepage | Homepage |
| 3.3 | Add placeholder hero image (`static/img/hero-robot.jpg`) | Hero image |
| 3.4 | Configure chapter links in navbar | Navigation |
| 3.5 | Create `sidebars.ts` with auto-generated structure | Sidebar config |
| 3.6 | Add logo and favicon (`static/img/`) | Branding assets |

**Acceptance**: Homepage displays hero section with image, chapters accessible via nav

---

### Milestone 4: Content Structure

**Objective**: Create folder structure for all 10 chapters and supplementary sections

| Step | Task | Output |
|------|------|--------|
| 4.1 | Create `docs/intro/` folder with supplementary pages | Intro section |
| 4.2 | Create chapter folders: `docs/chapter-01-introduction/` through `docs/chapter-10-conversational-capstone/` | 10 chapter folders |
| 4.3 | Add `_category_.json` to each chapter with proper metadata | Category configs |
| 4.4 | Create `index.md` for each chapter with learning outcomes | Chapter landings |
| 4.5 | Create Hardware Requirements page with all 4 options | Hardware docs |
| 4.6 | Create Quarter Overview with 13-week schedule | Schedule docs |
| 4.7 | Create Why Physical AI Matters page | Intro content |

**Acceptance**: Navigation shows all 10 chapters + intro section, each chapter has landing page

---

### Milestone 5: Chapter Content

**Objective**: Write substantive content for all chapters

| Step | Task | Output |
|------|------|--------|
| 5.1 | Chapter 1: Introduction to Physical AI (3-5 sections) | Ch1 complete |
| 5.2 | Chapter 2: Foundations of Humanoid Robotics (3-5 sections) | Ch2 complete |
| 5.3 | Chapter 3: ROS 2 Basics (4-6 sections) | Ch3 complete |
| 5.4 | Chapter 4: ROS 2 Advanced (4-6 sections) | Ch4 complete |
| 5.5 | Chapter 5: Gazebo Simulation (3-5 sections) | Ch5 complete |
| 5.6 | Chapter 6: Unity Simulation (3-5 sections) | Ch6 complete |
| 5.7 | Chapter 7: NVIDIA Isaac Platform (4-6 sections) | Ch7 complete |
| 5.8 | Chapter 8: Perception and Manipulation (4-6 sections) | Ch8 complete |
| 5.9 | Chapter 9: Humanoid Development (4-6 sections) | Ch9 complete |
| 5.10 | Chapter 10: Conversational Robotics & Capstone (4-5 sections) | Ch10 complete |

**Acceptance**: Each chapter has learning outcomes, overview, and multiple content sections

---

### Milestone 6: Chatbot Placeholder

**Objective**: Add UI placeholder for Phase 2 RAG chatbot

| Step | Task | Output |
|------|------|--------|
| 6.1 | Create `src/components/ChatbotPlaceholder/` component | Placeholder component |
| 6.2 | Add fixed-position styling (bottom-right, z-index) | Positioning CSS |
| 6.3 | Add collapsible behavior (open/close state) | Interactive widget |
| 6.4 | Import component in `src/theme/Root.tsx` or layout wrapper | Global availability |
| 6.5 | Add placeholder message for Phase 2 | User-facing message |

**Acceptance**: Floating chat button visible on all pages, opens placeholder panel

---

### Milestone 7: Deployment

**Objective**: Deploy to GitHub Pages with CI/CD

| Step | Task | Output |
|------|------|--------|
| 7.1 | Create `.github/workflows/deploy.yml` | CI/CD workflow |
| 7.2 | Update `docusaurus.config.ts` with GitHub Pages settings | Deployment config |
| 7.3 | Run `npm run build` locally to verify no errors | Successful build |
| 7.4 | Push to main branch, verify GitHub Actions runs | CI/CD running |
| 7.5 | Enable GitHub Pages in repository settings | Pages enabled |
| 7.6 | Verify site accessible at public URL | Live deployment |
| 7.7 | Run Lighthouse audit, verify score > 80 | Performance validated |
| 7.8 | Complete quality gate checklist | All gates pass |

**Acceptance**: Site live at `https://username.github.io/repo-name/`, all success criteria met

---

## Project Structure

### Documentation (this feature)

```text
specs/001-docusaurus-textbook/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Technical decisions
├── data-model.md        # Content entity definitions
├── quickstart.md        # Developer setup guide
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
/
├── docs/                           # Textbook content (Markdown)
│   ├── intro/                      # Getting Started section
│   │   ├── _category_.json
│   │   ├── index.md
│   │   ├── why-physical-ai.md
│   │   ├── quarter-overview.md
│   │   ├── hardware-requirements.md
│   │   └── assessments.md
│   ├── chapter-01-introduction/    # Chapter 1
│   │   ├── _category_.json
│   │   ├── index.md
│   │   └── [sections].md
│   ├── chapter-02-foundations/     # Chapter 2
│   ├── chapter-03-ros2-basics/     # Chapter 3
│   ├── chapter-04-ros2-advanced/   # Chapter 4
│   ├── chapter-05-gazebo/          # Chapter 5
│   ├── chapter-06-unity/           # Chapter 6
│   ├── chapter-07-nvidia-isaac/    # Chapter 7
│   ├── chapter-08-perception/      # Chapter 8
│   ├── chapter-09-humanoid/        # Chapter 9
│   └── chapter-10-capstone/        # Chapter 10
├── src/
│   ├── components/
│   │   ├── HeroSection/            # Homepage hero
│   │   │   ├── index.tsx
│   │   │   └── styles.module.css
│   │   └── ChatbotPlaceholder/     # Chat widget placeholder
│   │       ├── index.tsx
│   │       └── styles.module.css
│   ├── css/
│   │   └── custom.css              # Theme overrides
│   ├── pages/
│   │   └── index.tsx               # Custom homepage
│   └── theme/
│       └── Root.tsx                # Global wrapper (for chatbot)
├── static/
│   └── img/
│       ├── logo.svg                # Site logo
│       ├── favicon.ico             # Favicon
│       └── hero-robot.jpg          # Hero section image
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions deployment
├── docusaurus.config.ts            # Main configuration
├── sidebars.ts                     # Sidebar configuration
├── package.json                    # Dependencies
└── tsconfig.json                   # TypeScript config
```

**Structure Decision**: Web application (Docusaurus static site) with docs-focused layout. Content in `docs/`, custom components in `src/components/`, styling in `src/css/`.

---

## Risks & Mitigations

### Risk 1: Default Docusaurus Branding Persists

**Probability**: Medium
**Impact**: High (constitution violation, scoring impact)

**Mitigation**:
1. Comprehensive CSS variable override in `custom.css`
2. Swizzle Footer component if CSS insufficient
3. Visual QA checklist for each page
4. Automated check: search for `#2E8555` in build output

---

### Risk 2: Content Not Complete Before Deadline

**Probability**: Medium
**Impact**: High (base scoring requires all chapters)

**Mitigation**:
1. Use Claude Code for accelerated content generation
2. Establish minimum viable content per chapter (overview + 2 sections)
3. Prioritize structure over depth - can enhance later
4. Clear placeholder markers for incomplete sections

---

### Risk 3: Hero Image Sourcing Delays

**Probability**: Low
**Impact**: Medium (affects visual appeal)

**Mitigation**:
1. Use CSS gradient placeholder during development
2. Have backup royalty-free sources: Unsplash, Pexels
3. Final image sourced at least 48 hours before deadline

---

### Risk 4: GitHub Pages Deployment Issues

**Probability**: Low
**Impact**: High (blocks submission)

**Mitigation**:
1. Test deployment early in development
2. Vercel as backup deployment option
3. Document exact config settings in quickstart.md
4. Keep deployment workflow simple (standard Docusaurus pattern)

---

### Risk 5: Performance Below Threshold

**Probability**: Low
**Impact**: Medium (Lighthouse score < 80)

**Mitigation**:
1. Optimize images before adding (WebP format)
2. Lazy load non-critical images
3. Minimize custom JavaScript
4. Run Lighthouse during development, not just at end

---

## Timeline

**Target**: Complete all milestones before hackathon deadline (Nov 30, 2025)

| Milestone | Priority | Dependencies |
|-----------|----------|--------------|
| M1: Project Setup | P0 (blocking) | None |
| M2: UI/UX Customization | P0 (blocking) | M1 |
| M3: Hero Section & Navigation | P1 | M2 |
| M4: Content Structure | P1 | M1 |
| M5: Chapter Content | P1 | M4 |
| M6: Chatbot Placeholder | P2 | M3 |
| M7: Deployment | P0 (blocking) | M2, M3, M4, M5 |

**Parallel Opportunities**:
- M4 (Content Structure) can start after M1, parallel to M2
- M5 (Chapter Content) can proceed incrementally alongside M3, M6
- M6 (Chatbot Placeholder) can be done anytime after M3

---

## Complexity Tracking

No constitution violations requiring justification. Implementation follows standard Docusaurus patterns with minimal custom code.

---

## Next Steps

1. Run `/sp.tasks` to generate ordered implementation tasks
2. Begin Milestone 1: Project Setup
3. Use Claude Code for accelerated chapter content generation

---

## Related Documents

- [spec.md](./spec.md) - Feature specification
- [research.md](./research.md) - Technical decisions
- [data-model.md](./data-model.md) - Content entity definitions
- [quickstart.md](./quickstart.md) - Developer setup guide
- [Constitution](../../.specify/memory/constitution.md) - Binding project rules
