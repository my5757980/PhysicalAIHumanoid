# Data Model: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-docusaurus-textbook
**Date**: 2025-01-17

---

## Overview

This document defines the content entities and their structure for the Docusaurus textbook. Since this is a static site, "data models" represent the Markdown/JSON file structures rather than database schemas.

---

## Entity: Chapter

A major section of the textbook containing multiple sections/pages.

### File Structure
```
docs/chapter-XX-name/
├── _category_.json    # Chapter metadata
├── index.md           # Chapter landing page (overview + learning outcomes)
└── section-name.md    # Individual sections
```

### `_category_.json` Schema
```json
{
  "label": "Chapter X: Title",
  "position": 1,
  "collapsed": false,
  "link": {
    "type": "generated-index",
    "description": "Chapter overview description"
  }
}
```

### Chapter Index (`index.md`) Frontmatter
```yaml
---
sidebar_position: 1
title: "Chapter Title"
description: "Brief chapter description"
---
```

### Chapter Content Structure
```markdown
# Chapter X: Title

## Learning Outcomes

By the end of this chapter, you will be able to:
- Outcome 1
- Outcome 2
- Outcome 3

## Overview

[Chapter introduction paragraph]

## In This Chapter

- [Section 1 Title](./section-1.md)
- [Section 2 Title](./section-2.md)
- ...
```

### Chapter Instances (10 total)

| Position | Folder Name | Label |
|----------|-------------|-------|
| 1 | `chapter-01-introduction` | Introduction to Physical AI and Embodied Intelligence |
| 2 | `chapter-02-foundations` | Foundations of Humanoid Robotics |
| 3 | `chapter-03-ros2-basics` | ROS 2: The Robotic Nervous System |
| 4 | `chapter-04-ros2-advanced` | ROS 2 Advanced: Nodes, Topics, Services, URDF |
| 5 | `chapter-05-gazebo` | Robot Simulation with Gazebo |
| 6 | `chapter-06-unity` | Unity for High-Fidelity Simulation |
| 7 | `chapter-07-nvidia-isaac` | NVIDIA Isaac Platform: SDK and Sim |
| 8 | `chapter-08-perception-manipulation` | AI-Powered Perception and Manipulation |
| 9 | `chapter-09-humanoid-development` | Humanoid Robot Development |
| 10 | `chapter-10-conversational-capstone` | Conversational Robotics and Capstone Project |

---

## Entity: Section

A subpage within a chapter containing specific topic content.

### Section Frontmatter
```yaml
---
sidebar_position: 2
title: "Section Title"
description: "Section description for SEO"
keywords: ["keyword1", "keyword2"]
---
```

### Section Content Structure
```markdown
# Section Title

[Content paragraphs with Markdown formatting]

## Subsection 1

[Content]

### Code Examples (if applicable)
```python
# Example code
```

## Key Takeaways

- Point 1
- Point 2

## Further Reading

- [Resource 1](url)
- [Resource 2](url)
```

### Typical Sections per Chapter

| Chapter | Sections Count | Example Sections |
|---------|----------------|------------------|
| 1 | 5 | What is Physical AI, Embodied Intelligence, History, Current State, Careers |
| 3 | 5 | Why ROS 2, Architecture, Installation, Nodes/Topics, Pub/Sub |
| 7 | 4 | Isaac Overview, Isaac Sim, Isaac SDK, ROS 2 Integration |

---

## Entity: Hardware Option

Configuration for course hardware requirements.

### Location
```
docs/intro/hardware-requirements.md
```

### Content Structure
```markdown
# Hardware Requirements

## Option 1: Digital Twin Workstation

### Specifications
| Component | Requirement |
|-----------|-------------|
| GPU | NVIDIA RTX 3080 or higher |
| RAM | 32GB minimum |
| Storage | 500GB SSD |
| OS | Ubuntu 22.04 LTS |

### Use Cases
- Full Isaac Sim simulation
- Deep learning training
- Multi-robot scenarios

### Cost Tier
**High** - Professional development setup

---

## Option 2: Edge Kit
[Same structure]

## Option 3: Robot Lab Options
[Same structure]

## Option 4: Economy Jetson Kit
[Same structure]
```

### Hardware Option Instances

| Option | Name | Cost Tier |
|--------|------|-----------|
| 1 | Digital Twin Workstation | High |
| 2 | Edge Kit | Medium |
| 3 | Robot Lab Options | High (Physical) |
| 4 | Economy Jetson Kit | Low |

---

## Entity: Weekly Content Mapping

