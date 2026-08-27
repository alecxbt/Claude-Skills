---
name: gmail-bulk-management
description: "Use when bulk-cleaning Gmail or creating filter systems."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Gmail, bulk, cleanup, filters, labels, organization, OAuth]
    related_skills: [google-workspace, email-inbox-triage]
---

# Gmail Bulk Management

Bulk Gmail operations that go beyond single-message commands: trashing/archiving tens of thousands of emails by category, creating filter systems, and setting up professional folder/label organization. The bundled `google-workspace` skill handles individual message operations (search, read, send, reply, label one message); this skill handles operations at scale.

## When to Use

- "Clean up my Gmail" / "Delete all promotional emails"
- "Set up folders and filters for my Gmail"
- "Trash everything in Promotions/Social/Updates"
- "Create filters to auto-route emails to folders"
- "Organize my inbox professionally"

## Prerequisites

- `google-workspace` skill must be set up and authenticated (`$GSETUP --check` → `AUTHENTICATED`).
- For **filter creation**, the OAuth token must include the `gmail.settings.basic` scope. The bundled setup.py SCOPES list may not include it — check the token scopes and re-authorize if needed (see references/gmail-bulk-operations.md, "Scope Upgrade").

## References

- `references/gmail-bulk-operations.md` — the full technique guide: bulk trash/archive with batchModify, pagination via nextPageToken, filter creation via the Gmail API, the restricted label color palette, and the scope upgrade procedure. Load it before performing any bulk operation.
- `templates/professional-filter-setup.py` — copy-and-customize script for creating a complete label + filter system. Edit the LABELS and FILTERS config dicts at the top and run.

## Procedure

### 1. Assess the inbox

Use `$GAPI gmail search` with category filters to count what's in each bucket:

```
category:promotions in:inbox       — marketing junk
category:social in:inbox           — social media notifications
category:updates in:inbox          — newsletters, alerts
category:forums in:inbox            — forum digests
in:inbox -category:promotions -category:social -category:forums -category:updates  — primary
```

Present counts to the user and ask what to trash vs keep.

### 2. Bulk trash/archive

Write a Python script that uses the Gmail API directly (not the CLI wrapper — it's too slow for 50,000+ messages). The pattern:

1. Collect ALL message IDs via `users().messages().list()` with `nextPageToken` pagination (500 per page).
2. Batch modify in chunks of 1000 via `users().messages().batchModify()`:
   - **Trash**: `addLabelIds: ["TRASH"], removeLabelIds: ["INBOX"]`
   - **Archive**: `removeLabelIds: ["INBOX", "UNREAD"]` (no TRASH — keeps the email)
3. Rate-limit: 0.1-0.3s delays between API calls.

See `references/gmail-bulk-operations.md` for a complete working script template.

### 3. Create labels (folders)

Use `users().labels().create()`. **Critical**: Gmail restricts label colors to a specific palette — arbitrary hex values are rejected with HTTP 400. See the color palette reference in `references/gmail-bulk-operations.md`.

### 4. Create filters

Use `users().settings().filters().create()`. Each filter has:
- `criteria.query` — a Gmail search query (same syntax as the search bar)
- `action.addLabelIds` — labels to apply
- `action.removeLabelIds` — labels to remove (e.g. `["INBOX", "UNREAD"]` to skip inbox and mark read)

### 5. Archive old Primary emails

After trashing categories, the Primary inbox may still contain hundreds of old, no-longer-actionable emails (job applications, old work correspondence, service notifications). Archive everything older than a threshold (typically 30 days) to achieve true inbox zero:

```
in:inbox older_than:30d -category:promotions -category:social -category:forums -category:updates
```

Use `batch_archive` (remove INBOX + UNREAD, no TRASH). These emails stay searchable but out of the inbox.

### 6. Verify

After bulk operations, verify the inbox is clean:
```
$GAPI gmail search "in:inbox" --max 100
```

After filter creation, list filters to confirm:
```python
service.users().settings().filters().list(userId="me").execute()
```

## Key Decisions to Confirm with User

- **Trash vs archive**: Trash is recoverable for 30 days then permanently deleted. Archive keeps emails searchable but removes from inbox. Always confirm which the user wants.
- **Filter routing philosophy**: Which senders stay in inbox (actionable) vs auto-file (reference/noise) vs auto-trash (spam). Present a proposed mapping and get approval.
- **Category catch-all filters**: Auto-archiving all `category:promotions` etc. is a safety net that prevents future inbox buildup even from new senders.

## Pitfalls

- **Missing `gmail.settings.basic` scope**: Filter creation silently fails with HTTP 403 "Insufficient Permission". Must revoke and re-authorize with the upgraded scope. See references/gmail-bulk-operations.md.
- **Invalid label colors**: Gmail rejects arbitrary hex values. Use only colors from the official palette (see references/gmail-bulk-operations.md).
- **Token path on Windows**: `$HERMES_HOME` may differ from `~/.hermes`. Always resolve via `os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))`.
- **CLI wrapper too slow for bulk**: The `google_api.py` CLI wrapper makes one HTTP call per message for metadata. For 50,000+ messages, write a direct API script using `googleapiclient` instead.
- **Empty search results break JSON parsing**: When a category is fully trashed, the CLI wrapper may return empty output that fails `json.loads`. Handle this gracefully — empty output means success.
- **Duplicate filters**: No built-in dedup. Check existing filters with `.list()` before creating.
- **`setup.py --auth-url` flag limitations**: The setup script may not accept `--services` or `--format json` flags — it only takes `--auth-url` alone. If you need to pass custom scopes, edit the SCOPES list in `setup.py` directly before running `--auth-url`.
- **Existing filters may auto-apply to old emails**: After creating filters that match sender domains, Gmail may immediately apply them to existing emails in the inbox, removing them from inbox before you get a chance to manually trash them. This is normal — check inbox again after filter creation to see what remains.
