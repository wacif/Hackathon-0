Draft an email reply for a task in Needs_Action or Done, and create a human-in-the-loop approval request.

Steps:

VAULT = /media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault

1. Read $VAULT/Company_Handbook.md.

2. If a filename argument was provided, read that specific file from $VAULT/Needs_Action/.
   Otherwise list files in $VAULT/Needs_Action/ and pick the most recent FILE_ file that contains email content.

3. Read the email content carefully — sender, subject, full body.

4. Draft a professional reply that:
   - Addresses the sender's request directly
   - Is concise and friendly
   - Does NOT commit to anything you're unsure about
   - Asks for clarification if needed

5. Use the `draft_email` MCP tool to create an approval request in $VAULT/Pending_Approval/:
   - to: the sender's email address
   - subject: Re: <original subject>
   - body: your drafted reply
   - reason: brief explanation of why this reply is appropriate

6. Write a log entry in $VAULT/Logs/<today-date>.md:
   ```
   ## <HH:MM> — draft-reply
   - Drafted reply to: <sender>
   - Subject: <subject>
   - Approval file created in Pending_Approval/
   - Action required: Move approval file to /Approved to send, /Rejected to cancel
   ```

7. Update $VAULT/Dashboard.md:
   - Update the Pending Approval count
   - Add a warning callout to "Notes for Human" flagging the pending email approval
