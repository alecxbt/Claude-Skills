---
name: gateway-setup
description: "Set up Hermes messaging gateways and MCP servers."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gateway, telegram, mcp, setup, configuration, messaging]
    related_skills: [hermes-agent]
---

# Gateway Setup

Configure Hermes messaging platforms (Telegram, Email, etc.) and MCP servers. This skill covers the operational setup workflows — credential placement, gateway lifecycle, and MCP server installation patterns.

## When to Use

- User asks to set up Telegram, Email, or any messaging gateway
- User asks to install or configure MCP servers (GitHub, Cloudflare, Supabase, etc.)
- Gateway fails to start with "No bot token configured" or similar credential errors
- User wants to connect their phone via Telegram for mobile agent access
- Setting up cron jobs that need a messaging platform for delivery

## Prerequisites

- Hermes Agent installed and configured (`hermes setup` done)
- For Telegram: a bot token from @BotFather and the user's numeric Telegram ID
- For MCP servers: Node.js (for npx-based servers) or uv (for uvx-based servers), plus the `mcp` Python package

## MCP Server Installation

### Catalog Servers (OAuth or no-auth)

Use the `setup_mcp` tool for servers in the Hermes MCP catalog. It shows an inline consent card and handles OAuth flows:

```
setup_mcp(action='install', server='cloudflare', reason='Cloudflare-first hosting per CLAUDE.md')
```

Catalog servers to prioritize for a full-stack investment firm:
- **cloudflare** — DNS, Workers, Pages, R2, KV
- **supabase** — Postgres DB, auth, storage, realtime
- **context7** — version-specific library docs (no auth needed)
- **twelve-data** — market data (stocks, forex, crypto; API key needed)
- **sentry** — error tracking
- **deepwiki** — public GitHub repo Q&A (no auth needed)
- **wolfram** — computation and curated knowledge

### Manual stdio Servers (PAT/command-based)

GitHub and other PAT-based servers require `hermes mcp add`. The `setup_mcp` tool does NOT handle these — use the CLI:

```bash
hermes mcp add <name> --command npx --args -y <npm-package> --env KEY=value --connect-timeout 60
```

#### GitHub MCP Server

```bash
hermes mcp add github \
  --command npx \
  --args -y @modelcontextprotocol/server-github \
  --env GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxx \
  --connect-timeout 60
```

**Pitfall — interactive confirmation prompt:** `hermes mcp add` connects to the server, discovers tools, then asks "Enable all tools? [Y/n/select]". In a non-interactive terminal (e.g., from Hermes terminal tool), this prompt may auto-cancel. Pipe `Y` to confirm:

```bash
echo "Y" | hermes mcp add github --command npx --args -y @modelcontextprotocol/server-github --env GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxx --connect-timeout 60
```

### Verify MCP Configuration

```bash
hermes mcp list
```

Shows all configured servers, their transport, tool count, and status. A new session is required to pick up newly added MCP tools — they load at startup.

## Telegram Gateway Setup

### Step 1: Create the Bot

1. User opens Telegram, messages @BotFather
2. Sends `/newbot`, chooses display name and username (must end in `bot`)
3. BotFather returns the API token (format: `123456789:ABCdef...`)

### Step 2: Get the User's Numeric Telegram ID

The user messages @userinfobot on Telegram, which replies with their numeric ID. This is NOT the username.

### Step 3: Configure Credentials — .env NOT config.yaml

**CRITICAL PITFALL:** `hermes config set gateway.platforms.telegram.bot_token <token>` writes to `config.yaml`, but the Hermes gateway process reads Telegram credentials from the `.env` file. Setting the token via `hermes config set` will result in a "No bot token configured" error on gateway startup.

**Always write Telegram credentials to `.env`:**

