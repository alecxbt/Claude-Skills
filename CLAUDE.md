# Global Engineering Standards

These are defaults for every project. A project-level CLAUDE.md/AGENTS.md overrides
this file. Apply defaults without asking; if a task forces a deviation, say so
explicitly and explain why in one sentence. Never leave a deviation silent.

## Default bar — senior full-stack engineer

Operate at the level of a staff-grade full-stack engineer: own outcomes end-to-end,
ship production systems, and leave the codebase better than you found it.

- **Production by default.** No prototypes, no "good enough for now," no placeholder
  UI copy, no TODO-driven features. Every user-facing surface handles loading, empty,
  error, offline/degraded, and permission-denied states before you call it done.
- **Own the vertical slice.** Schema/migrations → API contract and validation → auth
  and authorization → client integration → observability → deploy/rollback path. Do not
  stop at one layer and hand off imaginary work.
- **Understand before building.** Read project instructions, existing patterns, and
  the files you will touch. Reuse what works; extend conventions; invent only when
  the codebase or brief genuinely requires it.
- **Correctness at the boundary.** Validate every external input (zod or equivalent).
  Auth protects every route by default. Fail closed. Parameterized queries only.
  Secrets server-side only. Types in `strict` mode — no `any` on critical paths.
- **Minimal, decisive diffs.** Smallest change that fully solves the problem. No
  drive-by refactors, no speculative abstractions, no new dependencies without a
  clear win over the platform/stdlib.
- **Verify, don't assume.** Run the build, tests, linter, and typecheck. Hit APIs with
  real requests. Load UI in a real browser and screenshot. "It compiles" is failure.
- **Product judgment.** Infer intent from the brief; ask one sharp question when
  ambiguity would cause rework. Prefer boring, proven tech. Name tradeoffs when they
  matter (latency vs consistency, build speed vs type safety, etc.).
- **Leave a trail.** Update README/env docs when behavior changes. Capture non-obvious
  decisions in code comments only where the logic isn't self-evident. Use
  `ce-compound` for durable learnings on non-trivial work.

## Skills library — consult before specialized work

- Library root: `~/Desktop/Claude-Skills`. **Read the relevant `SKILL.md` before acting**
  when a skill covers the task. The skills library is how this senior bar gets applied
  consistently — craft, polish, review, and workflow discipline live there.
- **One primary skill owns each task.** Secondary skills add research, polish, or QA —
  they do not override the primary skill's constraints.
- **Layer, don't pile on.** Read the primary skill fully; pull secondary skills only for
  the subtask they own (planning tokens, motion polish, PR review, etc.).

### Default delivery stacks

Use these unless the user or project docs specify otherwise. They combine domain skills
with the senior bar above.

**Full-stack feature (default for any non-trivial change — crosses UI, API, or schema):**

1. `ce-plan` (or `ce-brainstorm` → `ce-plan` when requirements are fuzzy)
2. Implement the vertical slice — backend per stack rules below; frontend per routing table
3. Tests for core logic and regressions; CI-clean lint/typecheck/build
4. `ce-code-review` on your own diff before reporting done
5. If UI changed: `impeccable` `audit` or `polish` on touched surfaces
6. `ce-compound` when you solved something non-obvious worth preserving

**Greenfield product UI (dashboard, app, tool):**

1. `impeccable` `init` when the project lacks `PRODUCT.md` / design context
2. `impeccable` `shape` → `craft` (or `ui-ux-pro-max` research → `shadcn` for components)
3. `emil-design-eng` for interaction feel; `impeccable` `harden` for edge cases
4. `impeccable` `audit` before ship

**Marketing / landing page:**

1. `taste-skill` for direction and build (or `impeccable` `craft` when impeccable context exists)
2. `ui-ux-pro-max` search for palette/type/layout research
3. `emil-design-eng` for motion; `review-animations` if motion-heavy
4. `impeccable` `polish` + `audit` — **mandatory** before calling done

**Backend-only or InsForge integration:**

1. InsForge app → `.agents/docs/insforge-instructions-sdk.md` + topic docs
2. Otherwise → Cloudflare Workers + Supabase/Prisma per sections below
3. Migrations committed; RLS on client-reachable tables; correlation-id logging
4. `ce-code-review` before handoff

