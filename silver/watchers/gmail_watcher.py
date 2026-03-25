"""
Gmail Watcher — Silver Tier
Monitors Gmail for unread important emails every 2 minutes.
Creates action .md files in Needs_Action/.

Setup required:
1. Go to https://console.cloud.google.com
2. Create a project → Enable Gmail API
3. Create OAuth 2.0 credentials → Download as credentials.json
4. Place credentials.json in project root (it's in .gitignore)
5. Run once manually to complete OAuth flow: uv run python watchers/gmail_watcher.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent dir to path so we can import base_watcher
sys.path.insert(0, str(Path(__file__).parent.parent))
from watchers.base_watcher import BaseWatcher, VAULT_PATH

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS_FILE = Path(__file__).parent.parent / "credentials.json"
TOKEN_FILE = Path(__file__).parent.parent / "token.json"


def get_gmail_service():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"credentials.json not found at {CREDENTIALS_FILE}\n"
                    "Download it from Google Cloud Console → APIs & Services → Credentials"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds)


class GmailWatcher(BaseWatcher):
    def __init__(self):
        super().__init__(check_interval=120)  # check every 2 minutes
        self.service = get_gmail_service()
        self.processed_ids: set = self._load_processed_ids()

    def _load_processed_ids(self) -> set:
        """Persist processed IDs so we don't re-process on restart."""
        state_file = VAULT_PATH / "Logs" / ".gmail_processed.json"
        if state_file.exists():
            return set(json.loads(state_file.read_text()))
        return set()

    def _save_processed_ids(self):
        state_file = VAULT_PATH / "Logs" / ".gmail_processed.json"
        state_file.write_text(json.dumps(list(self.processed_ids)))

    def check_for_updates(self) -> list:
        results = self.service.users().messages().list(
            userId="me", q="is:unread is:important", maxResults=10
        ).execute()
        messages = results.get("messages", [])
        return [m for m in messages if m["id"] not in self.processed_ids]

    def create_action_file(self, message: dict) -> Path:
        msg = self.service.users().messages().get(
            userId="me", id=message["id"], format="full"
        ).execute()

        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        sender = headers.get("From", "Unknown")
        subject = headers.get("Subject", "No Subject")
        snippet = msg.get("snippet", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        content = f"""---
type: email
source: gmail
from: {sender}
subject: {subject}
received: {datetime.now().isoformat()}
message_id: {message["id"]}
priority: high
status: pending
---

## Email Received

**From:** {sender}
**Subject:** {subject}
**Received:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Preview
{snippet}

## Suggested Actions
- [ ] Read full email and determine urgency
- [ ] Draft a reply (requires human approval before sending)
- [ ] Flag if action needed from another party

## Claude's Notes
_Add reasoning and plan here._
"""
        filepath = self.needs_action / f"EMAIL_{timestamp}_{message['id'][:8]}.md"
        filepath.write_text(content)

        self.processed_ids.add(message["id"])
        self._save_processed_ids()
        return filepath


if __name__ == "__main__":
    watcher = GmailWatcher()
    watcher.run()
