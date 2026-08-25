# Patch: google-workspace setup.py — Add gmail.settings.basic scope

## File
`skills/productivity/google-workspace/scripts/setup.py`

## Date
2026-08-25

## Change
Added `https://www.googleapis.com/auth/gmail.settings.basic` to the SCOPES list to enable programmatic Gmail filter creation via the API.

## Diff
```diff
 SCOPES = [
     "https://www.googleapis.com/auth/gmail.readonly",
     "https://www.googleapis.com/auth/gmail.send",
     "https://www.googleapis.com/auth/gmail.modify",
+    "https://www.googleapis.com/auth/gmail.settings.basic",
     "https://www.googleapis.com/auth/calendar",
     "https://www.googleapis.com/auth/drive",
     "https://www.googleapis.com/auth/contacts.readonly",
     "https://www.googleapis.com/auth/spreadsheets",
     "https://www.googleapis.com/auth/documents",
 ]
```

## Why
The `gmail.settings.basic` scope is required to create, modify, and delete Gmail filters via the API (`users().settings().filters()`). Without it, filter creation returns HTTP 403 "Insufficient Permission". Discovered during the Gmail bulk cleanup when attempting to create automated routing filters.

## How to Apply
If Hermes is reinstalled or the skill is updated from upstream, re-apply this patch by adding the scope line to the SCOPES list in `setup.py`, then run `setup.py --revoke` followed by `setup.py --auth-url` to re-authorize with the upgraded scope.
