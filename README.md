# Personal AI Employee — Autonomous FTEs Hackathon

> **Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

A "Digital FTE" (Full-Time Equivalent) — an AI agent powered by **Claude Code** and **Obsidian**
that proactively manages personal and business tasks 24/7.

---

## Project Structure

```
AutonomousFTEs/                         ← This repo (code & config)
├── .gitignore                          ← Excludes secrets, venv, cache
├── CLAUDE.md                           ← Claude's onboarding doc (auto-read on startup)
├── PLAN.md                             ← Bronze tier development roadmap
├── README.md                           ← You are here
├── filesystem_watcher.py               ← Watches Inbox/, triggers on new files
├── pyproject.toml                      ← Python project config (uv)
└── uv.lock                             ← Exact dependency versions

/media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/   ← AI's workspace (Obsidian)
├── Dashboard.md                        ← Real-time status (Claude updates this)
├── Company_Handbook.md                 ← Rules of engagement for Claude
├── Inbox/                              ← DROP FILES HERE
├── Needs_Action/                       ← Watcher writes action items here
├── In_Progress/                        ← Claude moves tasks here while working
├── Done/                               ← Completed tasks (never deleted)
├── Logs/                               ← Daily audit trail (YYYY-MM-DD.md)
└── Briefings/                          ← Daily/weekly CEO briefings
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   PERCEPTION LAYER                       │
│  You drop a file into Inbox/                            │
│         ↓                                               │
│  filesystem_watcher.py detects it (watchdog/inotify)   │
│         ↓                                               │
│  Creates FILE_<timestamp>_<name>.md in Needs_Action/   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   REASONING LAYER                        │
│  Claude Code reads CLAUDE.md + Company_Handbook.md      │
│         ↓                                               │
│  You run: /process-inbox                               │
│         ↓                                               │
│  Claude reads Needs_Action/, reasons about each item   │
│  Moves task to In_Progress/, creates a plan            │
│  Executes allowed actions, moves to Done/              │
│  Writes log entry + updates Dashboard.md               │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   OUTPUT LAYER                           │
│  Done/ — completed task files                           │
│  Logs/ — audit trail                                    │
│  Dashboard.md — updated status                         │
│  Briefings/ — daily/weekly reports                     │
└─────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Brain | Claude Code (claude-sonnet-4-6) | Reasoning & execution |
| Memory / GUI | Obsidian (local Markdown) | Dashboard & knowledge base |
| Senses | Python + watchdog | File system monitoring |
| Package manager | uv | Fast Python dependency management |
| Version control | git | Code tracking |

---

## Prerequisites

| Tool | Version | Status |
|------|---------|--------|
| Claude Code | Any | Required |
| Python | 3.12+ | Required |
| uv | Any | Required |
| Node.js | v24+ | Required (Silver tier MCP servers) |
| Obsidian | v1.10+ | Required |
| git | Any | Required |

---

## Setup

### 1. Clone the repo
```bash
git clone <repo-url>
cd AutonomousFTEs
```

### 2. Install Python dependencies
```bash
uv sync
```

### 3. Open the vault in Obsidian
- Open Obsidian
- Click the vault switcher icon (bottom left)
- Select "Open folder as vault"
- Navigate to `/media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault`

### 4. Start the filesystem watcher
```bash
uv run python filesystem_watcher.py
```

### 5. Start Claude Code (in a new terminal)
```bash
cd /media/wasi/mydata/Hackathons/AutonomousFTEs
claude
```

---

## Usage

### Dropping a task
1. Make sure the watcher is running (`uv run python filesystem_watcher.py`)
2. Drop any file into:
   ```
   /media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Inbox/
   ```
3. The watcher instantly creates an action item in `Needs_Action/`

### Processing tasks
Inside Claude Code, run:
```
/process-inbox
```
Claude will read all pending items in `Needs_Action/`, reason about each one,
and move them through `In_Progress/` → `Done/`.

### Daily briefing
Inside Claude Code, run:
```
/daily-briefing
```
Claude generates a summary report in `Briefings/` and updates `Dashboard.md`.

---

## Hackathon Tiers

| Tier | Status | Key Features |
|------|--------|-------------|
| **Bronze** | 🔨 In Progress | Vault setup, filesystem watcher, Claude skills |
| **Silver** | ⏳ Planned | Gmail + WhatsApp watchers, MCP server, LinkedIn posting |
| **Gold** | ⏳ Planned | Odoo accounting, CEO briefing, Ralph Wiggum loop |
| **Platinum** | ⏳ Planned | 24/7 cloud VM, Cloud+Local split, A2A messaging |

---

## Security

- **Never commit `.env` files** — the `.gitignore` protects you, but stay aware
- **Credentials** go in `.env` (Silver tier) — use environment variables only
- **The vault is local-only** — no data leaves your machine in Bronze tier
- **Claude cannot delete files** — only move to `/Done` (enforced via `Company_Handbook.md`)
- **Audit trail** — every Claude action is logged in `Logs/YYYY-MM-DD.md`

---

## File Lifecycle

```
Inbox/file.txt
    → Needs_Action/FILE_20260325_120000_file.md   (watcher creates)
    → In_Progress/FILE_20260325_120000_file.md    (Claude claims)
    → Done/FILE_20260325_120000_file.md           (Claude completes)
```

Files are **never deleted** — only moved forward in the pipeline.

---

## Research & Community

Weekly Research Meeting every Wednesday at 10:00 PM on Zoom.
YouTube: [Panaversity](https://www.youtube.com/@panaversity)