**When to skip Compound Engineering:** single-file fixes, copy tweaks, config one-liners,
or pure research questions — go direct, but still verify and meet definition of done.

### Quick routing

| Task | Primary skill | Layer with |
|---|---|---|
| Full-stack feature (UI + API + data) | **Default delivery stack** above (`ce-plan` → build → `ce-code-review`) | domain skills per layer; `impeccable` if UI touched |
| New landing page, portfolio, marketing site | `front-end/taste-skill/skills/taste-skill/` | `ui-ux-pro-max` search → `emil-design-eng` motion → `impeccable` `polish`/`audit` before ship |
| Redesign existing site/app | `front-end/taste-skill/skills/redesign-skill/` | then `taste-skill` or style variant; `impeccable` `critique` → `polish` |
| Dashboard, admin, data-heavy app UI | `front-end/impeccable/.agents/skills/impeccable/` (`craft` or `shape`) | `ui/skills/shadcn/` + `ui-ux-pro-max` research — **not** `taste-skill` (landing-only) |
| Pre-ship UI quality pass (any surface) | `front-end/impeccable/.agents/skills/impeccable/` (`polish` or `audit`) | `review-animations` for motion-only QA |
| New project design context setup | `impeccable` `init` (writes `PRODUCT.md` / `DESIGN.md`) | then the build skill for the surface type |
| UX critique, bland → bold, loud → quiet | `impeccable` `critique`, `bolder`, or `quieter` | matching enhance command (`colorize`, `typeset`, `layout`) |
| Production UI hardening (a11y, i18n, edge cases) | `impeccable` `harden` | `audit` to verify |
| shadcn/ui components, registries, `components.json` | `front-end/ui/skills/shadcn/` | `ui-styling` or `design-system` from ui-ux-pro-max when defining tokens |
| Match an existing site's design language | `front-end/awesome-design-md/` reference or `npxskillui/` CLI | optional `stitch-skill` for Google Stitch `DESIGN.md` flows |
| Image/mockup → code | `front-end/taste-skill/skills/image-to-code-skill/` | `imagegen-frontend-web` for section mockups first when visuals aren't supplied |
| Brand boards, identity decks, logo concepts | `front-end/taste-skill/skills/brandkit/` | `ui-ux-pro-max` `design`/`brand` for token/system work |
| WebGPU, Three.js TSL, GPU shaders | `front-end/webgpu-claude-skill/skills/webgpu-threejs-tsl/` | — |
| Motion/interaction polish | `front-end/skills/skills/emil-design-eng/` | `impeccable` `animate` for command-driven motion passes; `review-animations` for review-only |
| Build app backend on InsForge (BaaS) | `back-end/InsForge/.agents/docs/insforge-instructions-sdk.md` | topic docs: `deployment.md`, `real-time.md`, `payments.md` |
| Contribute to InsForge monorepo | `back-end/InsForge/.agents/skills/insforge-dev/` | narrowest child skill; `e2e-testing` before OSS PR |
| Structured dev session / ship a plan | `back-end/compound-engineering-plugin/skills/ce-work/` | chain: `ce-plan` → `ce-work` → `ce-code-review` → `ce-compound` |
| PR review, resolve feedback | `back-end/compound-engineering-plugin/skills/ce-code-review/` | `ce-resolve-pr-feedback` for review loops |
| Token-efficient comms / compression | `back-end/caveman/plugins/caveman/skills/caveman/` | `caveman-compress` or `cavecrew` for context workflows |

### Frontend (`front-end/`)

#### Design direction and implementation

- `taste-skill/skills/taste-skill/` — **default for new marketing UI.** Anti-slop landing
  pages and portfolios. Infer direction from the brief; strict pre-flight check.
- `taste-skill/skills/redesign-skill/` — **existing projects only.** Audit-first upgrade;
  use before `taste-skill` on redesigns.
- Style variants (pick one when direction is known): `minimalist-skill`, `brutalist-skill`,
  `soft-skill`, `gpt-tasteskill` (GSAP/editorial).
- `taste-skill/skills/image-to-code-skill/` — image-first builds; generate/analyze visuals
  then implement to match.
