# Silver Tier — Functional AI Assistant

Builds on Bronze. Adds real integrations: Gmail, WhatsApp, LinkedIn, email sending, human-in-the-loop approvals, and scheduled automation.

---

## What's New in Silver

| Feature | Description |
|---------|-------------|
| Gmail Watcher | Monitors Gmail for important emails → drops to Needs_Action |
| WhatsApp Watcher | Monitors WhatsApp Web for urgent messages → drops to Needs_Action |
| Email MCP Server | Gives Claude hands to draft + send emails (with approval) |
| LinkedIn Auto-Poster | Generates and posts business updates (with approval) |
| Human-in-the-Loop | Sensitive actions wait in Pending_Approval for your review |
| Orchestrator | Single command to run all watchers + approval watcher + scheduler |
| Cron Scheduling | Daily briefing at 8 AM, inbox processed every 30 min |

---

## Vault
```
/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/
├── Dashboard.md
├── Company_Handbook.md
├── Inbox/             ← drop files here
├── Needs_Action/      ← watchers write here
├── In_Progress/       ← Claude claims tasks here
├── Done/              ← completed tasks
├── Logs/              ← daily audit trail
├── Briefings/         ← daily reports
├── Plans/             ← Claude's multi-step plans
├── Pending_Approval/  ← awaiting your review
├── Approved/          ← move here to execute
└── Rejected/          ← move here to cancel
```

---

## Setup

### 1. Install dependencies
```bash
# From project root
uv sync

# Install Playwright browser (for WhatsApp)
uv run playwright install chromium
```

### 2. Gmail Watcher setup
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create project → Enable Gmail API
3. Create OAuth 2.0 credentials → Download as `silver/credentials.json`
4. Run once to authenticate:
   ```bash
   uv run python silver/watchers/gmail_watcher.py
   ```

### 3. WhatsApp Watcher setup
```bash
# Run once to scan QR code with your phone
uv run python silver/watchers/whatsapp_watcher.py --setup
```

### 4. Email MCP Server setup
1. Enable 2FA on Gmail
2. Go to [App Passwords](https://myaccount.google.com/apppasswords) → create one for "Mail"
3. Copy `silver/.env.example` to `silver/.env` and fill in credentials:
   ```bash
   cp silver/.env.example silver/.env
   ```
4. Register MCP with Claude Code — add contents of `silver/mcp-config.json` to:
   ```
   ~/.claude/claude_code_config.json
   ```

### 5. LinkedIn setup
```bash
uv run python silver/linkedin_poster.py --auth
```

---

## Running Silver Tier

### Option A — Run everything (recommended)
```bash
uv run python silver/orchestrator.py
```
This starts all watchers, approval watcher, and scheduler in parallel.

### Option B — Run components individually
```bash
# Filesystem watcher only
uv run python silver/filesystem_watcher.py

# Gmail watcher only
uv run python silver/watchers/gmail_watcher.py

# WhatsApp watcher only
uv run python silver/watchers/whatsapp_watcher.py
```

### Claude Code skills (in new terminal)
```bash
cd /media/wasi/mydata/Hackathons/AutonomousFTEs/silver
claude
```
Then use:
- `/process-inbox` — process all pending tasks
- `/daily-briefing` — generate daily report
- `/draft-reply` — draft email reply for latest email task
- `/post-linkedin` — generate + queue LinkedIn post

---

## Human-in-the-Loop Approval Flow

```
Claude detects action needed (e.g. send email)
         ↓
Writes APPROVAL_EMAIL_<timestamp>.md to Pending_Approval/
         ↓
You see it in Obsidian
         ↓
Move to /Approved  →  Orchestrator sends the email
Move to /Rejected  →  Orchestrator archives it, no action taken
```

---

## Architecture

```
orchestrator.py
├── Thread: filesystem_watcher.py   (watches Inbox/)
├── Thread: gmail_watcher.py        (polls Gmail every 2 min)
├── Thread: whatsapp_watcher.py     (polls WhatsApp Web every 30s)
├── Thread: approval_watcher        (watches Approved/ folder)
└── Thread: scheduler               (daily briefing 8AM, inbox every 30min)
         ↓
All watchers write to Needs_Action/
         ↓
Claude (triggered by you or scheduler) runs /process-inbox
         ↓
Sensitive actions → Pending_Approval/ → you approve → Orchestrator executes
```
