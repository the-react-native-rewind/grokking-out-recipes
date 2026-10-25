---
name: Never straight to main
description: >-
  Use before making ANY change to a website, app or code repository: every
  change goes on its own branch with a pull request and a preview link for the
  owner to review, and it only goes live (merge or publish) when the owner
  says so.
---
# Never straight to main

Nothing reaches the live site or the main branch without the owner seeing it first.

## The rule
- **Never** commit or push directly to `main` (or `master`, or whatever the production branch is), never force-push it, and never deploy to production as a first step.
- Every change, however small (a typo, a price, a phone number), goes through: **branch → pull request → preview link → owner's yes → merge/publish**.
- The owner's yes must be explicit and about this specific change ("yes, put it live", "approve", "go ahead"). Silence, a thumbs-up on something else, or an old approval doesn't count. If the change is edited after they approved, ask again.

## Steps
1. **Branch.** Create a branch named for the change, e.g. `update-opening-hours`. If a coding agent does the work, tell it to open a pull request and never merge.
2. **Make the change and open a pull request.** Title in plain words ("Update opening hours"). In the description: what changed, why, and anything to check.
3. **Get a preview link.**
   - If the repo is connected to Vercel (or similar), the pull request gets a preview deployment automatically; take its URL from the PR checks or the hosting dashboard.
   - If the site deploys from a folder instead of git, make a preview (not production) deployment. See the Vercel deploy skill.
   - Open the preview yourself first: check the changed page loads and looks right on mobile and desktop.
4. **Ask the owner** in plain language (see the plain-language skill): what changed, the preview link, and one clear question: "Put it live?" with "Yes, publish" / "Not yet" options.
5. **On "yes":** merge the pull request (or promote the preview to production), wait for the live site to update, open the live URL to confirm, then tell the owner it's live with the link.
6. **On "not yet" or changes requested:** keep working on the same branch and pull request, share the new preview link, and ask again.
7. **Log it** in the bot's audit log if one exists (date, what, link, status).

## Exceptions
None by default. If the owner explicitly asks for a different process for a specific project ("just push small text fixes live"), write that down in the project spec and follow it only for that project.

## If something goes wrong after publishing
Roll back to the previous live version first (revert the merge or roll back the deployment), tell the owner what happened in plain words, then fix it on a new branch the normal way.
