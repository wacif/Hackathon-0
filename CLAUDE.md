# AI Employee — Claude Code Configuration

## Vault Location
All work happens inside:
```
/media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/
```

## Before Every Task
1. Read `/media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Company_Handbook.md`
2. Check `/media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Needs_Action/` for pending items
3. Never delete files — move to `/Done` instead
4. Always append an entry to `/Logs/YYYY-MM-DD.md` after acting
5. Update `Dashboard.md` after every run

## Folder Shortcuts
- **Inbox:** `/media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Inbox`
- **Needs_Action:** `/media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Needs_Action`
- **In_Progress:** `/media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/In_Progress`
- **Done:** `/media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Done`
- **Logs:** `/media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Logs`
- **Briefings:** `/media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Briefings`

## Skills

### /process-inbox
Scan all files in `/Needs_Action/`, reason about each one, create a plan, move the task to
`/In_Progress/`, execute what is possible within Bronze tier permissions, then move to `/Done/`.
Write a log entry for each task processed.

### /daily-briefing
Read `Dashboard.md`, count files in each folder, summarize status, and rewrite `Dashboard.md`
with an updated summary. Write a `Briefings/YYYY-MM-DD_Briefing.md` file with the daily report.
