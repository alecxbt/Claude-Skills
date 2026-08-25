# Hermes-Skills

Custom skills, memory, and patches created by Hermes Agent for Refractor Fund Management. These are organized separately from the Claude-Skills (front-end/back-end) to distinguish their originator.

## Structure

```
Hermes-Skills/
├── README.md                  ← this file
├── skills/                    ← custom skills created during sessions
│   ├── gmail-bulk-management/ ← Gmail inbox cleanup + filter system
│   └── gateway-setup/         ← Telegram gateway + MCP server configuration
├── memory/                    ← persistent memory files
│   ├── MEMORY.md              ← environment facts, tool quirks, conventions
│   └── USER.md                ← user profile (Alec Wilson)
└── patches/                  ← modifications to bundled skills
    └── google-workspace-setup-scopes.md  ← gmail.settings.basic scope patch
```

## Skills

### gmail-bulk-management
Created: 2026-08-25

Workflow for bulk-cleaning Gmail inboxes and creating professional filter/label systems. Covers OAuth scope verification, batch trashing via `batchModify`, label creation with valid Gmail color palette, and filter creation via the Gmail API.

**Used for:** Cleaning 50,000+ emails from wilsonalec13@gmail.com and setting up 40 automated routing filters.

### gateway-setup
Created: 2026-08-25

Procedure for setting up Hermes messaging gateways (Telegram, Discord, etc.) and configuring MCP servers. Covers bot token creation, gateway installation as a startup service, and the full MCP server catalog with auth requirements.

**Used for:** Setting up Telegram bot and 8 MCP servers on Alec's Windows machine.

## Patches

### google-workspace-setup-scopes
Added `gmail.settings.basic` scope to `setup.py` SCOPES list. Required for programmatic Gmail filter management. See the patch file for the full diff and re-application instructions.

## Memory

Persistent memory files synced from `~/.hermes/memories/`. These contain environment facts, user preferences, and operational conventions that Hermes carries across sessions.

## Backup

This folder is included in the Claude-Skills repo and backed up to GitHub automatically every Wednesday at 9:05 PM EST via a cron job.
