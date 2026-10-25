---
name: Fetch business invoices
description: >-
  Use when chasing missing receipts or invoices for a bookkeeping period (e.g. a
  quarter's bank lines with no document). It covers where a supplier's invoice
  usually lives (an inbox, a hosted link or a billing page), how to turn emails
  into PDFs, how to name and file them, and common supplier gotchas.
---
# Fetch business invoices

Read-only chase. Never email suppliers without the owner's yes (draft instead), never pay or buy, and never write into the accountant's shared folder unless the owner says so. Work in a local copy and file into the shared folder at the end.

## Steps
1. **Build the missing list.** Take the period's bank and card lines that have no document: date, merchant text, amount, account or card. Group them by supplier.
2. **Search every connected inbox, one supplier at a time.** Search by supplier name, sender domain and amount, include the bin, and use dates from about 3 days before the period to about 3 days after it.
   - Mail connections usually can't see spam. Say so; don't report "not found" as "doesn't exist".
3. **Turn the email into a PDF.**
   - Keep any PDF attachments. Some billing systems (e.g. Stripe) attach both an *Invoice* and a *Receipt* PDF; merge them into one file (`pdfunite invoice.pdf receipt.pdf out.pdf`).
   - If there's no attachment, save the email itself as a PDF (e.g. headless Chrome `--print-to-pdf`) with From / To / Date / Subject at the top.
   - Check the text (e.g. with `pdftotext`): amount, date, invoice number, who it's addressed to.
4. **Try hosted links.** Many receipt emails link to a hosted invoice page or PDF. These links often sit behind an email click-tracker; open the real link inside it.
5. **Try the supplier's own connection.** If the owner has connected the supplier (or it has a billing API with the right access), use it. If access is refused, ask the owner to reconnect; don't work around it.
6. **Billing-page-only suppliers.** Use the browser on your own computer, one site at a time, with the login saved in the Grok Bot vault.
   - Before asking the owner to sign in, open every sign-in page you need as a tab so they can see them all when they take over the screen.
   - Stop at any phone code, captcha or payment step and add the exact web address to a "needs the owner" list.
   - Downloaded file names can be misleading (start-of-period dates, other currencies); always check the PDF text before filing.
7. **File each document.**
   - Name: the accountant's convention, or by default `YYYY-MM-DD Supplier Amount.pdf`, adding the invoice number when one supplier repeats in a month.
   - File it in the month the money left the bank, unless the accountant says otherwise. Check for duplicates first (compare against what the accountant already has, including last month's folder) and link to their copy rather than saving a second one.
8. **Update the period's bank sheet**, if the accountant uses one: put the document link next to the bank line and mark it green = document linked, yellow = no document needed (transfers, payroll, tax payments), red = still missing. In the comment, say whether it's a real invoice or only proof of payment, and note anything odd.
9. **Check who it's addressed to.** It should show the business's legal name and tax number. Flag invoices addressed to the owner personally or to an old business name, so the owner or accountant can decide what to do.
10. **Report.** Counts found / still missing, why each item is still missing and where you looked, and the "needs the owner" list.

## Common supplier gotchas
Replace these with the owner's own suppliers over time and keep a short note of where each one's invoices arrive.
- **Software subscriptions billed through Stripe:** the receipt email usually has the invoice and receipt PDFs attached. If a month is missing, check the other inboxes, then the supplier's billing page (Stripe customer portals list every invoice).
- **Big platforms (Google Workspace, cloud hosting, domain sellers):** an "invoice available" email, with the full list on the account's billing page. Admin pages often ask the owner to re-enter their password: that's an owner step.
- **Hotels and booking sites:** a booking site's "receipt" or "booking confirmed" email is often proof of payment, not an invoice. The invoice may have to come from the hotel itself; note it and draft a request for the owner.
- **Airlines and train companies:** some email an invoice after booking; others only offer it from "Manage my booking" on their site. Tickets are often addressed to the passenger, so flag that.
- **Online marketplaces (e.g. Amazon):** order and delivery emails are not invoices. Get the invoice from the order page; one card payment can cover several sellers' invoices, so check they add up to the bank line. Check the order was placed on the business account.
- **Phone and internet providers:** the email is often only a "new bill available" notice; download the PDF from the account. Match each bill to the bank payment by amount, not by the service month.
- **Paper invoices (notaries, local services):** ask the owner for a photo and file it from `To sort`.

## Gotchas
- Card amounts for foreign-currency invoices differ by the exchange rate and the bank's card fee. Note it in the comment rather than calling it a mismatch.
- Some file connections create a new file instead of overwriting. When updating a sheet, upload the new one, then move the old one to the bin.
- Never upload working files (your notes, CSVs, reports) to the accountant's folder.
- Never touch, rename or re-file anything the accountant has already filed.
- Tax questions (what's deductible, which box it goes in) are for the accountant: flag them, don't decide them.
