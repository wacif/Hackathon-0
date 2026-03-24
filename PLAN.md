# Bronze Tier Plan: Personal AI Employee

> Full plan lives in the Obsidian vault:
> `/media/wasi/mydata/Obsidian Vaults/AI Vault/Plans/Bronze_Tier_Plan.md`



## Goal
Build a Minimum Viable AI Employee:
- Obsidian vault with Dashboard.md and Company_Handbook.md
- One working Watcher script (filesystem monitoring)
- Claude Code reading from and writing to the vault
- Folder structure: /Inbox, /Needs_Action, /Done
- All AI functionality implemented as Agent Skills

---

## Dependency Status

| Tool | Required | Status |
|------|----------|--------|
| Claude Code | ✅ | ✅ Installed (v2.1.81) |
| Python 3.13+ | ✅ | ⚠️ Have 3.12.3 (close enough, works fine) |
| Node.js v24+ | ✅ | ✅ Installed (v24.11.1) |
| uv (Python pkg mgr) | ✅ | ✅ Installed (v0.9.3) |
| Obsidian | ✅ | ✅ Already installed |
| git | ✅ | ✅ Installed (v2.43.0) |
| watchdog (Python pkg) | ✅ | ❌ Not installed — need to install |
| google-auth (Python pkg) | Optional (Silver) | ❌ Not installed — skip for Bronze |

---

## Bronze Tier Steps

### Phase 1: Project Setup
- [x] Initialize git repo
- [x] Create .gitignore
- [ ] Set up UV Python project
- [ ] Create project folder structure

### Phase 2: Obsidian Vault Structure
Create `AI_Employee_Vault/` with these folders and files:
```
AI_Employee_Vault/
├── Dashboard.md          ← Real-time summary
├── Company_Handbook.md   ← Rules of Engagement
├── Inbox/                ← Raw drops land here
├── Needs_Action/         ← Watcher writes here
├── In_Progress/          ← Claude moves tasks here
├── Done/                 ← Completed tasks
└── Logs/                 ← Audit trail
```

### Phase 3: Python Watcher (Filesystem)
- Install `watchdog` via uv
- Implement `filesystem_watcher.py` using the BaseWatcher pattern
- Watcher monitors `AI_Employee_Vault/Inbox/` for new files
- On new file → creates a `.md` action item in `Needs_Action/`

### Phase 4: Agent Skills (Claude Code)
Implement these as Claude Code skills in `.claude/`:
- `/process-inbox` — scan Needs_Action, reason, create Plan.md, move to In_Progress
- `/daily-briefing` — read Dashboard.md, summarize status, update it

### Phase 5: CLAUDE.md (Employee Handbook binding)
Create `CLAUDE.md` that instructs Claude to:
- Always read `Company_Handbook.md` before acting
- Never delete files — move to /Done instead
- Write audit log entry for every action taken

### Phase 6: Test End-to-End
1. Drop a test file into `AI_Employee_Vault/Inbox/`
2. Watcher detects it → creates `Needs_Action/FILE_test.md`
3. Run `/process-inbox` skill → Claude reads, creates plan, moves to Done
4. Verify audit log entry created

---

## What We're Skipping (Bronze scope)
- Gmail/WhatsApp watchers (Silver tier)
- MCP servers (Silver tier)
- Human-in-the-loop approval flow (Silver tier)
- Ralph Wiggum loop (Gold tier)
- Scheduling/cron (Silver tier)

---

## Install Commands (to run next)
```bash
cd /media/wasi/mydata/Hackathons/AutonomousFTEs
uv init
uv add watchdog
```
