# Global Engineering Standards

These are defaults for every project. A project-level CLAUDE.md/AGENTS.md overrides
this file. Apply defaults without asking; if a task forces a deviation, say so
explicitly and explain why in one sentence. Never leave a deviation silent.

## Skills library — consult before specialized work

- A curated skills library lives at `~/Desktop/Claude-Skills`. **Consult it
  before website design, frontend polish, InsForge platform work, or InsForge
  app integration** — read the relevant `SKILL.md` files and follow them; do not
  improvise from instinct when a skill covers the task.

### Frontend (`front-end/`)

- **Consult before any website design or frontend work.**
- What's there:
  - `leonxinx/taste-skill/skills/` — design taste and direction: `taste-skill`,
    `minimalist-skill`, `brutalist-skill`, `soft-skill`, `brandkit`,
    `redesign-skill`, `image-to-code-skill`, `stitch-skill`, image-gen skills
    for web and mobile mockups.
  - `emilkowalski/skills/` — motion and polish: `animation-vocabulary`,
    `emil-design-eng`, `review-animations`.
  - `pbakaus/impeccable/` — frontend-quality skills, agents, and hooks.
- Selection rule: pick the skill matching the task (new design → a taste/style
  skill; restyling → `redesign-skill`; animation work → Emil's skills; quality
  pass → impeccable). When in doubt, start with `taste-skill`.
- Frontend baseline regardless of skill: React + Vite + TypeScript, semantic
  HTML, keyboard-accessible and WCAG AA contrast, responsive from 360px up,
  real fonts loaded via `@fontsource`, no layout shift on load, and verify the
  result in a real browser (screenshot) before calling it done.

### Backend — InsForge (`back-end/InsForge/`)

- **Vendored copy of [InsForge/InsForge](https://github.com/InsForge/InsForge)** —
  open-source backend platform for agentic coding (database, auth, storage,
  edge functions, realtime, AI gateway, deployment).
- Maintainer skills — canonical source is `.agents/skills/insforge-dev/` (mirrored
  to `.claude/skills/` and `.codex/skills/`; edit only `.agents/` then run
  `scripts/sync-skills.sh`):
  - `insforge-dev` — entry point for contributing to the InsForge monorepo.
  - `backend` — API routes, services, providers, auth, database, schedules.
  - `dashboard` — shared dashboard package (`packages/dashboard/`).
  - `ui` — reusable design-system primitives (`packages/ui/`).
  - `shared-schemas` — cross-package Zod contracts and exported types.
  - `docs` — product docs, agent docs, SDK guides, OpenAPI specs.
  - `e2e-testing` — deterministic E2E gate before opening or updating an
    InsForge OSS PR.
- `doc-author` (`.claude/skills/doc-author/`) — writing and maintaining InsForge
  MDX docs; InsForge-specific overrides live in `doc-author/INSFORGE.md`.
- Agent reference docs (`.agents/docs/`) — use when building apps **on** InsForge
  as BaaS (not when editing the platform itself): `insforge-instructions-sdk.md`,
  `deployment.md`, `real-time.md`, `payments.md` (+ Stripe/Razorpay variants).
- Selection rule: contributing to InsForge itself → start with `insforge-dev`,
  then the narrowest child skill; writing InsForge docs → `doc-author`; integrating
  InsForge SDK/MCP in an app → `.agents/docs/`; opening an InsForge PR →
  `e2e-testing`.

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
- Tests for core logic (money math, auth, data transforms) run in CI on every
  push. Bug fixes ship with a regression test.
- Prefer boring, proven technology; add a dependency only when it beats the
  stdlib/platform equivalent decisively.
- README documents: how to run locally, how to test, how to deploy, and every
  required env var.

## Definition of done

Work is done only when all of these hold:

1. Code builds clean — no type errors, no new lint warnings.
2. Tests pass, including new coverage for the change itself.
3. Verified running — API hit with real requests, UI checked in a real browser
   (screenshot), desktop app launched. "It compiles" is not verification.
4. Secrets, keys, and config follow the standards above.
5. Docs updated where behavior changed (README, env vars, API shape).
6. Anything skipped or deviating from this file is called out explicitly.
