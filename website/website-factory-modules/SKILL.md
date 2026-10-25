---
name: Website factory modules
description: >-
  Use at the start of a website project, or when the owner asks for
  "accounts", "log in", "booking", "a calendar", "a shop" or "selling online",
  to decide which optional modules the site needs (none, Supabase accounts and
  bookings, Shopify shop, or both), explain them in plain words, and load the
  matching recipe.
---
# Website factory modules

Most sites need none of these. Add a module only when the owner needs what it does.

| The owner says | Module | Recipe |
|---|---|---|
| "People should log in", "My account", "members", "save their details" | Accounts | User accounts and bookings with Supabase |
| "Book and pay online", "my own calendar", "deposits" | Bookings | User accounts and bookings with Supabase (+ Stripe) |
| "Sell products", "stock", "shipping", "I already use Shopify" | Shop | Shop with Shopify (headless) |
| A contact form, a menu, opening hours, a simple "book a call" link | No module | Plain site; a booking link or Stripe Payment Link is enough |

## How the modules fit together
- **Supabase** = accounts + bookings + the record of everything a customer has done.
- **Stripe Checkout** = booking payments. Its webhook marks bookings paid in Supabase.
- **Shopify** = products, stock and product checkout. Its orders webhook saves orders in Supabase against the same customer.
- One login only: the Supabase account. Shopify customer accounts stay off.

## Steps
1. Ask the owner (plain words, one question at a time): Do customers need to log in? Do they book time with you? Do you sell physical products?
2. Recommend the smallest set. Say what each costs (check current prices on the providers' pricing pages; don't guess).
3. Load the matching recipe(s) and follow them. Order when both: Supabase first (accounts), then Shopify (shop), then link orders to accounts.
4. Every change follows "Never straight to main". Payments stay in test mode until the owner approves going live.
