# Research: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-docusaurus-textbook
**Date**: 2025-01-17
**Status**: Complete

---

## Technology Decisions

### 1. Static Site Generator

**Decision**: Docusaurus 3.x (latest stable)

**Rationale**:
- Constitution mandates Docusaurus for static site generation
- Version 3.x provides React 18 support, improved performance, and better TypeScript integration
- Built-in docs/blog structure maps well to textbook chapters
- Swizzling allows complete UI customization (required to remove default branding)

**Alternatives Considered**:
- Next.js: More flexible but requires more setup for documentation-style sites
- GitBook: Less customizable, harder to remove branding
- VitePress: Vue-based, team expertise in React

---

### 2. Styling Approach

**Decision**: Custom CSS with CSS Modules + Docusaurus Theme Overrides

**Rationale**:
- CSS Modules provide scoped styling without additional dependencies
- Docusaurus allows complete theme customization via `src/css/custom.css`
- Swizzling specific components (Navbar, Footer) gives full control
- No need for heavy CSS-in-JS libraries for this scope

**Alternatives Considered**:
- Tailwind CSS: Adds build complexity, not necessary for custom design system
- Styled Components: Runtime overhead, Docusaurus has built-in theming
- Framer Motion: For animations only, CSS transitions sufficient for subtle effects

**Implementation Details**:
```css
/* Color scheme per constitution */
:root {
  --ifm-color-primary: #000000;
  --ifm-background-color: #FFFFFF;
  --ifm-color-secondary: #333333;
  --ifm-font-family-base: 'Inter', system-ui, sans-serif;
}
```

---

### 3. Animation Strategy

**Decision**: CSS Transitions + `scroll-behavior: smooth`

**Rationale**:
- Constitution requires "subtle animations" and "smooth scroll"
- CSS transitions handle fade-ins and hover effects efficiently
- No JavaScript animation library needed for simple effects
- Page transitions handled by Docusaurus client-side routing

**Implementation Details**:
- Page fade-in: `opacity` transition on `.main-wrapper` (200-300ms)
- Hover effects: `opacity: 0.8` or `text-decoration: underline` transitions
- Scroll: `html { scroll-behavior: smooth; }`

**Alternatives Considered**:
- Framer Motion: Overkill for subtle animations, adds bundle size
- GSAP: Enterprise-grade, unnecessary complexity
- AOS (Animate on Scroll): Adds scroll-triggered effects we don't need

---

### 4. Hero Section Implementation

**Decision**: Custom React component with CSS styling

**Rationale**:
- Docusaurus homepage is customizable via `src/pages/index.tsx`
- Full-width hero with centered image and overlaid text
- Responsive breakpoints for mobile/tablet/desktop
- Image optimization via Docusaurus image handling

**Implementation Details**:
```
src/
├── pages/
│   └── index.tsx          # Homepage with HeroSection component
├── components/
│   └── HeroSection/
│       ├── index.tsx      # Hero component
│       └── styles.module.css
```

---

### 5. Content Structure (Docs)

**Decision**: Docusaurus `docs` folder with sidebar categories

**Rationale**:
- Built-in sidebar generation from folder structure
- Each chapter = top-level folder under `docs/`
- Sections = individual `.md` files within chapter folders
- `_category_.json` for chapter metadata (label, position, collapsed state)

**Folder Structure**:
```
docs/
├── intro/                      # Supplementary: Why Physical AI Matters, etc.
├── chapter-01-introduction/    # Chapter 1
│   ├── _category_.json
│   ├── index.md                # Chapter overview + learning outcomes
│   ├── what-is-physical-ai.md
│   ├── embodied-intelligence.md
│   └── ...
├── chapter-02-foundations/     # Chapter 2
│   └── ...
└── ... (chapters 3-10)
```

---

### 6. Branding Removal Strategy

**Decision**: Swizzle and override Navbar, Footer, and theme components

**Rationale**:
- Constitution mandates NO default Docusaurus branding
- Swizzling allows full replacement of components
- Custom Footer with only project-relevant links
- Remove default social links and "Built with Docusaurus" text

**Components to Swizzle**:
1. `@theme/Navbar` - Custom navigation with project title
2. `@theme/Footer` - Minimal footer without Docusaurus branding
3. `@theme/Logo` - Custom favicon and logo (robotics-themed)

**Configuration**:
```js
// docusaurus.config.js
themeConfig: {
  navbar: {
    title: 'Physical AI & Humanoid Robotics',
    logo: { src: 'img/logo.svg' },
    items: [/* chapter links */],
  },
  footer: {
    style: 'dark',
    links: [], // No default social links
    copyright: '', // Remove "Built with Docusaurus"
  },
}
```

---

### 7. Chatbot Placeholder

**Decision**: Fixed-position React component (bottom-right)

**Rationale**:
- Phase 1 only creates UI placeholder per specification
- Fixed positioning ensures visibility across all pages
- Collapsible design prevents content obstruction
- Easy to replace with actual chatbot in Phase 2

**Implementation Details**:
```
src/components/
└── ChatbotPlaceholder/
    ├── index.tsx        # Floating button/container
    └── styles.module.css # Fixed position, z-index
```

---

### 8. Image Strategy

**Decision**: Placeholder images initially, optimized images before deployment

**Rationale**:
- Development can proceed with placeholder images
- Final submission requires royalty-free/stock images
- Docusaurus handles image optimization via `@docusaurus/plugin-ideal-image`
- Lazy loading for chapter images to maintain performance

**Image Sources**:
- Unsplash: Royalty-free robotics/AI images
- Pexels: Additional stock options
- Custom placeholder: Simple SVG or gradient until final images sourced

---

### 9. Deployment Strategy

**Decision**: GitHub Pages via GitHub Actions

**Rationale**:
- Constitution mandates GitHub Pages as primary deployment target
- GitHub Actions provides automated CI/CD on push
- Docusaurus has official GitHub Pages deployment guide
- Free hosting for public repositories

**Workflow**:
```yaml
# .github/workflows/deploy.yml
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build
      - uses: peaceiris/actions-gh-pages@v3
```

---

### 10. Responsive Design

**Decision**: Mobile-first CSS with breakpoint at 768px

**Rationale**:
- Specification requires mobile responsiveness at 768px breakpoint
- Docusaurus has built-in responsive sidebar (collapsible on mobile)
- Hero section needs custom responsive styles
- Content width constraint (800px max) needs implementation

**Breakpoints**:
- Mobile: < 768px (hamburger menu, stacked layout)
- Tablet: 768px - 1024px (sidebar visible, narrower content)
- Desktop: > 1024px (full layout with sticky sidebar)

---

## Risk Mitigations

### Risk 1: Default Docusaurus UI Persists

**Mitigation**:
1. Run Lighthouse audit to detect any remaining blue colors (#2E8555)
2. Search codebase for any `--ifm-color-primary` references not overridden
3. Visual QA checklist for branding elements

### Risk 2: Performance Below Threshold

**Mitigation**:
1. Enable image optimization plugin
2. Lazy load non-critical images
3. Minimize custom JavaScript
4. Run Lighthouse during development

### Risk 3: Content Incomplete Before Deadline

**Mitigation**:
1. Prioritize chapter structure over deep content
2. Use placeholder text (marked clearly) for sections under development
3. Focus on navigation and UI first, then content

---

## Research Complete

All technical decisions resolved. Ready for Phase 1 design artifacts.