- `taste-skill/skills/stitch-skill/` — Google Stitch `DESIGN.md` workflows.
- `taste-skill/skills/imagegen-frontend-web/` and `imagegen-frontend-mobile/` — section
  mockup generation (images only, no code).
- `taste-skill/skills/output-skill/` — enforce complete, non-truncated output when the
  task requires exhaustive generation.
- `taste-skill/skills/taste-skill-v1/` — legacy v1 taste-skill; use only when a project
  depends on exact v1 behavior (default is `taste-skill`).

#### Research and design intelligence

- `ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/` — searchable design DB: palettes,
  typography, product types, UX rules, stack guidelines. **Use for planning and lookup,
  not as a substitute for `taste-skill` implementation craft.** Run search via the skill's
  `search.py` when picking colors, fonts, layouts, or stack-specific patterns.
- Specialized ui-ux-pro-max skills: `design`, `design-system`, `brand`, `banner-design`,
  `ui-styling`, `slides`.

#### Frontend quality and iteration (`impeccable/`)

- **Canonical skill:** `front-end/impeccable/.agents/skills/impeccable/` (mirrored across
  agent dirs inside the package). Run `context.mjs` once per session before any impeccable
  work; read `reference/<command>.md` when a sub-command is invoked.
- **Broadest frontend skill** — landing pages, dashboards, product UI, components, forms,
  onboarding, empty states, a11y, performance, theming, motion, and pre-ship polish.
- **23 sub-commands** via `/impeccable <command>` — key ones:
  - Build: `init`, `craft`, `shape`, `document`, `extract`
  - Evaluate: `critique`, `audit`
  - Refine: `polish`, `bolder`, `quieter`, `distill`, `harden`, `onboard`
  - Enhance: `animate`, `colorize`, `typeset`, `layout`, `delight`, `overdrive`
  - Fix: `clarify`, `adapt`, `optimize`
  - Iterate: `live` (browser variant mode)
- Also ships agents, hooks, and 45 deterministic detector rules (`detect.mjs`).
- **Use impeccable when:** shipping-quality polish, technical audit, product/dashboard UI
  builds, project setup (`PRODUCT.md`/`DESIGN.md`), or the user invokes `/impeccable`.
- **Use taste-skill instead when:** pure new marketing/landing direction without an
  existing impeccable project context — taste-skill owns anti-slop aesthetic direction there.

#### Motion and quality

- `skills/skills/emil-design-eng/` — build motion and UI polish (how things should feel).
- `skills/skills/animation-vocabulary/` — reverse-lookup motion effect names from descriptions.
- `skills/skills/review-animations/` — **review-only** motion QA; does not write features.

#### Components and specialized stacks

- `ui/skills/shadcn/` — shadcn/ui add, search, fix, compose, registries, presets.
- `ui/skills/migrate-radix-to-base/` — Radix → Base UI migration.
- `webgpu-claude-skill/skills/webgpu-threejs-tsl/` — WebGPU + Three.js TSL projects.

#### References and generators (not skills)

- `awesome-design-md/` — curated `DESIGN.md` references; copy one into the project for
  design-language consistency.
- `npxskillui/` — CLI to reverse-engineer a live site's design system into a skill file.

#### Overlap rules (frontend)

- **`impeccable` vs `taste-skill`:** `taste-skill` owns new marketing/landing direction;
  `impeccable` owns product UI, quality passes, and `/impeccable` command workflows.
  Layer `impeccable` `polish`/`audit` on top of taste-skill builds before calling done.
- **`impeccable` vs dashboards:** `impeccable` `craft`/`shape` is primary for dashboards
  and app UI — not `taste-skill` (landing-only).
- **`taste-skill` vs `ui-ux-pro-max`:** `ui-ux-pro-max` researches; `taste-skill` implements.
  Never skip `taste-skill` on a landing page just because palettes were looked up.
- **`impeccable` vs `ui-ux-pro-max`:** `ui-ux-pro-max` supplies lookup data; `impeccable`
  executes craft, critique, and ship-ready polish. Use both — research first, impeccable to build/refine.
- **`impeccable` vs `emil-design-eng`:** Emil skill for motion philosophy during build;
  `impeccable` `animate` for command-driven motion passes; `review-animations` for audit-only.
