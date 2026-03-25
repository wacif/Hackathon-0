Generate and post a professional LinkedIn update about the business.

Steps:

1. Read /media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Company_Handbook.md.

2. Read /media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Dashboard.md to understand current business context.

3. Check /media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Done/ for recently completed tasks that could be turned into a LinkedIn post (e.g. completed projects, client wins, milestones).

4. Write a LinkedIn post that:
   - Is professional and engaging (150–300 words)
   - Highlights a recent win, insight, or update
   - Ends with a call to action or question to encourage engagement
   - Uses 3–5 relevant hashtags

5. Create an approval request file at:
   /media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Pending_Approval/APPROVAL_LINKEDIN_<timestamp>.md

   With this content:
   ```
   ---
   type: approval_request
   action: linkedin_post
   created: <ISO timestamp>
   status: pending
   ---
   ## LinkedIn Post — Awaiting Approval

   <the post text here>

   ## To Approve
   Move this file to /Approved. The orchestrator will post it.

   ## To Reject
   Move this file to /Rejected.
   ```

6. Write a log entry in Logs/<today-date>.md:
   ```
   ## <HH:MM> — post-linkedin
   - Draft created in Pending_Approval/
   - Action required: Approve or reject the post
   ```
