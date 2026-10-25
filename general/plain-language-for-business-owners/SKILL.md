---
name: Plain language for business owners
description: >-
  Use whenever you're talking to a non-technical business owner (status
  updates, questions, reports, asking for approval): plain words, no jargon,
  what changed, why it matters, and exactly what they need to do next.
---
# Plain language for business owners

The person you're talking to runs a business, not a codebase. Write the way a helpful person would text them.

## Rules
1. **Lead with the outcome.** First line: what's done or what you need. "Your new opening hours are on the preview site." Not the process.
2. **No jargon.** Swap technical words for everyday ones:
   | Don't say | Say |
   |---|---|
   | PR, pull request, branch, merge | "a draft of the change", "put it live" |
   | deploy, build, push, production | "publish", "put it online", "the live site" |
   | preview deployment, staging | "the preview link" (a private copy only you can review) |
   | DNS, domain records | "pointing your web address at the new site" |
   | API, MCP, connector, webhook | "the connection to <app name>" |
   | bug, regression | "a problem", "something that broke" |
   | repo, commit, CI | leave out entirely |
   If a technical term is unavoidable (they'll see it on screen), explain it once in brackets.
3. **Every update answers three things,** in this order:
   - **What changed:** one or two sentences, in their terms ("The booking button now opens your calendar").
   - **Where to see it:** a link they can tap.
   - **What you need from them:** a clear yes/no or a single choice. If nothing, say "Nothing needed from you."
4. **Short.** Two to five sentences, or a few bullets. No walls of text, no logs, no code, no file paths.
5. **One question at a time.** If you need a decision, give two or three concrete options, not an open "what do you think?".
6. **Money, risk and anything public get spelled out.** Say what it costs, what customers will see, and whether it can be undone.
7. **Problems: say it straight.** What happened, whether anything customers see is affected, and what you're doing about it. No blame, no technical post-mortem unless they ask.
8. **Use their words.** If they call it "the shop page", call it that too. Match their language (reply in Spanish if they write in Spanish).

## Before sending, check
- Would someone with no tech background understand every word?
- Is the ask obvious within the first two lines?
- Is there a link for anything they need to look at?

## Example
Bad: "Opened PR #12 on feat/hours, Vercel preview is green, needs approval to merge to main."
Good: "Your new opening hours are ready to check: [preview link](https://example.vercel.app). It's a private copy, customers can't see it yet. Happy for me to put it live?"
