"""
WhatsApp Watcher — Silver Tier
Monitors WhatsApp Web for urgent messages using Playwright browser automation.
Creates action .md files in Needs_Action/.

Setup required:
1. Run once to scan QR code: uv run python watchers/whatsapp_watcher.py --setup
2. After scanning, session is saved to whatsapp_session/ (in .gitignore)
3. Subsequent runs reuse the saved session (no QR scan needed)

Note: WhatsApp Web automation — use responsibly and in line with WhatsApp ToS.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from watchers.base_watcher import BaseWatcher, VAULT_PATH

from playwright.sync_api import sync_playwright

SESSION_PATH = Path(__file__).parent.parent / "whatsapp_session"
URGENT_KEYWORDS = ["urgent", "asap", "invoice", "payment", "help", "emergency", "important"]


class WhatsAppWatcher(BaseWatcher):
    def __init__(self):
        super().__init__(check_interval=90)  # 90s — page load takes ~45s, avoid overlapping cycles
        self.processed_messages: set = set()

    def check_for_updates(self) -> list:
        messages = []
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                str(SESSION_PATH),
                headless=False,
                args=[
                    "--no-sandbox",
                    "--window-position=-10000,-10000",  # fully off-screen
                    "--window-size=1280,720",            # real size so DOM renders
                ],
            )
            try:
                page = browser.pages[0] if browser.pages else browser.new_page()
                self.logger.info("WhatsApp: navigating to web.whatsapp.com...")
                page.goto("https://web.whatsapp.com", timeout=60000)
                # Try multiple selectors — WhatsApp Web updates its DOM periodically
                loaded = False
                for selector in ['[data-testid="chat-list"]', '#pane-side', '[aria-label="Chat list"]']:
                    try:
                        page.wait_for_selector(selector, timeout=45000)
                        loaded = True
                        self.logger.info(f"WhatsApp: chat list loaded (selector: {selector})")
                        page.wait_for_timeout(3000)  # let list items fully render
                        break
                    except Exception:
                        continue
                if not loaded:
                    self.logger.warning("WhatsApp: chat list did not load — session may be expired")
                    return messages

                # Find chats with unread messages — WhatsApp uses role="row" for chat rows
                seen_in_this_run: set = set()
                chat_rows = page.query_selector_all('#pane-side div[role="grid"] div[role="row"]')
                self.logger.info(f"WhatsApp: found {len(chat_rows)} chat rows")
                for item in chat_rows:
                    try:
                        # Check if this row contains an unread badge
                        has_unread = page.evaluate(
                            "(el) => !!el.querySelector('[aria-label*=\"unread\"]')",
                            item
                        )
                        if not has_unread:
                            continue
                        text = item.inner_text().strip()
                        if not text:
                            continue
                        # Extract contact name from the title span, not inner_text first line
                        sender = page.evaluate(
                            """(el) => {
                                const title = el.querySelector('[data-testid="cell-frame-title"] span, [title], span[dir="auto"]');
                                return title ? title.textContent.trim() : null;
                            }""",
                            item
                        ) or text.split("\n")[0].strip()
                        if not sender or sender in seen_in_this_run:
                            continue
                        seen_in_this_run.add(sender)
                        msg_id = hash(sender)
                        if msg_id not in self.processed_messages:
                            text_lower = text.lower()
                            is_urgent = any(kw in text_lower for kw in URGENT_KEYWORDS)
                            messages.append({
                                "text": text,
                                "sender": sender,
                                "id": msg_id,
                                "urgent": is_urgent,
                            })
                            self.processed_messages.add(msg_id)
                    except Exception:
                        continue
                self.logger.info(f"WhatsApp: scan complete — {len(messages)} new urgent message(s)")
            finally:
                browser.close()
        return messages

    def create_action_file(self, message: dict) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        priority = "urgent" if message["urgent"] else "normal"

        content = f"""---
type: whatsapp_message
source: whatsapp
priority: {priority}
received: {datetime.now().isoformat()}
status: pending
---

## WhatsApp Message Received

**From:** {message.get("sender", "Unknown")}
**Priority:** {priority.upper()}
**Received:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Message Preview
{message["text"][:500]}

## Suggested Actions
- [ ] Review full message in WhatsApp
- [ ] Draft a reply (requires human approval before sending)
- [ ] Escalate if payment/invoice related

## Claude's Notes
_Add reasoning and plan here._
"""
        sender_slug = message.get("sender", "unknown").replace(" ", "_")[:20]
        filepath = self.needs_action / f"WHATSAPP_{timestamp}_{sender_slug}.md"
        filepath.write_text(content)
        return filepath

    @staticmethod
    def setup_session():
        """Run once to scan QR code and save session."""
        print("Opening WhatsApp Web — scan the QR code with your phone...")
        SESSION_PATH.mkdir(exist_ok=True)
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                str(SESSION_PATH),
                headless=False,  # must be visible to scan QR
            )
            page = browser.pages[0] if browser.pages else browser.new_page()
            page.goto("https://web.whatsapp.com")
            print("Waiting for you to scan the QR code and WhatsApp to load...")
            page.wait_for_selector('[data-testid="chat-list"]', timeout=120000)
            print("Session saved! You can now run the watcher in headless mode.")
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", action="store_true", help="Run QR code setup")
    args = parser.parse_args()

    if args.setup:
        WhatsAppWatcher.setup_session()
    else:
        if not SESSION_PATH.exists():
            print("No session found. Run with --setup first to scan QR code.")
            sys.exit(1)
        watcher = WhatsAppWatcher()
        watcher.run()