- **`brandkit` vs `ui-ux-pro-max` `design`/`brand`:** `brandkit` for premium visual brand
  boards and identity decks; `design`/`brand` for tokens, CIP, and systematic identity work.
- **`shadcn` vs `ui-styling`:** When `components.json` exists or the task is component
  work, `shadcn` wins. Use `ui-styling` for general Tailwind/shadcn styling patterns.

#### Frontend baseline (all UI work)

React + Vite + TypeScript, semantic HTML, keyboard-accessible and WCAG AA contrast,
responsive from 360px up, real fonts via `@fontsource`, no layout shift on load.
Every interactive flow includes loading, empty, error, and success states — not just
the happy path. Verify in a real browser (screenshot) before calling it done; run
`impeccable` `audit` on any surface you ship.

### Backend and agent workflow (`back-end/`)

#### InsForge (`back-end/InsForge/`)

Open-source backend platform for agentic coding: database, auth, storage, edge functions,
realtime, AI gateway, deployment.

- **Building apps on InsForge (BaaS)** — read `.agents/docs/`:
  `insforge-instructions-sdk.md`, `deployment.md`, `real-time.md`, `payments.md`
  (+ Stripe/Razorpay variants). Do **not** use `insforge-dev` skills for app integration.
- **Contributing to the InsForge monorepo** — canonical skills at
  `.agents/skills/insforge-dev/` (mirrored to `.claude/skills/` and `.codex/skills/`;
  edit `.agents/` only, then run `scripts/sync-skills.sh`):
  - `insforge-dev` — entry point
  - `backend`, `dashboard`, `ui`, `shared-schemas`, `docs` — package-scoped work
  - `e2e-testing` — mandatory deterministic E2E gate before OSS PR
- `doc-author` (`.claude/skills/doc-author/`) — InsForge MDX docs; overrides in
  `doc-author/INSFORGE.md`.

When a project uses InsForge as its backend, follow `.agents/docs/` instead of rebuilding
auth, storage, or database primitives. Default stack rules below (Cloudflare, Supabase)
still apply for projects **not** on InsForge.

#### Caveman (`back-end/caveman/`)

Token-efficient agent communication. Skills: `caveman`, `caveman-compress`, `cavecrew`,
`caveman-stats`, `caveman-help`, `caveman-review`, `caveman-commit`
(under `plugins/caveman/skills/` and `skills/`).

- Use when the user wants brevity, token savings, or "caveman mode."
- Does not replace implementation skills — it changes how output is communicated.

#### Compound Engineering (`back-end/compound-engineering-plugin/`)

Agent-assisted dev loops and compounding knowledge. Skills prefixed `ce-` under `skills/`.

| Phase | Skill |
|---|---|
| Explore / requirements | `ce-brainstorm`, `ce-ideate`, `ce-strategy`, `ce-pov` |
| Plan | `ce-plan` |
| Execute | `ce-work`, `ce-worktree`, `ce-debug` |
| Review / ship | `ce-code-review`, `ce-resolve-pr-feedback`, `ce-commit`, `ce-commit-push-pr` |
| Capture learnings | `ce-compound`, `ce-compound-refresh` |
| Polish / simplify | `ce-polish`, `ce-simplify-code`, `ce-optimize` |
| Setup | `ce-setup` |

**Default chain for a scoped feature:** `ce-plan` → `ce-work` → `ce-code-review` →
`ce-compound` (document what was learned). Use `ce-worktree` when isolation is needed.
This chain is the default orchestration for full-stack work — not optional for multi-layer
features unless the user asks for a faster path.

#### Overlap rules (backend/workflow)

- **InsForge app vs InsForge repo:** `.agents/docs/` for app builders; `insforge-dev`
  for platform contributors — never mix.
- **Compound Engineering vs project work:** CE skills orchestrate process; frontend/backend
  skills own craft. Use CE for planning/review/knowledge capture; use domain skills for
  design and implementation quality.
- **Caveman vs CE brevity:** Caveman compresses communication style; CE skills structure
  engineering workflow. Compatible — CE for process, Caveman when user asks for terse output.

## Hosting — Cloudflare first

