---
name: Publish or view buttons for Vercel links
description: >-
  Use whenever you share a Vercel preview or live link with the owner in chat:
  show a tappable "View" link plus a question widget ("Publish to live" / "Not
  yet") so they can review and approve publishing in one tap, then act on
  their choice.
---
# Publish or view buttons for Vercel links

Grok Bot chat has no custom-button component. The closest thing that works today is two parts in one message: a markdown link (renders as a tappable link) and a question widget whose options come back to you as the owner's reply. Together they behave like "View" and "Publish" buttons.

## Message format (in-app chat)
1. **Text** (plain language, see the plain-language skill):
   - One line on what changed.
   - `[View preview](https://<preview-url>)`, plus `[Current live site](https://<production-url>)` if there is one, so they can compare.
   - If the preview is behind a Vercel login, share the link from the Vercel connector's `get_access_to_vercel_url` instead and mention it works for about a day.
2. **Question widget**, sent right after the text:
   - Prompt names the exact thing: "Publish the new opening hours to your live site?"
   - Options: **Publish to live** / **Not yet**. Turn on custom answers so they can type a change ("make the button bigger").
   - The widget ends your turn. Don't do anything else in that turn.

## Acting on the answer (next turn)
- **Publish to live:** that's the owner's explicit approval for *this* preview only. Publish it the project's normal way (merge the pull request, or promote that exact deployment; see the Vercel deploy skill), open the live URL to check, then reply "It's live: [View live site](https://<production-url>)". Log it.
- **Not yet:** acknowledge in one line, leave everything as is, log "Waiting on owner".
- **A typed change:** make it on the same branch, deploy a new preview, and send a fresh link + widget. The old "Publish" answer no longer counts.
- If anything changed after the widget went out, ask again with a new widget before publishing.

## On outside channels (Slack, WhatsApp, Telegram, etc.)
Widgets don't render there. Send the same text with the links, then the options as a numbered list ("Reply 1 to publish to live, 2 for not yet") and treat their reply the same way.

## Limits to be honest about
- These aren't real buttons: "Publish" works by sending the bot an answer, which starts its next turn. Publishing then takes as long as the merge/build does (usually a minute or two). Say so if they ask.
- A widget answers one question once. For a new preview, send a new widget.
- Links open in the browser; the chat can't embed the site itself.
- If the owner says they can't see the widget (for example on a phone), fall back to the numbered-list version.
