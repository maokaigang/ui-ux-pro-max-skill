# Antigravity Kit

A collection of AI-powered design intelligence tools for building professional UI/UX across multiple platforms and frameworks.

## Overview

Antigravity Kit provides a searchable database of UI styles, color palettes, font pairings, chart types, product recommendations, UX guidelines, and stack-specific best practices. It's designed to work as a skill/workflow for AI coding assistants (Claude, Windsurf, Cursor, etc.).

## Features

- **50+ UI Styles** - Glassmorphism, Claymorphism, Minimalism, Brutalism, Neumorphism, Bento Grid, Dark Mode, and more
- **21 Color Palettes** - Industry-specific palettes for SaaS, E-commerce, Healthcare, Fintech, Beauty, etc.
- **50 Font Pairings** - Curated typography combinations with Google Fonts imports
- **20+ Chart Types** - Recommendations for dashboards and analytics
- **8 Tech Stacks** - React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, HTML+Tailwind
- **UX Guidelines** - Best practices, anti-patterns, and accessibility rules

## Project Structure

```
antigravity-kit/
├── .claude/skills/ui-ux-pro-max/    # Claude Code skill
│   ├── SKILL.md                      # Skill definition
│   ├── scripts/                      # Search tools
│   │   ├── search.py                 # Main search script
│   │   └── core.py                   # Core search logic
│   └── data/                         # Design database
│       ├── styles.csv                # UI styles
│       ├── colors.csv                # Color palettes
│       ├── typography.csv            # Font pairings
│       ├── charts.csv                # Chart types
│       ├── products.csv              # Product recommendations
│       ├── landing.csv               # Landing page structures
│       ├── ux-guidelines.csv         # UX best practices
│       ├── prompts.csv               # AI prompts
│       └── stacks/                   # Stack-specific guidelines
│           ├── html-tailwind.csv
│           ├── react.csv
│           ├── nextjs.csv
│           ├── vue.csv
│           ├── svelte.csv
│           ├── swiftui.csv
│           ├── react-native.csv
│           └── flutter.csv
├── .windsurf/workflows/              # Windsurf workflow
│   └── ui-ux-pro-max.md
├── .agent/workflows/                 # Generic agent workflow
│   └── ui-ux-pro-max/
└── .shared/ui-ux-pro-max/            # Shared data (symlinked)
```

## Prerequisites

- Python 3.x

## Installation

### For Claude Code

The skill is automatically available in `.claude/skills/ui-ux-pro-max/`.

### For Windsurf

Use the workflow via `/ui-ux-pro-max` slash command.

### For Other Agents

Copy the workflow from `.agent/workflows/ui-ux-pro-max/`.

## Usage

### Search Command

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

### Available Domains

| Domain       | Use For                      | Example Keywords               |
| ------------ | ---------------------------- | ------------------------------ |
| `product`    | Product type recommendations | SaaS, e-commerce, portfolio    |
| `style`      | UI styles, colors, effects   | glassmorphism, minimalism      |
| `typography` | Font pairings                | elegant, playful, professional |
| `color`      | Color palettes               | saas, healthcare, beauty       |
| `landing`    | Page structure               | hero, testimonial, pricing     |
| `chart`      | Chart types                  | trend, comparison, funnel      |
| `ux`         | Best practices               | animation, accessibility       |
| `prompt`     | AI prompts                   | (style name)                   |

### Available Stacks

| Stack           | Focus                                    |
| --------------- | ---------------------------------------- |
| `html-tailwind` | Tailwind utilities, responsive (DEFAULT) |
| `react`         | State, hooks, performance                |
| `nextjs`        | SSR, routing, images                     |
| `vue`           | Composition API, Pinia                   |
| `svelte`        | Runes, stores, SvelteKit                 |
| `swiftui`       | Views, State, Navigation                 |
| `react-native`  | Components, Navigation                   |
| `flutter`       | Widgets, State, Layout                   |

### Example Workflow

```bash
# 1. Search product type
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard" --domain product

# 2. Search style
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "glassmorphism dark" --domain style

# 3. Search typography
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "modern professional" --domain typography

# 4. Search color palette
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "saas" --domain color

# 5. Search stack guidelines
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "layout responsive" --stack html-tailwind
```

## License

MIT
