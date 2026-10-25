# Grokking Out recipes

Recipes are step-by-step instructions for your Grok Bot. Each one teaches your bot how to do one job for your business well, such as putting your website online, setting up your newsletter or keeping your invoices in order.

These recipes go with the guides at [grokkingout.com](https://grokkingout.com/guides/). You don't need to read them yourself. Your bot reads them and follows them.

## How to add them to your bot

Copy the message below and send it to your main Grok Bot. It adds every recipe, then checks for updates every Monday morning and tells you what changed.

```
Hi! Please install the Grokking Out recipes as skills, and keep them up to date.

1. Open this list: https://raw.githubusercontent.com/the-react-native-rewind/grokking-out-recipes/main/recipes.json
2. For each recipe in the list, open its "url" link. Save that file so you can follow it later, as one of your skills: use the name and description at the top of the file, and the rest of the file as the steps. Keep the wording exactly as it is. If you already have a skill with the same name, update it instead of making a second one.
3. Make a note of the version number of each recipe you saved.
4. Set up a routine that runs every Monday at 9am in my time zone. Each time, open the same list, compare each recipe's version with the one you saved, and update any recipe that has changed. Add any new recipes too. Then send me a short message in plain words saying what changed. If nothing changed, you don't need to message me. If a recipe disappears from the list, ask me before you delete anything.
5. Only install recipes from this list. When you're done, tell me how many recipes you installed and when the first weekly check will run.
```

You only need to do this once. Your other bots can use the recipes too.

## What's included

### General (every bot)
| Recipe | What it's for |
|---|---|
| Plain language for business owners | Your bot talks to you in plain words: what changed, where to see it, and what it needs from you. |
| Never straight to main | Every change to your website gets a private preview link first, and only goes live when you say yes. |
| Notion project spec and audit log | Optional. A Notion page with the project plan and a list of everything your bot has done. |

### Website
| Recipe | What it's for |
|---|---|
| Website factory modules | Works out whether your website needs customer log-in, bookings or a shop, and picks the right recipe. |
| Deploy a site to Vercel | Puts your website online: preview first, publish when you say yes, and undo if something breaks. |
| Publish or view buttons for Vercel links | Sends you a "View" link and a simple "Publish to live / Not yet" question. |
| User accounts and bookings with Supabase | Customer log-in, a booking calendar and paid bookings. |
| Shop with Shopify (headless) | Sells your products on your own website, with Shopify looking after stock and payment. |

### Email
| Recipe | What it's for |
|---|---|
| Email Factory | Emails from your website, a newsletter, welcome emails and help with your inbox. |
| Email sequences end to end | Plans, writes and sets up a series of emails. Nothing is sent without your yes. |
| Email sequence preview | Shows you draft emails on a private page of your own website, so you can read them first. |
| Prepare newsletter email media | Gets the pictures in your newsletter the right size so the email loads quickly. |

### Accounting
| Recipe | What it's for |
|---|---|
| Accounting Factory | Keeps your invoices, receipts and bank statements complete and tidy for your accountant. |
| Fetch business invoices | Tracks down missing invoices and receipts for a month or quarter. |

## Safe by design

Every recipe follows the same rules: your bot asks before anything goes live, gets sent or costs money. It never puts passwords in the chat. Logins and keys are kept in the Grok Bot vault.

## How it's organised

- Each recipe is a folder with one `SKILL.md` file, grouped into `general/`, `website/`, `email/` and `accounting/`.
- `recipes.json` lists every recipe with a one-line description, its version number and a link to the file. Bots use it to install and update recipes.

## For maintainers

1. Edit or add a recipe folder (`<group>/<recipe-id>/SKILL.md`, with `name` and `description` at the top).
2. Run `python3 tools/update-manifest.py`. It refreshes `recipes.json` and raises the version of any recipe that changed, so bots pick up the change at their next weekly check.
3. Keep recipes general: no client names, account details, keys or private links.
