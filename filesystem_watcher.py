"""
Filesystem Watcher — Bronze Tier
Monitors Bronze_Tier_Vault/Inbox/ for new files.
On detection, creates a .md action item in Needs_Action/.
"""

import time
import shutil
import logging
from pathlib import Path
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Configuration ---
VAULT_PATH = Path("/media/wasi/mydata/Obsidian Vaults/Bronze_Tier_Vault")
INBOX = VAULT_PATH / "Inbox"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("FilesystemWatcher")


class InboxHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Ignore hidden/temp files
        if source.name.startswith(".") or source.name.startswith("~"):
            return

        logger.info(f"New file detected: {source.name}")
        self._handle_new_file(source)

    def _handle_new_file(self, source: Path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        action_filename = f"FILE_{timestamp}_{source.stem}.md"
        action_path = NEEDS_ACTION / action_filename

        # Copy original file to Needs_Action alongside the .md
        dest_copy = NEEDS_ACTION / f"FILE_{timestamp}_{source.name}"
        shutil.copy2(source, dest_copy)

        # Create the .md action item
        content = f"""---
type: file_drop
original_name: {source.name}
size_bytes: {source.stat().st_size}
detected_at: {datetime.now().isoformat()}
status: pending
---

## New File Dropped

**File:** `{source.name}`
**Received:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Size:** {source.stat().st_size} bytes

## Suggested Actions
- [ ] Review the file contents
- [ ] Determine required action
- [ ] Move to /Done when complete

## Notes
_Claude: add your reasoning and plan here._
"""
        action_path.write_text(content)
        logger.info(f"Action file created: {action_filename}")


def main():
    logger.info(f"Starting Filesystem Watcher")
    logger.info(f"Watching: {INBOX}")
    logger.info(f"Writing actions to: {NEEDS_ACTION}")

    if not INBOX.exists():
        logger.error(f"Inbox folder not found: {INBOX}")
        return

    handler = InboxHandler()
    observer = Observer()
    observer.schedule(handler, str(INBOX), recursive=False)
    observer.start()

    logger.info("Watcher running. Drop files into Inbox/ to trigger. Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping watcher...")
        observer.stop()

    observer.join()
    logger.info("Watcher stopped.")


if __name__ == "__main__":
    main()
