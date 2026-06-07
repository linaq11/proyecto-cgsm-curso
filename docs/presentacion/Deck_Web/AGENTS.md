<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

## Stack

Next.js 16 (App Router, `src/`), React 19, Tailwind v4 (`@tailwindcss/postcss`),
shadcn 4 (preset nova, baseColor neutral, CSS variables), motion (NOT framer-motion).
Reusable starter for dashboards and web presentations.

## Cult UI registry

Cult UI is wired as a shadcn registry in `components.json`:
`"@cult-ui": "https://cult-ui.com/r/{name}.json"`. Add components with:

    npx shadcn@latest add "@cult-ui/<component>"

If that ever fails with "registry not found", fall back to the direct URL:
`npx shadcn@latest add https://cult-ui.com/r/<component>.json`.

Some Cult UI components require extra keyframes/utilities in `src/app/globals.css`
(Tailwind v4 `@utility` syntax). Read the docstring at the top of the generated
`.tsx`; if it says "Requires these keyframes...", add them to `globals.css`.

## Project skills (`.claude/skills/`)

This repo ships two Cult UI skills. They load only when the Claude Code session
starts with this folder as its working directory (CLI launched here, or a Desktop
Code tab opened on this folder). A session started from another directory will not
have them.

- `components-build`: spec for building composable, accessible React components.
  16 rules live in `.claude/skills/components-build/rules/`. Auto-applies when
  asked to build, review, or refactor components. Follow it for all component
  work in this repo. To force it: "use the components-build skill".
- `fixing-motion-performance`: animation performance auditor. Invoke with the
  slash command `/fixing-motion-performance [file]`.
