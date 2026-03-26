Generate and post a professional LinkedIn update about the business.

Steps:

VAULT = /media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault

1. Read $VAULT/Company_Handbook.md.

2. Read $VAULT/Dashboard.md to understand current business context.

3. Check $VAULT/Done/ for recently completed tasks that could be turned into a LinkedIn post (e.g. completed projects, client wins, milestones).

4. Write a LinkedIn post that:
   - Is professional and engaging (150–300 words)
   - Highlights a recent win, insight, or update
   - Ends with a call to action or question to encourage engagement
   - Uses 3–5 relevant hashtags

5. Create an approval request file at:
   $VAULT/Pending_Approval/APPROVAL_LINKEDIN_<timestamp>.md

   With this content:
   ```
   ---
   type: approval_request
   action: linkedin_post
   created: <ISO timestamp>
   status: pending
   ---
   ## 💼 LinkedIn Post — Awaiting Approval

   <the post text here>

   ## To Approve
   Move this file to [[Approved/Approved|Approved]]. The orchestrator will post it.

   ## To Reject
   Move this file to [[Rejected/Rejected|Rejected]].
   ```

6. Write a log entry in $VAULT/Logs/<today-date>.md:
   ```
   ## <HH:MM> — post-linkedin
   - Draft created in Pending_Approval/
   - Action required: Approve or reject the post
   ```

7. Update $VAULT/Dashboard.md:
   - Update the Pending Approval count
   - Add a warning callout to "Notes for Human" flagging the pending LinkedIn post
