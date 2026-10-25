---
name: Email sequence preview
description: >-
  Use when building or reviewing an email sequence for whatever project is being
  deployed — publish a review path on that same site/app, not a fixed host or a
  new Vercel project.
---
# Build and preview an email sequence

Use when someone asks to build, draft, redesign, or review a lifecycle / welcome / onboarding (or similar) email sequence and wants to **look at it** before it goes to a mail provider.

## Goal

Draft **real HTML emails** and put a **reviewable path on whatever project is being deployed for that ask** — then return that URL. Edits stay in chat; republish the same path.

This is a **generic workflow**. It is not tied to a fixed domain or a dedicated email-previews site.

## Host = the thing you’re building

The sequence lives on **the same deployment as the work in front of you**:

- “Email sequence for the <client> demo site” → that client’s existing Vercel/app deploy (e.g. `/sequences/[slug]` or `public/sequences/...` in that repo).
- “Welcome emails for <product>” → that product’s site/app.
- Whatever repo/site the conversation is already building.

Do **not** hardcode a host in this skill. Do **not** create a dedicated Vercel project just for email previews unless the user explicitly asks.

## Shape

1. Draft structured sequence + full HTML per email.
2. Publish into **that** project’s codebase under a stable path (prefer `/sequences/[slug]` or static files the existing app already serves).
3. Publish via that project’s normal path (branch + pull request → its preview link; production only on the owner’s yes).
4. Reply with the review URL, a short outline, and that edits are “change X” → republish same slug.

## Sequence contract

```json
{
  "slug": "welcome",
  "title": "Welcome sequence",
  "emails": [
    {
      "id": "confirm",
      "name": "Confirm email",
      "subject": "Confirm your email",
      "html": "<!doctype html>...full email HTML..."
    }
  ]
}
```

- Real HTML (email-client-safe), not field mockups.
- Just the list of emails — no forced arrows or storyboard groups.

## Review page (required)

**Full-bleed email only.** The review URL must show the email HTML edge-to-edge — no left sidebar, no meta panel (from / subject / preheader / audience), no desktop/mobile toggle chrome, no outline chrome around an iframe.

- Prefer serving the email HTML itself at the review path (e.g. `/sequences/[slug]/` or `/sequences/[slug]/email.html` as the link you return).
- If there are several emails in a sequence, a minimal email-to-email switcher is fine **only if** it does not steal layout from the email (e.g. a thin floating control). Default still: open one email full-bleed.
- Put subject, preheader, from, and outline in the **chat reply**, not on the page.
- Keep `sequence.json` (or equivalent) in the project for structure; do not require a chrome-heavy review UI.

## Out of scope unless asked

Sending, Resend sync, audiences, analytics, WYSIWYG overlay, a shared global sequences host, sidebar / split-pane review chrome.

## Success

One link on the **same** deploy as the product/demo, real HTML full-bleed to review, iterate in chat.
