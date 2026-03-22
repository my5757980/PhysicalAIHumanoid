# Quickstart: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-docusaurus-textbook
**Date**: 2025-01-17

---

## Prerequisites

- **Node.js**: 18.x or higher ([Download](https://nodejs.org/))
- **npm**: 9.x or higher (comes with Node.js)
- **Git**: Latest version
- **Code Editor**: VS Code recommended

### Verify Installation
```bash
node --version   # Should be v18.x.x or higher
npm --version    # Should be 9.x.x or higher
git --version    # Any recent version
```

---

## Project Setup

### 1. Initialize Docusaurus Project

```bash
# Create new Docusaurus site
npx create-docusaurus@latest physical-ai-textbook classic --typescript

# Navigate to project
cd physical-ai-textbook

# Install dependencies
npm install
```

### 2. Start Development Server

```bash
npm start
```

Visit `http://localhost:3000` to see the default Docusaurus site.

---

## Project Structure (After Setup)

```
physical-ai-textbook/
├── docs/                    # Textbook content (10 chapters)
├── src/
│   ├── components/          # Custom React components
│   │   ├── HeroSection/
│   │   └── ChatbotPlaceholder/
│   ├── css/
│   │   └── custom.css       # Theme overrides
│   └── pages/
│       └── index.tsx        # Custom homepage
├── static/
│   └── img/                 # Images and assets
├── docusaurus.config.ts     # Main configuration
├── sidebars.ts              # Sidebar configuration
└── package.json
```

---

## Key Configuration Files

### `docusaurus.config.ts`

```typescript
import type { Config } from '@docusaurus/types';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'AI-Native Textbook for the Physical AI Course',
  url: 'https://YOUR_USERNAME.github.io',
  baseUrl: '/YOUR_REPO_NAME/',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',

  organizationName: 'YOUR_USERNAME',
  projectName: 'YOUR_REPO_NAME',

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
        },
        blog: false, // Disable blog
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],

  themeConfig: {
    colorMode: {
      defaultMode: 'light',
      disableSwitch: true, // Force light mode
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Textbook',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Physical AI Textbook ${new Date().getFullYear()}`,
      // No links array = no default social links
    },
  },
};

export default config;
```

### `src/css/custom.css`

```css
/* Constitution-mandated color scheme: Black & White only */
:root {
  /* Override Docusaurus defaults */
  --ifm-color-primary: #000000;
  --ifm-color-primary-dark: #000000;
  --ifm-color-primary-darker: #000000;
  --ifm-color-primary-darkest: #000000;
  --ifm-color-primary-light: #333333;
  --ifm-color-primary-lighter: #333333;
  --ifm-color-primary-lightest: #333333;

  --ifm-background-color: #FFFFFF;
  --ifm-font-color-base: #000000;

  /* Typography */
  --ifm-font-family-base: 'Inter', system-ui, -apple-system, sans-serif;
  --ifm-font-size-base: 16px;
  --ifm-line-height-base: 1.6;

  /* Layout */
  --ifm-container-width: 800px;

  /* Remove blue link color */
  --ifm-link-color: #000000;
  --ifm-link-hover-color: #333333;
}

/* Smooth scroll */
html {
  scroll-behavior: smooth;
}

/* Subtle page transitions */
.main-wrapper {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Hover effects for navigation */
.navbar__link:hover {
  opacity: 0.8;
  text-decoration: underline;
}

/* Sidebar styling */
.menu__link:hover {
  background-color: #f5f5f5;
}

/* Content width constraint */
.markdown {
  max-width: 800px;
}

/* Remove default Docusaurus blue from any remaining elements */
.button--primary {
  background-color: #000000;
  border-color: #000000;
}

.button--primary:hover {
  background-color: #333333;
  border-color: #333333;
}
```

---

## Creating Chapter Content

### Step 1: Create Chapter Folder

```bash
mkdir -p docs/chapter-01-introduction
```

### Step 2: Add Category Metadata

Create `docs/chapter-01-introduction/_category_.json`:
```json
{
  "label": "Chapter 1: Introduction to Physical AI",
  "position": 1,
  "collapsed": false
}
```

### Step 3: Create Chapter Index

Create `docs/chapter-01-introduction/index.md`:
```markdown
---
sidebar_position: 1
title: "Introduction to Physical AI and Embodied Intelligence"
description: "Learn the fundamentals of Physical AI and embodied intelligence"
---

# Chapter 1: Introduction to Physical AI and Embodied Intelligence

## Learning Outcomes

By the end of this chapter, you will be able to:
- Define Physical AI and explain its significance
- Describe the concept of embodied intelligence
- Identify key applications of humanoid robotics
- Understand the career landscape in Physical AI

## Overview

Physical AI represents the next frontier of artificial intelligence...

## In This Chapter

- [What is Physical AI?](./what-is-physical-ai.md)
- [Embodied Intelligence Concepts](./embodied-intelligence.md)
- [History and Evolution](./history-evolution.md)
```

### Step 4: Add Section Pages

Create `docs/chapter-01-introduction/what-is-physical-ai.md`:
```markdown
---
sidebar_position: 2
title: "What is Physical AI?"
---

# What is Physical AI?

Physical AI refers to artificial intelligence systems that...

## Key Concepts

...

## Examples in the Real World

...
```

---

## Custom Components

### Hero Section Component

Create `src/components/HeroSection/index.tsx`:
```tsx
import React from 'react';
import styles from './styles.module.css';

export default function HeroSection(): JSX.Element {
  return (
    <section className={styles.hero}>
      <div className={styles.heroContent}>
        <h1>Physical AI & Humanoid Robotics</h1>
        <p>AI-Native Textbook for the Physical AI Course</p>
        <a href="/docs/intro" className={styles.heroButton}>
          Start Learning
        </a>
      </div>
      <div className={styles.heroImage}>
        <img
          src="/img/hero-robot.jpg"
          alt="Humanoid Robot"
          loading="eager"
        />
      </div>
    </section>
  );
}
```

Create `src/components/HeroSection/styles.module.css`:
```css
.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 600px;
  background-color: #000000;
  color: #FFFFFF;
  padding: 2rem;
}

