---
name: Email sequences end to end
description: >-
  Use when someone wants an email sequence (welcome, lead-magnet follow-up,
  onboarding, nurture, win-back, launch): plan it, write the copy in plain
  language, show it for review, then set it up on a review page or in a mail
  tool. Nothing is ever sent, scheduled or switched on without the owner's yes.
---
# Email sequences end to end

Three stages: **draft → preview → deploy**. Do them in order. Each stage ends with something the owner can look at.

## The one rule
**Nothing is sent, scheduled, activated or published without the owner's explicit yes for that specific step.** That includes test sends, switching an automation on, importing contacts, creating API keys and putting a signup form live. "Looks good" on the copy is not a yes to send. Ask separately, name the action ("Switch on the welcome sequence for new signups?"), and wait. If you're unsure whether you have a yes, you don't.

## 1. Draft

### a) Get the brief (ask only for what's missing)
- **Goal:** the one thing the sequence should achieve (book a call, buy, start using the product, come back).
- **Audience and trigger:** who gets it and what starts it (signed up for a free guide, bought, went quiet for 60 days).
- **Cadence and length:** default 5–7 emails over about 2 weeks, most frequent at the start (day 0, 2, 4, 6, 8, 11, 14).
- **Offer and links:** the main call to action, plus any booking, payment or resource links. Missing links become clearly marked placeholders.
- **Sender:** from-name, from-address, reply-to, and which domain it sends from.
- **Proof:** real examples, numbers or customer stories the owner is happy to share. Never invent results.

### b) Outline first
Show a table before writing any copy, and get a quick OK on it:

| # | Day | Subject | Purpose (one line) | CTA |
|---|---|---|---|---|

Shape that works for most lead-magnet and nurture sequences: deliver what was promised immediately, then give value, then **one** soft ask, then more value. Not every email should sell.

### c) Write the copy
- Plain language. Short sentences. Write like a person, not a brand. Confident, no hype.
- **Subject:** under ~45 characters, specific, no clickbait or ALL CAPS. Add a **preheader** (the preview line) that adds to the subject instead of repeating it.
- **One point and one call to action per email.** One main link; extra links only if they serve the same goal.
- **Length:** most emails 60–150 words. The delivery email can be shorter.
- Sign off as a real person. Invite replies.
- Every email has a footer with the sender's postal address (or what local law requires) and an unsubscribe link. Leave a placeholder if the details aren't known yet.
- Mark anything assumed as `[PLACEHOLDER: …]` and list them in your reply.
- Save each email as its own file (e.g. `emails/01-welcome.md`) with subject, preheader, body and CTA, plus one `sequence` file holding the outline. Turn it into email-safe HTML only once the words are approved, or when the review step needs it.

## 2. Preview (always, before any setup)
Pick the lightest option that lets the owner read every email as recipients will see it:
1. **Review page on the project's own site** (default when there is a site). Follow the *Email sequence preview* skill: real HTML, each email full-bleed at a stable path like `/sequences/<slug>/`, published via branch → pull request → preview link. Don't create a separate project just for previews.
2. **A sequence preview/editor app** the owner already uses, if one is connected. Open the sequence there and pull back any edits they make.
3. **In chat**, for a quick first pass: the outline table plus each email's subject, preheader and body.

In your reply, give the outline, the preview link, the list of placeholders, and one clear question ("Happy with the words, or what should change?"). Edits go back into the same files and the same preview path.

## 3. Deploy (only after the copy is approved)
Pick one target with the owner.

### Option A: review page only
The sequence lives on the site for review or sharing (e.g. as a "sample emails" page). Publish it the project's normal way: pull request → preview → publish only on the owner's yes.

### Option B: into a mail tool (e.g. Resend, or a newsletter platform)
1. **Look before you touch (read-only).** List what already exists: sending domains and whether they're verified, lists/segments/audiences, templates, automations, topics or unsubscribe groups. Reuse what fits. Don't rename or change anything that belongs to another project.
2. **Sending domain.** It must be a domain the owner controls, verified in the tool (the DNS records come from the tool). A subdomain such as `mail.<domain>` keeps reputation separate. Without a verified domain there's no sending: stop and say so.
3. **Where signups go.** One list/segment (or tag) per sequence or source, with a clear name.
4. **Signup capture.** Either the platform's own form, or a small serverless function on the site (e.g. `/api/subscribe`) that validates the email, adds the contact to the list, and fires the event that starts the sequence. API keys go only in the host's environment variables: never in code, chat or files. Creating a key is the owner's call. Add basic spam protection (a hidden honeypot field, rate limit). Decide with the owner whether to use double opt-in (a confirmation email), as some countries require it.
5. **Templates.** One per email, built from the approved copy, with the footer and unsubscribe link.
6. **Automation, built switched off.** Trigger (signup event) → send email 1 → wait → send email 2 → … Set from, subject and reply-to on every send step. Create it **disabled/draft**.
7. **Test.** Ask before any test send, and send it only to an address the owner names. Check links, images, the unsubscribe link and how it looks on a phone.
8. **Go live, only on a yes.** Ask: "Switch it on? From now on, everyone who signs up will get these emails automatically." Then enable it, put the signup form live through the site's normal review flow, and confirm with one real signup the owner makes themselves.
9. **Record it:** what was created, where, and its on/off state, in the project's notes or audit log.

Newsletter platforms (MailerLite, Kit, Mailchimp and similar) follow the same steps under different names: form → group/tag → automation/workflow → paused until approved.

## Never
- Send, schedule or switch on without a specific yes.
- Email people who didn't sign up, or import a list without the owner confirming they have permission.
- Invent results, testimonials or prices.
- Put keys or secrets in code, chat or files.
- Edit or reuse another project's templates, segments or automations without asking.
