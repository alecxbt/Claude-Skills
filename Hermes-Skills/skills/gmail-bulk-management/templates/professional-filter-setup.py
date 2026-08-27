#!/usr/bin/env python
"""
Template: Professional Gmail filter/label setup.
Copy and customize for each user's folder structure and sender list.

Usage:
  1. Define the LABELS dict with folder names and valid Gmail palette colors.
  2. Define the FILTERS list with routing rules.
  3. Run the script.

Requires: gmail.settings.basic scope on the OAuth token.
"""
import json
import os
import time
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

# ========================================
# CONFIGURATION — customize per user
# ========================================

LABELS = [
    # (name, background_color, text_color)
    # Colors MUST be from the Gmail palette — see references/gmail-bulk-operations.md
    ("LinkedIn", "#285bac", "#ffffff"),
    ("Travel", "#0b804b", "#ffffff"),
    ("Travel/Airlines", "#0b804b", "#ffffff"),
    ("Newsletters", "#fbe983", "#684e07"),
    ("Finance", "#cc3a21", "#ffffff"),
    ("Finance/Brokerage", "#cc3a21", "#ffffff"),
    ("Finance/Crypto", "#cc3a21", "#ffffff"),
    ("Finance/Banking", "#cc3a21", "#ffffff"),
    ("Accounts & Security", "#8e63ce", "#ffffff"),
    ("Shopping", "#076239", "#ffffff"),
]

# (name, query, label_id_key, remove_labels, add_trash)
# remove_labels: list of label IDs to remove (e.g. ["INBOX", "UNREAD"])
# add_trash: if True, add TRASH label (auto-trash). If False, add the folder label.
FILTERS = [
    # Auto-trash: straight to trash, never hit inbox
    ("LinkedIn notifications", "from:(linkedin.com)", None, ["INBOX", "UNREAD"], True),

    # Folder routing: label + skip inbox + mark read
    ("LinkedIn", "from:(linkedin.com)", "linkedin", ["INBOX", "UNREAD"], False),
    ("Airlines/Travel", "from:(delta.com OR united.com OR southwest.com OR aa.com OR jetblue.com OR alaskaair.com OR kayak.com OR expedia.com OR booking.com OR hotels.com OR airbnb.com)", "airlines", ["INBOX"], False),
    ("Newsletters", "from:(substack.com OR beehiiv.com OR mailchimp.com OR sendgrid.net OR convertkit.com)", "newsletters", ["INBOX", "UNREAD"], False),
    ("Shopping/Receipts", "from:(amazon.com OR ebay.com OR stockx.com OR noreply@uber.com OR usps.com OR ups.com OR fedex.com)", "shopping", ["INBOX", "UNREAD"], False),

    # Keep in inbox: label but don't remove from inbox
    ("Brokerage", "from:(tdameritrade.com OR schwab.com OR fidelity.com OR vanguard.com OR robinhood.com OR webull.com)", "brokerage", [], False),
    ("Crypto", "from:(coinbase.com OR kraken.com OR binance.us OR bybit.com OR crypto.com OR gemini.com)", "crypto", [], False),
    ("Banking", "from:(chase.com OR bankofamerica.com OR discover.com OR paypal.com OR venmo.com)", "banking", [], False),
    ("Account/Security", "from:(accounts.google.com OR noreply@tm.openai.com OR mail.anthropic.com OR notifications@vercel.com OR github.com)", "security", [], False),

    # Category catch-all: auto-archive entire categories
    ("All Promotions", "category:promotions", None, ["INBOX", "UNREAD"], False),
    ("All Social", "category:social", None, ["INBOX", "UNREAD"], False),
    ("All Forums", "category:forums", None, ["INBOX", "UNREAD"], False),
]

# ========================================
# EXECUTION — don't modify below
# ========================================

def create_label(service, name, bg, text="#ffffff"):
    body = {
        "name": name,
        "messageListVisibility": "show",
        "labelListVisibility": "labelShow",
        "color": {"backgroundColor": bg, "textColor": text}
    }
    try:
        result = service.users().labels().create(userId="me", body=body).execute()
        print(f"  ✓ Label: {name} → {result['id']}")
        return result
    except Exception:
        labels = service.users().labels().list(userId="me").execute().get("labels", [])
        for l in labels:
            if l["name"].lower() == name.lower():
                print(f"  → Exists: {name} → {l['id']}")
                return l
        raise

def create_filter(service, query, add_labels, remove_labels, name):
    body = {"criteria": {"query": query}, "action": {}}
    if add_labels:
        body["action"]["addLabelIds"] = add_labels
    if remove_labels:
        body["action"]["removeLabelIds"] = remove_labels
    try:
        result = service.users().settings().filters().create(userId="me", body=body).execute()
        print(f"  ✓ Filter: {name}")
        return result
    except Exception as e:
        print(f"  ✗ Filter failed: {name} → {e}")
        return None

def main():
    service = get_service()

    # Create labels
    print("=== CREATING LABELS ===\n")
    label_ids = {}
    for name, bg, text in LABELS:
        result = create_label(service, name, bg, text)
        if result:
            label_ids[name.lower().replace(" & ", "_").replace("/", "_")] = result["id"]
        time.sleep(0.2)

    # Create filters
    print("\n=== CREATING FILTERS ===\n")
    for name, query, label_key, remove_labels, add_trash in FILTERS:
        add = []
        if add_trash:
            add = ["TRASH"]
        elif label_key and label_key in label_ids:
            add = [label_ids[label_key]]
        create_filter(service, query, add if add else None, remove_labels if remove_labels else None, name)
        time.sleep(0.3)

    # Summary
    all_labels = service.users().labels().list(userId="me").execute().get("labels", [])
    user_labels = [l for l in all_labels if l["type"] == "user"]
    all_filters = service.users().settings().filters().list(userId="me").execute().get("filter", [])
    print(f"\n=== DONE: {len(user_labels)} labels, {len(all_filters)} filters ===")

if __name__ == "__main__":
    main()