```bash
# Uncomment and fill the TELEGRAM_BOT_TOKEN line in .env
sed -i 's/# TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=<token>/' ~/.hermes/.env
sed -i 's/# TELEGRAM_ALLOWED_USERS=.*/TELEGRAM_ALLOWED_USERS=<user_id>/' ~/.hermes/.env
```

You can also set `config.yaml` values for non-credential settings (like `enabled: true`, `allowed_users`), but credentials MUST go in `.env`.

### Step 4: Install and Start the Gateway

```bash
hermes gateway install     # Installs as a service (Linux systemd / macOS launchd / Windows Startup folder)
hermes gateway start       # Start the service
hermes gateway status      # Check if running
```

On Windows, `hermes gateway install` creates a Startup folder item. It may prompt for UAC elevation for a Scheduled Task — if denied, it falls back to the Startup folder, which is fine.

### Step 5: Verify Connection

```bash
tail -20 ~/.hermes/logs/gateway.log
```

Look for `✓ telegram connected` and `Gateway running with 1 platform(s)`. If you see `No bot token configured`, the credentials are not in `.env` — fix Step 3.

### Step 6: Register the Chat

The gateway shows "0 target(s)" in the channel directory until the user sends their first message to the bot. The user must:
1. Open Telegram
2. Find the bot they created
3. Tap Start
4. Send any message

Only after this does the chat register, enabling cron job delivery to that chat.

### Customizing the Bot (Optional)

Message @BotFather on Telegram:
- `/setdescription` — "What can this bot do?" text
- `/setuserpic` — avatar
- `/setcommands` — command menu

### Privacy Mode (for Groups)

Telegram bots have privacy mode ON by default — they only see `/` commands, replies, and service messages. For group use:
- `/mybots` → select bot → Bot Settings → Group Privacy → Turn off
- OR promote the bot to group admin (admin bots see all messages regardless)
- Must remove and re-add the bot to any group after changing privacy mode

## Email Gateway Setup

The email gateway uses IMAP/SMTP and requires credentials in `.env` (same pitfall as Telegram — do NOT use `hermes config set` for credentials):

```bash
EMAIL_ADDRESS=hermes@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop    # App password (not regular password)
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_ALLOWED_USERS=your@email.com
EMAIL_POLL_INTERVAL=15
```

For Gmail: enable 2FA, then create an App Password at Google Account → Security → App Passwords.

## Gateway Lifecycle

```bash
hermes gateway              # Run in foreground
hermes gateway install      # Install as service
hermes gateway start        # Start the service
hermes gateway stop         # Stop the service
hermes gateway status       # Check status
```

Logs: `~/.hermes/logs/gateway.log`

## Cron Jobs (Post-Setup)

Once a messaging platform is live, create scheduled jobs via the `cronjob` tool. Common EA patterns:
- **Morning brief** — daily at 7 AM: calendar + urgent emails → Telegram
- **Weekly report** — Fridays: portfolio performance → Email or Telegram
- **Weekly recap** — Friday EOD: work summary → Obsidian Brain folder

Deliver to Telegram by default (auto-detected). Use `deliver='platform:chat_id:thread_id'` for specific targets.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No bot token configured` | Token is in config.yaml, not .env. Write `TELEGRAM_BOT_TOKEN` to `~/.hermes/.env` |
| `telegram failed to connect` | Check `.env` has `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ALLOWED_USERS`; restart gateway |
| Gateway not running after reboot | Run `hermes gateway install` to install the startup service, then `hermes gateway start` |
| `0 target(s)` in channel directory | User hasn't messaged the bot yet. Send a message to register the chat |
| MCP tools not available | New MCP servers require a new session to load. Restart Hermes or start a new chat |
| `hermes mcp add` cancelled | Non-interactive terminal didn't confirm tool enablement. Pipe `echo "Y" \|` before the command |
| Telegram dependencies missing | Gateway auto-installs on first start. Check `gateway.log` for install progress |

## References

- `references/mcp-server-catalog.md` — recommended MCP servers for an investment firm tech stack, with setup notes
