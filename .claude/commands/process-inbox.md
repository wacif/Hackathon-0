Process all pending items in the AI Employee vault's Needs_Action folder.

VAULT = /media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault

Follow these steps exactly:

1. Read $VAULT/Company_Handbook.md to confirm current rules.

2. List all .md files in $VAULT/Needs_Action/ — skip .gitkeep and Needs_Action.md (the index note).

3. If no files found, update Dashboard.md with "Needs_Action is clear" and stop.

4. For each .md file found:
   a. Read the file to understand the task.
   b. Move it to $VAULT/In_Progress/ (copy then delete original) — this claims the task.
   c. Read the original file content if it was copied alongside the .md.
   d. Reason about what action is needed:
      - If it contains an email or message needing a reply → use the `draft_email` MCP tool
        to create an approval request in $VAULT/Pending_Approval/
      - If it needs a LinkedIn post → create an approval file in $VAULT/Pending_Approval/
        named APPROVAL_LINKEDIN_<timestamp>.md
      - If it's a general task (summarize, analyze, organize) → do it directly
      - Write your reasoning and plan into the file under "## Claude's Notes"
   e. Move the completed file from In_Progress/ to $VAULT/Done/.

5. Append a log entry to $VAULT/Logs/<today-date>.md:
   ```
   ## <HH:MM> — process-inbox
   - Files processed: <count>
   - Files moved to Done: <count>
   - Approvals created: <count>
   - Notes: <any issues or observations>
   ```

6. Update $VAULT/Dashboard.md:
   - Set "Last updated" to today's date and time
   - Update the Inbox Summary counts (Pending, Pending Approval, In Progress, Completed Today)
   - Add the most recent action to the "Recent Actions" table
   - If approvals were created, add a warning callout to "Notes for Human"
