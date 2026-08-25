# MCP Server Catalog — Investment Firm Tech Stack

Recommended MCP servers for a full-stack investment management firm building in-house technology. Organized by priority tier.

## Tier 1 — Core Infrastructure

### GitHub (stdio, PAT-based)
- **Package:** `@modelcontextprotocol/server-github` via npx
- **Auth:** GitHub Personal Access Token (PAT) with `repo`, `read:org`, `read:user` scopes
- **Config:** `hermes mcp add github --command npx --args -y @modelcontextprotocol/server-github --env GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx`
- **Tools:** 26 — create/merge PRs, search code/repos, create branches, issues, reviews
- **Use case:** Dev workflow — branch, commit, PR, review. User reviews before merge.

### Cloudflare (HTTP, OAuth)
- **URL:** `https://mcp.cloudflare.com/mcp`
- **Auth:** OAuth via `setup_mcp(action='install', server='cloudflare')`
- **Use case:** DNS, Workers, Pages, R2, KV — Cloudflare-first hosting standard

### Supabase (HTTP, OAuth)
- **URL:** `https://mcp.supabase.com/mcp`
- **Auth:** OAuth via `setup_mcp`
- **Use case:** Postgres DB, auth, storage, realtime — default database layer

### Context7 (HTTP, no auth)
- **URL:** `https://mcp.context7.com/mcp`
- **Auth:** None
- **Use case:** Version-specific library docs — React, Prisma, Cloudflare Workers API references

## Tier 2 — Research & Operations

### Twelve Data (HTTP, API key)
- **URL:** `https://mcp.twelvedata.com/...`
- **Auth:** API key from https://twelvedata.com/ (free tier available)
- **Use case:** Live market data — stocks, forex, crypto. Sector tracking for AI infrastructure equities.

### Sentry (HTTP, OAuth)
- **URL:** `https://mcp.sentry.dev/mcp`
- **Auth:** OAuth via `setup_mcp`
- **Use case:** Error tracking for production surfaces — observability standard

### DeepWiki (HTTP, no auth)
- **URL:** `https://mcp.deepwiki.com/mcp`
- **Auth:** None
- **Use case:** Ask questions about any public GitHub repo — open-source research

### Wolfram (HTTP, App ID)
- **URL:** `https://agenttools.wolfram.com/...`
- **Auth:** App ID from https://products.wolframalpha.com/api/
- **Use case:** Computation, math, curated financial/data knowledge — modeling

## Tier 3 — Situational

### Calendly (OAuth)
- **Use case:** Scheduling links for investor meetings

### Todoist (OAuth)
- **Use case:** Personal task tracking across work and firm-building

### Notion (OAuth)
- **Use case:** If using Notion for notes/dashboards instead of Obsidian

### Fireflies (OAuth)
- **Use case:** Meeting transcripts — auto-capture investor call notes

## Installation Patterns

### OAuth-based (catalog) — use setup_mcp tool
```
setup_mcp(action='install', server='<name>', reason='<one sentence why>')
```

### PAT-based (stdio) — use hermes mcp add CLI
```bash
echo "Y" | hermes mcp add <name> --command npx --args -y <package> --env KEY=value --connect-timeout 60
```

### Verification
```bash
hermes mcp list    # Shows all servers, transport, tools, status
```

**Note:** New MCP servers require a new session to activate — they load at startup, not mid-session.
