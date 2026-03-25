Process all pending items in the AI Employee vault's Needs_Action folder.

Follow these steps exactly:

1. Read /media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Company_Handbook.md to confirm current rules.

2. List all .md files in /media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Needs_Action/ (skip .gitkeep).

3. If no files found, update Dashboard.md with "Needs_Action is clear" and stop.

4. For each .md file found:
   a. Read the file to understand the task.
   b. Move it to In_Progress/ by copying then deleting the original.
   c. Reason about what action is needed.
   d. Within Bronze tier permissions (no external APIs, no deleting files):
      - Write a brief analysis and plan directly into the file
      - If the task is completable (e.g. summarize, analyze, organize), do it
      - If the task requires Silver/Gold tier capabilities, note that clearly
   e. Move the completed file from In_Progress/ to Done/.

5. Append a log entry to /media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Logs/<today-date>.md
   in this format:
   ```
   ## <HH:MM> — process-inbox
   - Files processed: <count>
   - Files moved to Done: <count>
   - Notes: <any issues or observations>
   ```

6. Update /media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Dashboard.md:
   - Set "Last updated" to today's date and time
   - Update the Inbox Summary counts
   - Add the most recent action to "Recent Actions"