.heroContent {
  max-width: 500px;
  text-align: center;
}

.heroContent h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.heroButton {
  display: inline-block;
  padding: 1rem 2rem;
  background-color: #FFFFFF;
  color: #000000;
  text-decoration: none;
  font-weight: bold;
  margin-top: 1rem;
  transition: opacity 0.2s;
}

.heroButton:hover {
  opacity: 0.9;
}

.heroImage img {
  max-width: 100%;
  height: auto;
}

@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    min-height: auto;
    padding: 3rem 1rem;
  }

  .heroContent h1 {
    font-size: 2rem;
  }
}
```

### Chatbot Placeholder Component

Create `src/components/ChatbotPlaceholder/index.tsx`:
```tsx
import React, { useState } from 'react';
import styles from './styles.module.css';

export default function ChatbotPlaceholder(): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className={styles.chatbotContainer}>
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <span>AI Assistant</span>
            <button onClick={() => setIsOpen(false)}>×</button>
          </div>
          <div className={styles.chatBody}>
            <p>Chatbot coming in Phase 2!</p>
            <p>Ask questions about the textbook content.</p>
          </div>
        </div>
      )}
      <button
        className={styles.chatButton}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chat"
      >
        💬
      </button>
    </div>
  );
}
```

Create `src/components/ChatbotPlaceholder/styles.module.css`:
```css
.chatbotContainer {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chatButton {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #000000;
  color: #FFFFFF;
  border: none;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  transition: transform 0.2s;
}

.chatButton:hover {
  transform: scale(1.05);
}

.chatWindow {
  position: absolute;
  bottom: 70px;
  right: 0;
  width: 300px;
  background-color: #FFFFFF;
  border: 1px solid #333333;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.chatHeader {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: #000000;
  color: #FFFFFF;
}

.chatHeader button {
  background: none;
  border: none;
  color: #FFFFFF;
  font-size: 20px;
  cursor: pointer;
}

.chatBody {
  padding: 20px;
  text-align: center;
  color: #333333;
}
```

---

## Building for Production

```bash
# Build static files
npm run build

# Preview production build locally
npm run serve
```

Build output is in the `build/` directory.

---

## Deploying to GitHub Pages

### 1. Configure GitHub Repository

Update `docusaurus.config.ts`:
```typescript
const config: Config = {
  url: 'https://YOUR_USERNAME.github.io',
  baseUrl: '/YOUR_REPO_NAME/',
  organizationName: 'YOUR_USERNAME',
  projectName: 'YOUR_REPO_NAME',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,
  // ...
};
```

### 2. Create GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: npm

      - name: Install dependencies
        run: npm ci
      - name: Build website
        run: npm run build

      - name: Upload Build Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 3. Enable GitHub Pages

1. Go to repository Settings > Pages
2. Set Source to "GitHub Actions"
3. Push to `main` branch to trigger deployment

---

## Validation Checklist

Before submitting, verify:

- [ ] All 10 chapters have content
- [ ] Hero section displays correctly
- [ ] No Docusaurus default branding visible
- [ ] Black-white color scheme enforced
- [ ] Navigation works on mobile
- [ ] Chatbot placeholder appears in bottom-right
- [ ] `npm run build` completes without errors
- [ ] Site is accessible via GitHub Pages URL
