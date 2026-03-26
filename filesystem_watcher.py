"""
Filesystem Watcher — Bronze Tier
Monitors Bronze_Tier_Vault/Inbox/ for new files.
On detection:
  1. Creates a .md action item in Needs_Action/
  2. Auto-updates Dashboard.md with live counts
"""

import re
import time
import shutil
import logging
from pathlib import Path
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Configuration ---
VAULT_PATH = Path("/media/wasi/mydata/Obsidian Vaults/Bronze_Tier_Vault")
INBOX       = VAULT_PATH / "Inbox"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
IN_PROGRESS  = VAULT_PATH / "In_Progress"
DONE         = VAULT_PATH / "Done"
DASHBOARD    = VAULT_PATH / "Dashboard.md"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("FilesystemWatcher")


def count_md_files(folder: Path) -> int:
    """Count .md files in a folder, ignoring .gitkeep."""
    if not folder.exists():
        return 0
    return len([f for f in folder.iterdir() if f.suffix == ".md" and f.name != ".gitkeep"])


def update_dashboard():
    """Rewrite the live counts in Dashboard.md after every file event."""
    if not DASHBOARD.exists():
        return

    pending    = count_md_files(NEEDS_ACTION)
    in_progress = count_md_files(IN_PROGRESS)
    completed  = count_md_files(DONE)
    now        = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = DASHBOARD.read_text()

    # Update last_updated in frontmatter
    content = re.sub(r"last_updated:.*", f"last_updated: {datetime.now().strftime('%Y-%m-%d')}", content)

    # Update the "Last updated" line in the callout
    content = re.sub(
        r"Last updated: \*\*.*?\*\*",
        f"Last updated: **{now}**",
        content
    )

    # Update the three pipeline counts line-by-line (robust against wikilink escapes)
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if "📬 Pending" in line and "|" in line:
            lines[i] = re.sub(r"\|\s*\d+\s*\|?\s*$", f"| {pending} |", line)
        elif "⚙️ In Progress" in line and "|" in line and "[[" not in line:
            lines[i] = re.sub(r"\|\s*\d+\s*\|?\s*$", f"| {in_progress} |", line)
        elif "✅ Completed Today" in line and "|" in line:
            lines[i] = re.sub(r"\|\s*\d+\s*\|?\s*$", f"| {completed} |", line)
    content = "\n".join(lines)

    DASHBOARD.write_text(content)
    logger.info(f"Dashboard updated — Pending: {pending}, In Progress: {in_progress}, Done: {completed}")


class InboxHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        if source.name.startswith(".") or source.name.startswith("~"):
            return
        logger.info(f"New file detected: {source.name}")
        self._handle_new_file(source)

    def on_modified(self, event):
        # Catches the case where a file with same name is overwritten (re-dropped)
        if event.is_directory:
            return
        source = Path(event.src_path)
        if source.name.startswith(".") or source.name.startswith("~"):
            return
        # Only treat as new task if no action file exists for this file yet in this second
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        existing = list(NEEDS_ACTION.glob(f"FILE_*_{source.stem}.md"))
        # Check if an action file was created in last 3 seconds to avoid double-processing
        recent = [f for f in existing if f.stat().st_mtime > time.time() - 3]
        if not recent:
            logger.info(f"File modified (re-drop detected): {source.name}")
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
title: {source.stem}
tags:
  - needs-action
  - bronze-tier
  - file-drop
type: file_drop
original_name: {source.name}
size_bytes: {source.stat().st_size}
detected_at: {datetime.now().isoformat()}
status: pending
---

## 📥 New File Dropped

**File:** `{source.name}`
**Received:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Size:** {source.stat().st_size} bytes

## Suggested Actions
- [ ] Review the file contents
- [ ] Determine required action
- [ ] Move to [[Done/|Done]] when complete

## Claude's Notes
_Add reasoning and plan here._
"""
        action_path.write_text(content)
        logger.info(f"Action file created: {action_filename}")

        # Auto-update dashboard immediately
        update_dashboard()


def main():
    logger.info("Starting Filesystem Watcher [Bronze Tier]")
    logger.info(f"Watching:          {INBOX}")
    logger.info(f"Writing actions to: {NEEDS_ACTION}")

    if not INBOX.exists():
        logger.error(f"Inbox folder not found: {INBOX}")
        return

    # Update dashboard on startup to reflect current state
    update_dashboard()

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
