# AI Employee — Silver Tier Configuration

## Vault Location
```
/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/
```

## Before Every Task
1. Read `Company_Handbook.md` in the vault
2. Check `Needs_Action/` for pending items
3. Never delete files — move to `/Done` instead
4. Always log every action to `Logs/YYYY-MM-DD.md`
5. Sensitive actions (email, LinkedIn) → write to `Pending_Approval/`, never act directly
6. Update `Dashboard.md` after every run

## Folder Shortcuts
| Name | Path |
|------|------|
| Inbox | `/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/Inbox` |
| Needs_Action | `/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/Needs_Action` |
| In_Progress | `/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/In_Progress` |
| Done | `/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/Done` |
| Logs | `/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/Logs` |
| Briefings | `/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/Briefings` |
| Plans | `/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/Plans` |
| Pending_Approval | `/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/Pending_Approval` |
| Approved | `/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/Approved` |
| Rejected | `/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault/Rejected` |

## Skills

### /process-inbox
Scan all `.md` files in `Needs_Action/`. For each:
1. Move to `In_Progress/` (claim-by-move)
2. Read the original file content
3. Reason about the task — create a `Plans/<task-name>_Plan.md` for complex tasks
4. If it's an email/message needing a reply → use `draft_email` MCP tool to write to `Pending_Approval/`
5. Otherwise execute within Silver permissions
6. Move to `Done/`
7. Log entry + update Dashboard

### /daily-briefing
Count files in all folders. Read today's log. Write `Briefings/YYYY-MM-DD_Briefing.md`.
Update `Dashboard.md` with current status.

### /draft-reply
Read the most recent EMAIL file in `Needs_Action/` (or filename passed as argument).
Draft a professional reply. Use `draft_email` MCP tool to create an approval request in `Pending_Approval/`.
Log the action. Update Dashboard with "Action required: approve email reply".

### /post-linkedin
Read `Dashboard.md` and recent `Done/` items for business context.
Write a professional LinkedIn post (150–300 words + hashtags).
Create approval file in `Pending_Approval/APPROVAL_LINKEDIN_<timestamp>.md`.
Log + update Dashboard.
