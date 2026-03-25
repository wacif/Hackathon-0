"""
Orchestrator — Silver Tier
Master process that:
1. Runs all watchers in parallel background threads
2. Watches /Approved folder for human-approved actions and triggers them
3. Runs scheduled tasks (daily briefing at 8 AM, weekly audit on Sunday)

Usage:
    uv run python orchestrator.py

Stop with Ctrl+C.
"""

import os
import sys
import time
import shutil
import logging
import threading
import subprocess
from pathlib import Path
from datetime import datetime

import schedule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("Orchestrator")

VAULT_PATH = Path("/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault")
PROJECT_PATH = Path(__file__).parent
SILVER_PATH = PROJECT_PATH
APPROVED = VAULT_PATH / "Approved"
REJECTED = VAULT_PATH / "Rejected"
DONE = VAULT_PATH / "Done"


# ── Watcher threads ──────────────────────────────────────────────────────────

def run_filesystem_watcher():
    logger.info("Starting filesystem watcher thread...")
    from watchers.base_watcher import VAULT_PATH as VP
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "filesystem_watcher", SILVER_PATH / "filesystem_watcher.py"
    )
    mod = importlib.util.load_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()


def run_gmail_watcher():
    credentials = SILVER_PATH / "credentials.json"
    if not credentials.exists():
        logger.warning("Gmail watcher skipped — credentials.json not found.")
        logger.warning("See watchers/gmail_watcher.py for setup instructions.")
        return
    logger.info("Starting Gmail watcher thread...")
    from watchers.gmail_watcher import GmailWatcher
    GmailWatcher().run()


def run_whatsapp_watcher():
    session = SILVER_PATH / "whatsapp_session"
    if not session.exists():
        logger.warning("WhatsApp watcher skipped — no session found.")
        logger.warning("Run: uv run python watchers/whatsapp_watcher.py --setup")
        return
    logger.info("Starting WhatsApp watcher thread...")
    from watchers.whatsapp_watcher import WhatsAppWatcher
    WhatsAppWatcher().run()


# ── Approval watcher ─────────────────────────────────────────────────────────

def watch_approvals():
    """
    Watches /Approved folder. When a file appears:
    - EMAIL approvals → triggers email-mcp send_approved_email
    - Other approvals → logs for Claude to handle on next /process-inbox run
    """
    logger.info("Approval watcher running...")
    seen = set()
    while True:
        try:
            for f in APPROVED.iterdir():
                if f.name == ".gitkeep" or f.name in seen:
                    continue
                seen.add(f.name)
                logger.info(f"Approved action detected: {f.name}")

                if f.name.startswith("APPROVAL_EMAIL_"):
                    logger.info(f"Triggering email send for: {f.name}")
                    subprocess.run(
                        ["node",
                         str(SILVER_PATH / "mcp-servers/email-mcp/index.js"),
                         "--send", f.name],
                        check=False,
                    )
                else:
                    # Move to Done so Claude can see it on next run
                    dest = DONE / f.name
                    shutil.copy2(f, dest)
                    f.unlink()
                    logger.info(f"Approval moved to Done: {f.name}")
        except Exception as e:
            logger.error(f"Approval watcher error: {e}")
        time.sleep(5)


# ── Scheduled tasks ───────────────────────────────────────────────────────────

def run_daily_briefing():
    logger.info("Running scheduled daily briefing...")
    subprocess.run(
        ["claude", "--print", "/daily-briefing"],
        cwd=str(SILVER_PATH),
        check=False,
    )


def run_process_inbox():
    logger.info("Running scheduled inbox processing...")
    subprocess.run(
        ["claude", "--print", "/process-inbox"],
        cwd=str(SILVER_PATH),
        check=False,
    )


def setup_schedule():
    schedule.every().day.at("08:00").do(run_daily_briefing)
    schedule.every(30).minutes.do(run_process_inbox)
    logger.info("Schedule set: daily briefing at 08:00, inbox check every 30 min")


def run_scheduler():
    setup_schedule()
    while True:
        schedule.run_pending()
        time.sleep(30)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    logger.info("=" * 60)
    logger.info("AI Employee Orchestrator starting...")
    logger.info(f"Vault: {VAULT_PATH}")
    logger.info("=" * 60)

    threads = [
        threading.Thread(target=run_filesystem_watcher, name="FilesystemWatcher", daemon=True),
        threading.Thread(target=run_gmail_watcher, name="GmailWatcher", daemon=True),
        threading.Thread(target=run_whatsapp_watcher, name="WhatsAppWatcher", daemon=True),
        threading.Thread(target=watch_approvals, name="ApprovalWatcher", daemon=True),
        threading.Thread(target=run_scheduler, name="Scheduler", daemon=True),
    ]

    for t in threads:
        t.start()
        logger.info(f"Thread started: {t.name}")

    logger.info("All systems running. Press Ctrl+C to stop.")
    try:
        while True:
            alive = [t.name for t in threads if t.is_alive()]
            logger.info(f"Active threads: {', '.join(alive)}")
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Orchestrator shutting down...")


if __name__ == "__main__":
    main()