Maps 13-week course schedule to chapter content.

### Location
```
docs/intro/quarter-overview.md
```

### Content Structure
```markdown
# Quarter Overview

## 13-Week Schedule

### Week 1: Introduction & Setup
**Topics**: Course overview, development environment
**Chapter Reference**: [Chapter 1](../chapter-01-introduction/index.md), [Chapter 3](../chapter-03-ros2-basics/index.md)

### Week 2: ROS 2 Fundamentals
**Topics**: Nodes, topics, publisher/subscriber
**Chapter Reference**: [Chapter 3](../chapter-03-ros2-basics/index.md)

[... weeks 3-13]

## Assessment Timeline

| Week | Assessment |
|------|------------|
| 4 | Lab 1: ROS 2 Basics |
| 7 | Lab 2: Simulation |
| 10 | Lab 3: Isaac Platform |
| 13 | Capstone Project |
```

### Week-to-Chapter Mapping

| Week | Primary Chapters | Focus |
|------|------------------|-------|
| 1 | 1, 3 | Intro, Environment Setup |
| 2 | 3 | ROS 2 Pub/Sub |
| 3 | 4 | TF2, URDF, Navigation |
| 4 | 5 | Gazebo Basics |
| 5 | 6 | Unity Integration |
| 6 | 7 | Isaac Sim Intro |
| 7 | 7, 8 | Isaac ROS, Perception |
| 8 | 8 | Isaac Gym, RL |
| 9 | 9 | VLA Foundations |
| 10 | 9 | VLA Training |
| 11 | 9 | Deployment Patterns |
| 12 | 10 | Project Integration |
| 13 | 10 | Final Presentations |

---

## Entity: Supplementary Section

Non-chapter content pages (Why Physical AI Matters, Assessments, etc.)

### Location
```
docs/intro/
├── _category_.json
├── index.md              # "Getting Started" or similar
├── why-physical-ai.md    # Why Physical AI Matters
├── quarter-overview.md   # 13-week schedule
├── hardware-requirements.md
└── assessments.md
```

### `_category_.json`
```json
{
  "label": "Getting Started",
  "position": 0,
  "collapsed": false
}
```

---

## Static Assets

### Location
```
static/
├── img/
│   ├── logo.svg           # Site logo (robotics-themed)
│   ├── favicon.ico        # Browser favicon
│   ├── hero-robot.jpg     # Hero section image
│   └── chapters/          # Chapter-specific images
│       ├── ch01-intro.jpg
│       ├── ch03-ros2.jpg
│       └── ...
└── fonts/                 # Custom fonts (if not using system fonts)
```

### Image Specifications

| Asset | Dimensions | Format | Notes |
|-------|------------|--------|-------|
| Logo | 200x50px | SVG | Scales well, monochrome preferred |
| Favicon | 32x32px | ICO | Multiple sizes in .ico file |
| Hero Image | 1920x800px | JPG/WebP | Responsive, lazy-loaded |
| Chapter Images | 800x400px | JPG/WebP | Optional header images |

---

## Configuration Files

### `docusaurus.config.js` - Key Settings
```javascript
module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'AI-Native Textbook',
  url: 'https://username.github.io',
  baseUrl: '/repo-name/',

  themeConfig: {
    colorMode: {
      defaultMode: 'light',
      disableSwitch: true,  // Force light mode for black/white scheme
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      items: [
        { to: '/docs/intro', label: 'Start Here' },
        { to: '/docs/chapter-01-introduction', label: 'Chapters' },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Physical AI Textbook ${new Date().getFullYear()}`,
    },
  },

  docs: {
    sidebar: {
      hideable: true,
      autoCollapseCategories: true,
    },
  },
};
```

### `sidebars.js` - Auto-generated Structure
```javascript
module.exports = {
  tutorialSidebar: [
    {
      type: 'autogenerated',
      dirName: '.',  // Generate from docs/ folder structure
    },
  ],
};
```

---

## Validation Rules

### Chapter Validation
- Each chapter folder MUST have `_category_.json`
- Each chapter MUST have `index.md` with learning outcomes
- Position values MUST be sequential (0-10 for intro + 10 chapters)

### Section Validation
- All sections MUST have `sidebar_position` frontmatter
- All sections MUST have `title` and `description`
- No orphan sections (every section belongs to a chapter)

### Image Validation
- Hero image MUST exist at `static/img/hero-robot.jpg`
- Logo MUST exist at `static/img/logo.svg`
- Favicon MUST exist at `static/img/favicon.ico`
