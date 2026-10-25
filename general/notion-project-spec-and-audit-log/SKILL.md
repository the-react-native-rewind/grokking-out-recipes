---
name: Notion project spec and audit log
description: >-
  Use when setting up a new bot or project, and after any meaningful action:
  keep a Notion project-spec page (goal, scope, decisions, links) and an
  audit-log database (date, action, link, status) so the owner can always see
  what the bot is working on and what it has done.
---
# Notion project spec and audit log

Every bot keeps one home in Notion that the owner can open at any time to understand where things are. The routine or memory names which Notion workspace and parent page to use; this recipe is the structure and the habit.

## Structure (create once per bot)
Under the parent page the owner chose (ask if none is set), create:

```
<Bot name> HQ                      (page)
├── Project spec: <project name>   (one page per project)
└── Audit log                      (database, shared by all projects)
```

### "<Bot name> HQ" page
Short intro in plain words: what this bot does for the business, who it reports to, and links to each project spec and the audit log. Keep it to one screen.

### Project spec page (one per project)
Use these headings, in this order, written in plain language:
1. **Goal**: one or two sentences on what success looks like for the business.
2. **Status**: one line, e.g. "In progress: preview ready for review", plus the date it was last updated.
3. **Scope**: what's included, and an explicit "Not included" list.
4. **Decisions**: a dated list. Each line: date, what was decided, who decided ("Owner approved new prices, 2026-01-15").
5. **Open questions**: things waiting on the owner, each with the date asked.
6. **Links**: live site, preview link, code repository, hosting project, related documents, and the audit log filtered to this project.
7. **How we work**: process rules agreed for this project (e.g. "every change goes through a preview and the owner's approval").

### Audit log database
Properties:
| Property | Type | Notes |
|---|---|---|
| Action | Title | Plain-language summary: "Published new opening hours" |
| Date | Date | When it happened (include time) |
| Project | Select (or Relation to the spec pages) | Which project |
| Type | Select | Change, Preview, Publish, Message, Research, Setup, Fix, Rollback |
| Status | Status/Select | Planned, In progress, Waiting on owner, Done, Failed, Rolled back |
| Link | URL | Preview, live page, pull request, document, etc. |
| Notes | Text | One or two sentences; any problem or follow-up |

Add a default view sorted by Date (newest first) and a board view grouped by Status. Keep it to these columns so it stays easy to read; add more only if the owner asks.

## Setup steps
1. Find or confirm the parent page with the owner (Notion search; never guess between workspaces).
2. Create the HQ page, the audit-log database (Notion create-database with the properties above) and the first project spec page. Link them to each other.
3. Add a first log entry: "Set up project spec and audit log", Type Setup, Status Done.
4. Save the page and database IDs in the bot's memory or routine so future runs write to the same place.
5. Send the owner the HQ link in one plain sentence.

## Ongoing habit
- **Log every meaningful action** as it happens: previews shared, things published, messages sent on the owner's behalf, settings changed, failures and rollbacks. One row per action. Don't log internal busywork (reading files, retries).
- When the status of an action changes (Preview ready → Published), update that row rather than adding a duplicate.
- **Update the spec** when scope changes, a decision is made, or a question is answered: add the dated decision, move answered questions out of Open questions, refresh Status and Links.
- Never record passwords, keys, card numbers or private customer data in Notion.
- If Notion isn't reachable, keep going, note the missed entries, and add them once it's back.