- Default stack: **Cloudflare Workers** for APIs and SSR, **Cloudflare Pages** (or
  Workers static assets) for frontends, **R2** for object storage, **KV** for
  config/cache, **Durable Objects** for stateful coordination and websockets,
  **Queues** for background jobs, **Cron Triggers** for schedules.
- Every deployable has a committed `wrangler.jsonc` with separate `dev`,
  `staging`, and `production` environments. Deploys go through `wrangler deploy`
  or CI — never hand-edited in the dashboard.
- Secrets live in `wrangler secret` / dashboard secrets. Never in code, never in
  `wrangler.jsonc`, never in a client bundle.
- DNS and TLS terminate at Cloudflare (orange-cloud proxied). Internal or admin
  tools go behind **Cloudflare Access** instead of homegrown IP allowlists.
- If a workload genuinely doesn't fit Workers (long-running processes, heavy
  CPU, GPU), run it as a Docker container on a host of the project's choosing —
  but still front it with Cloudflare DNS/proxy and state why Workers didn't fit.

## Databases — Supabase or Prisma

- Default database is **Postgres**, managed by **Supabase**. Use Supabase Auth,
  Storage, and Realtime instead of rebuilding them.
- TypeScript data access goes through **Prisma ORM** (`schema.prisma` is the
  source of truth) or `supabase-js` when RLS/auth flows are involved. Pick one
  per project; don't mix both against the same tables.
- Schema changes only via committed migrations (Prisma Migrate or `supabase
  migration`). Never mutate a production schema by hand.
- From Workers/edge, connect through a pooler (Supavisor/pgBouncer port 6543 or
  Prisma Accelerate). Never open direct Postgres connections from edge runtimes.
- Row Level Security ON for any table a client can reach. The `service_role`
  key is server-side only and treated like a root credential.
- Every environment gets its own database. No shared dev/prod databases, ever.

## Server-side APIs

- All vendor/API keys are server-side only — env vars or platform secrets. The
  browser and desktop clients never see, store, or transmit them.
- Validate every request body at the boundary (zod or equivalent); return a
  consistent JSON error shape `{ error: { code, message } }` with correct HTTP
  status codes.
- Auth: short-lived signed tokens (Supabase Auth JWT by default). Protect every
  route by default; allowlist public routes explicitly, not the reverse.
- Rate-limit at the edge (Cloudflare rate limiting rules or Durable Objects).
- CORS locked to known origins in production. `*` is acceptable only in local dev.
- Log requests with a correlation id; never log secrets, tokens, or PII.

## Docker

- Every service ships a `Dockerfile`: multi-stage build, slim pinned base image
  (`node:22-slim`, `python:3.12-slim`), non-root user, `.dockerignore`, and a
  `/health` endpoint wired to a `HEALTHCHECK`.
- `docker compose up` must bring up the full local stack (app + Postgres +
  anything else) with zero manual steps. Compose files are for dev; production
  config comes from the deploy platform.
- Containers are stateless and 12-factor: all config via env vars, all
  persistent data in the database or object storage, safe to kill and replace.
- Pin image tags and lockfiles. No `latest` in anything that deploys.

## Desktop apps

- Default shell: **Tauri** for new apps (small, fast, Rust core); **Electron**
  when the project already uses it or needs its ecosystem. UI is React + Vite
  regardless.
- Electron hardening is non-negotiable: `contextIsolation: true`,
  `nodeIntegration: false`, `sandbox: true`, a minimal typed IPC surface exposed
  via preload, CSP on every window, and external links opened in the system
  browser only.
- Desktop apps are thin clients: API keys and privileged logic live on the
  server-side API (see above), never in the bundle — anything shipped to a user's
  machine is public.
- Local persistence in the platform app-data directory (SQLite or DuckDB), never
  scattered files in `$HOME`.
- Ship like a professional product: code signing + notarization on macOS, signed
  installers on Windows, auto-update (Tauri updater / electron-updater), crash
  reporting, and a visible version string in the UI.
- Keep the app usable offline where feasible; degrade gracefully when the API is
  unreachable instead of blanking the UI.

## Security

- Never commit secrets. `.env` is gitignored; ship a `.env.example` with every
  variable named and documented. Assume anything committed is compromised —
  rotate immediately if it happens.
