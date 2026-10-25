---
name: Deploy a site to Vercel
description: >-
  Use when a website or web app needs to go online or be updated on Vercel:
  make a preview deployment, check it, share the preview link for review, and
  on the owner's approval publish it to production and share the live link.
---
# Deploy a site to Vercel

Always preview first, publish second (see the "Never straight to main" skill). The routine or project spec names the Vercel team and project; this recipe is the how.

## 0. Find out how this project deploys
- **Git-connected project** (the Vercel project is linked to a GitHub or Cursor Origin repo): every pull request gets a preview deployment automatically and merging to the production branch publishes. Use the Vercel connector's `get_project` (look at its `link` field) or the repo's PR checks to confirm.
- **Folder-linked project** (a local folder with `.vercel/project.json` holding `projectId`, `orgId`, `projectName`): deploy with the Vercel CLI from that folder (`npx vercel ...`, already signed in on the box; check with `npx vercel whoami`). Never print or copy the CLI's auth files.
- **No project yet:** create one with the CLI (`npx vercel link` then deploy) or the connector's `create_project`. Note: the very first deployment of a new project always goes to production, so for a brand-new client site make sure that first version is safe to be public (or add the no-index header below) before deploying.
- Record the team, project name and production URL in the project spec.

## 1. Before deploying
- Build locally if the project has a build step (`npm run build`) and fix errors first. For static exports, check the output folder (often `out/` or `dist/`) matches the project's Output Directory setting.
- Demo or not-yet-launched sites: keep search engines out with a `vercel.json` header `X-Robots-Tag: noindex, nofollow` on `/(.*)` plus `robots.txt` `Disallow: /`. Remove both when the site really launches.

## 2. Make a preview
- Git-connected: push the branch and open the pull request; wait for the Vercel check to go green, then take the preview URL from the check or from the connector's `list_deployments` (filter by project, newest first).
- Folder-linked: from the project folder run `npx vercel deploy --yes` (add `--scope <team-slug>` if needed). The preview URL is the last line printed. **Do not pass `--prod` here.**
- Check status with `npx vercel inspect <url>` or the connector's `get_deployment`; on an error, read the build output with `list_deployment_events` / `get_runtime_logs` and fix it.

## 3. Check it yourself
- Open the preview URL (or curl it): the home page and every page you changed load, nothing is broken on mobile width, links and forms work.
- **Login wall?** Team previews are often protected by Vercel Authentication, so the owner would see a Vercel sign-in page. Make a shareable link with the connector's `get_access_to_vercel_url` (link expires in about 23 hours; make a fresh one if they come back later), or ask the owner whether to turn protection off for previews. Never change protection settings without asking.

## 4. Share the preview
Send the owner, in plain words: what changed, the preview link as a markdown link, and one question: publish now or not yet. If the chat supports it, use the "Publish / view buttons for Vercel links" skill for the message format.

## 5. Publish (only after the owner's explicit yes)
- Git-connected: merge the pull request; Vercel builds production from the production branch.
- Folder-linked: either run `npx vercel deploy --prod --yes` from the same folder (only if nothing in it changed since the approved preview), or promote the approved preview: `npx vercel promote <preview-url> --yes` (then `npx vercel promote status`). Promoting a preview triggers a fresh production build with production environment variables, so re-check the live site afterwards.
- The connector's `request_promote` (projectId + deploymentId) promotes an existing deployment to production without rebuilding; use it for a production-target deployment that hasn't been assigned to the domain yet (a staged build) or to go back to an earlier production deployment.
- Open the production URL, confirm the change is there, then send the owner the live link.

## 6. If production breaks
Roll back first, fix second: `npx vercel rollback <previous-production-url>` or the connector's `request_rollback`. (Hobby plans can only roll back to the immediately previous production deployment.) Tell the owner in plain words, then fix on a new branch/preview as normal.

## 7. Domains
Connecting a custom domain (`add_project_domain`, DNS changes) or buying one (`buy_domain`) affects the live business and may cost money: always get the owner's explicit yes first, and tell them what it costs.

## 8. Log
Add an audit-log entry for each preview and each publish: date, what changed, preview or live link, status (Preview ready / Published / Rolled back).
