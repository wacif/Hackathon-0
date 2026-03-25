Draft an email reply for a task in Needs_Action or Done, and create a human-in-the-loop approval request.

Steps:

1. Read /media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Company_Handbook.md.

2. If a filename argument was provided, read that specific file. Otherwise list files in Needs_Action/ and pick the most recent EMAIL_ file.

3. Read the email content carefully — sender, subject, full preview.

4. Draft a professional reply that:
   - Addresses the sender's request directly
   - Is concise and friendly
   - Does NOT commit to anything you're unsure about
   - Asks for clarification if needed

5. Use the email MCP tool `draft_email` to create an approval request file in Pending_Approval/:
   - to: the sender's email address
   - subject: Re: <original subject>
   - body: your drafted reply
   - reason: brief explanation of why this reply is appropriate

6. Write a log entry in /media/wasi/mydata/Obsidian Vaults/AI_Employee_Vault/Logs/<today-date>.md:
   ```
   ## <HH:MM> — draft-reply
   - Drafted reply to: <sender>
   - Subject: <subject>
   - Approval file created in Pending_Approval/
   - Action required: Move approval file to /Approved to send, /Rejected to cancel
   ```

7. Update Dashboard.md — add a "Notes for Human" entry flagging the pending approval.