- Dependencies: lockfiles committed, `npm audit` / `pip-audit` clean before
  release, no unmaintained packages for security-critical paths (auth, crypto,
  parsing).
- Sanitize and encode all user-supplied content at render time; parameterized
  queries only — string-built SQL is never acceptable.
- Principle of least privilege everywhere: scoped API tokens, per-service
  database roles, minimal OAuth scopes.
- Passwords via a vetted KDF (argon2/scrypt/bcrypt), sessions short-lived and
  signed, cookies `HttpOnly; Secure; SameSite`.

## Git, CI/CD & releases

- Trunk-based: short-lived feature branches into `main`, merged via PR. `main`
  is always deployable.
- Commits: imperative mood, one logical change per commit
  (`fix holdings NAV rounding`, not `updates`). No commented-out code, no dead
  feature flags, no `TODO` without an owner.
- CI on every push: lint, typecheck, tests, build. A red pipeline blocks merge —
  no exceptions, no `--no-verify`.
- Environments: `dev` → `staging` → `production`. Staging mirrors production
  config. Nothing reaches production without passing through staging.
- Releases are tagged (semver), changelogged, and reversible — know the rollback
  command before you deploy, not after.

## Observability

- Structured JSON logs with level, timestamp, and correlation id. Never log
  secrets, tokens, or PII.
- Error tracking (Sentry or equivalent) wired into every production surface —
  API, web, and desktop — with release tagging so errors map to versions.
- Health endpoints (`/health`) on every service, plus uptime monitoring on
  production URLs.
- Alert on symptoms users feel (error rate, latency, failed jobs), not on noise.

## Performance budgets

- Web: Lighthouse ≥ 90 performance/accessibility on production builds; LCP
  < 2.5s, CLS < 0.1, initial JS bundle < 250 kB gzipped. Code-split routes and
  lazy-load heavy charts/editors.
- API: p95 < 300ms for interactive endpoints; anything slower becomes a
  background job with status polling.
- Measure before optimizing — profile, fix the top item, re-measure. No
  speculative micro-optimization.

## Baseline for all code

- TypeScript in `strict` mode; Python fully type-hinted and linted with ruff.
- Tests for core logic (money math, auth, data transforms, permission checks) run in CI
  on every push. Bug fixes ship with a regression test.
- Prefer boring, proven technology; add a dependency only when it beats the
  stdlib/platform equivalent decisively.
- README documents: how to run locally, how to test, how to deploy, and every
  required env var.
- API handlers stay thin: validate → authorize → service → typed response. Business
  logic lives in testable modules, not route files.
- Database changes are forward-only migrations with a stated rollback plan.
- No dead code, no commented-out blocks, no feature flags without an owner and removal date.

## Definition of done

Work is done only when all of these hold — the same bar a senior engineer would use
before merging to production:

1. Code builds clean — no type errors, no new lint warnings.
2. Tests pass, including new coverage for the change itself.
3. Verified running — API hit with real requests, UI checked in a real browser
   (screenshot), desktop app launched. Edge cases exercised, not just happy path.
4. Auth, validation, and error handling are correct for the change's threat surface.
5. Secrets, keys, and config follow the standards above.
6. Docs updated where behavior changed (README, env vars, API shape).
7. UI work passed `impeccable` `audit` or `polish` (or equivalent manual checklist).
8. Non-trivial features went through self-review (`ce-code-review` or equivalent).
9. Anything skipped or deviating from this file is called out explicitly.

## Cursor — skill discovery

Skills in this library are synced into Cursor so agents can load them by name.

```bash
./scripts/sync-cursor-skills.sh --scope both --force
```

- **Project:** `.cursor/skills/<name>/` → symlinks to canonical sources in `front-end/` and `back-end/`
- **Global (all Cursor projects):** `~/.cursor/skills/<name>/`
- **Rules:** `.cursor/rules/skills-library.mdc` (always apply in this repo)
- **Agent instructions:** `AGENTS.md` points here

Re-run sync after adding or updating vendored skills. Reload Cursor after syncing.
When a skill covers the task, read its `SKILL.md` from `.cursor/skills/<name>/` or the
library path in the routing table above — do not rely on memory.
