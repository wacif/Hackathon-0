/**
 * Email MCP Server — Silver Tier
 * Gives Claude Code the ability to draft and send emails via Gmail SMTP.
 *
 * Setup required:
 * 1. Enable 2FA on your Google account
 * 2. Go to https://myaccount.google.com/apppasswords
 * 3. Create an App Password for "Mail"
 * 4. Add to .env:
 *    GMAIL_USER=your@gmail.com
 *    GMAIL_APP_PASSWORD=your_16_char_app_password
 *
 * Register in Claude Code:
 * Add to ~/.claude/claude_code_config.json under "mcpServers":
 * {
 *   "email": {
 *     "command": "node",
 *     "args": ["/media/wasi/mydata/Hackathons/AutonomousFTEs/mcp-servers/email-mcp/index.js"],
 *     "env": {
 *       "GMAIL_USER": "your@gmail.com",
 *       "GMAIL_APP_PASSWORD": "your_app_password"
 *     }
 *   }
 * }
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import nodemailer from "nodemailer";
import fs from "fs";
import path from "path";

const VAULT_PATH = "/media/wasi/mydata/Obsidian Vaults/Silver_Tier_Vault";
const PENDING_APPROVAL = path.join(VAULT_PATH, "Pending_Approval");
const APPROVED = path.join(VAULT_PATH, "Approved");

const server = new McpServer({
  name: "email-mcp",
  version: "1.0.0",
});

function getTransporter() {
  return nodemailer.createTransport({
    service: "gmail",
    auth: {
      user: process.env.GMAIL_USER,
      pass: process.env.GMAIL_APP_PASSWORD,
    },
  });
}

function writeLog(action, details) {
  const today = new Date().toISOString().split("T")[0];
  const logFile = path.join(VAULT_PATH, "Logs", `${today}.md`);
  const time = new Date().toTimeString().slice(0, 5);
  const entry = `\n## ${time} — email-mcp: ${action}\n${JSON.stringify(details, null, 2)}\n`;
  fs.appendFileSync(logFile, entry);
}

// Tool 1: Draft an email (writes approval request — does NOT send)
server.tool(
  "draft_email",
  {
    to: z.string().describe("Recipient email address"),
    subject: z.string().describe("Email subject"),
    body: z.string().describe("Email body text"),
    reason: z.string().describe("Why this email needs to be sent"),
  },
  async ({ to, subject, body, reason }) => {
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
    const filename = `APPROVAL_EMAIL_${timestamp}.md`;
    const filepath = path.join(PENDING_APPROVAL, filename);

    const content = `---
type: approval_request
action: send_email
to: ${to}
subject: ${subject}
reason: ${reason}
created: ${new Date().toISOString()}
status: pending
---

## Email Draft — Awaiting Your Approval

**To:** ${to}
**Subject:** ${subject}
**Reason:** ${reason}

## Email Body
${body}

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
`;
    fs.writeFileSync(filepath, content);
    writeLog("draft_email", { to, subject, approval_file: filename });

    return {
      content: [
        {
          type: "text",
          text: `Email draft created and waiting for approval.\nApproval file: Pending_Approval/${filename}\nMove it to /Approved to send, /Rejected to cancel.`,
        },
      ],
    };
  }
);

// Tool 2: Send approved email (only processes files in /Approved)
server.tool(
  "send_approved_email",
  {
    approval_filename: z.string().describe("The approval .md filename from Pending_Approval/"),
  },
  async ({ approval_filename }) => {
    const approved_path = path.join(APPROVED, approval_filename);

    if (!fs.existsSync(approved_path)) {
      return {
        content: [{ type: "text", text: `Error: ${approval_filename} not found in /Approved. Move it there first.` }],
      };
    }

    const content = fs.readFileSync(approved_path, "utf8");

    // Parse frontmatter
    const toMatch = content.match(/^to: (.+)$/m);
    const subjectMatch = content.match(/^subject: (.+)$/m);
    const bodyMatch = content.match(/## Email Body\n([\s\S]+?)(?=\n##|$)/);

    if (!toMatch || !subjectMatch || !bodyMatch) {
      return { content: [{ type: "text", text: "Error: Could not parse approval file." }] };
    }

    const transporter = getTransporter();
    await transporter.sendMail({
      from: process.env.GMAIL_USER,
      to: toMatch[1].trim(),
      subject: subjectMatch[1].trim(),
      text: bodyMatch[1].trim(),
    });

    writeLog("send_email", { to: toMatch[1], subject: subjectMatch[1], file: approval_filename });

    // Move to Done
    const done_path = path.join(VAULT_PATH, "Done", approval_filename);
    fs.renameSync(approved_path, done_path);

    return {
      content: [{ type: "text", text: `Email sent successfully to ${toMatch[1]} and logged.` }],
    };
  }
);

// Tool 3: List pending approvals
server.tool(
  "list_pending_approvals",
  {},
  async () => {
    const files = fs.readdirSync(PENDING_APPROVAL).filter(f => f.endsWith(".md") && f !== ".gitkeep");
    return {
      content: [
        {
          type: "text",
          text: files.length
            ? `Pending approvals:\n${files.map(f => `- ${f}`).join("\n")}`
            : "No pending approvals.",
        },
      ],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
