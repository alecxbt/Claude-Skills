# Gmail Bulk Operations

Techniques for bulk Gmail management: trashing/archiving thousands of emails, creating filters, and managing labels via the Gmail API directly.

## Scope Upgrade: gmail.settings.basic

The bundled `google-workspace` setup.py may not include `gmail.settings.basic` in its SCOPES list. Without it, filter creation fails with HTTP 403 "Insufficient Permission".

**To check current scopes:**
```python
import json, os
token_path = os.path.join(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")), "google_token.json")
with open(token_path) as f:
    t = json.load(f)
for s in t.get("scopes", []):
    print(s)
```

**To upgrade:**
1. Add `"https://www.googleapis.com/auth/gmail.settings.basic"` to the SCOPES list in `setup.py`.
2. Revoke: `$GSETUP --revoke`
3. Generate new auth URL: `$GSETUP --auth-url`
4. User completes OAuth consent flow (same process as initial setup).
5. Verify: `$GSETUP --check` → `AUTHENTICATED`.

## Bulk Trash/Archive Pattern

For 50,000+ messages, the CLI wrapper (`google_api.py`) is too slow — it makes one HTTP call per message for metadata. Use the Gmail API directly with `googleapiclient`.

### Complete working script:

```python
import json, os, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
TOKEN_PATH = os.path.join(HERMES_HOME, "google_token.json")

def get_service():
    with open(TOKEN_PATH, "r") as f:
        token_data = json.load(f)
    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get("token_uri"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=token_data.get("scopes"),
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)

def collect_message_ids(service, query):
    """Collect ALL message IDs matching a query, paginating through everything."""
    all_ids = []
    page_token = None
    while True:
        kwargs = {"userId": "me", "q": query, "maxResults": 500}
        if page_token:
            kwargs["pageToken"] = page_token
        result = service.users().messages().list(**kwargs).execute()
        messages = result.get("messages", [])
        all_ids.extend([m["id"] for m in messages])
        page_token = result.get("nextPageToken")
        if not page_token:
            break
        time.sleep(0.1)
    return all_ids

def batch_trash(service, message_ids):
    """Trash messages in batches of 1000 (API limit)."""
    trashed = 0
    for i in range(0, len(message_ids), 1000):
        batch = message_ids[i:i+1000]
        service.users().messages().batchModify(
            userId="me",
            body={
                "ids": batch,
                "addLabelIds": ["TRASH"],
                "removeLabelIds": ["INBOX"],
            }
        ).execute()
        trashed += len(batch)
        time.sleep(0.3)
    return trashed

def batch_archive(service, message_ids):
    """Archive messages (remove from inbox, mark read) in batches of 1000."""
    archived = 0
    for i in range(0, len(message_ids), 1000):
        batch = message_ids[i:i+1000]
        service.users().messages().batchModify(
            userId="me",
            body={
                "ids": batch,
                "removeLabelIds": ["INBOX", "UNREAD"],
            }
        ).execute()
        archived += len(batch)
        time.sleep(0.3)
    return archived
```

### Common queries for bulk cleanup:

```python
queries = {
    "promotions": "category:promotions in:inbox",
    "social": "category:social in:inbox",
    "updates": "category:updates in:inbox",
    "forums": "category:forums in:inbox",
    "old_primary": "in:inbox older_than:30d -category:promotions -category:social -category:forums -category:updates",
}
```

## Filter Creation

```python
def create_filter(service, query, add_labels=None, remove_labels=None, name=""):
    body = {
        "criteria": {"query": query},
        "action": {}
    }
    if add_labels:
        body["action"]["addLabelIds"] = add_labels
    if remove_labels:
        body["action"]["removeLabelIds"] = remove_labels
    try:
        result = service.users().settings().filters().create(
            userId="me", body=body
        ).execute()
        print(f"  ✓ {name}")
        return result
    except Exception as e:
        print(f"  ✗ {name}: {e}")
        return None
```

### Filter action patterns:

| Goal | addLabelIds | removeLabelIds |
|------|-------------|---------------|
| Auto-trash | `["TRASH"]` | `[]` |
| Auto-archive + mark read | `[]` | `["INBOX", "UNREAD"]` |
| Label + skip inbox | `["Label_ID"]` | `["INBOX"]` |
| Label + keep in inbox | `["Label_ID"]` | `[]` |
| Label + skip inbox + mark read | `["Label_ID"]` | `["INBOX", "UNREAD"]` |

## Label Creation

```python
def create_label(service, name, bg_color, text_color="#ffffff"):
    body = {
        "name": name,
        "messageListVisibility": "show",
        "labelListVisibility": "labelShow",
        "color": {"backgroundColor": bg_color, "textColor": text_color}
    }
    try:
        result = service.users().labels().create(userId="me", body=body).execute()
        return result
    except Exception as e:
        # Maybe already exists — find it
        labels = service.users().labels().list(userId="me").execute().get("labels", [])
        for l in labels:
            if l["name"].lower() == name.lower():
                return l
        raise
```

## Gmail Label Color Palette

Gmail rejects arbitrary hex colors with HTTP 400 "Label color is not on the allowed color palette". Use only these values:

**Background colors (pick from this list):**
```
#000000 #434343 #666666 #999999 #cccccc #efefef #f3f3f3 #ffffff
#fb4c2f #ffad47 #fad165 #16a766 #43d692 #4a86e8 #a479e2 #f691b3
#f6c5be #ffe6c7 #fef1d1 #b9e4d0 #c6f3de #c9daf8 #e4d7f5 #fcdee8
#efa093 #ffd6a2 #fce8b3 #89d3b2 #a0eac9 #a4c2f4 #d0bcf1 #fbc8d9
#e66550 #ffbc6b #fcda83 #44b984 #68dfa9 #6d9eeb #b694e8 #f7a7c0
#cc3a21 #eaa041 #f2c960 #149e60 #3dc789 #3c78d8 #8e63ce #e07798
#ac2b16 #cf8933 #d5ae49 #0b804b #2a9c68 #285bac #653e9b #b65775
#822111 #a46a21 #aa8831 #076239 #1a764d #1c4587 #41236d #83334c
#464646 #e7e7e7 #0d3472 #b6cff5 #0d3b44 #98d7e4 #3d188e #e3d7ff
#711a36 #fbd3e0 #8a1c0a #f2b2a8 #7a2e0b #ffc8af #7a4706 #ffdeb5
#594c05 #fbe983 #684e07 #fdedc1 #0b4f30 #b3efd3 #04502e #a2dcc1
#c2c2c2 #4986e7 #2da2bb #b99aff #994a64 #f691b2 #ff7537 #ffad46
#662e37 #ebdbde #cca6ac #094228 #42d692 #16a765
```

Text colors must be from the same list. Common pairings:
- Blue label: bg `#285bac`, text `#ffffff`
- Green label: bg `#0b804b`, text `#ffffff`
- Red label: bg `#cc3a21`, text `#ffffff`
- Purple label: bg `#8e63ce`, text `#ffffff`
- Yellow label: bg `#fbe983`, text `#684e07`
- Teal label: bg `#076239`, text `#ffffff`
- Orange label: bg `#cf8933`, text `#ffffff`

Source: [Gmail API labels reference](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.labels)
