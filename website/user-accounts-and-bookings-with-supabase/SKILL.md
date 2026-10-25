---
name: User accounts and bookings with Supabase
description: >-
  Use when a website needs customer accounts (sign up, log in, "My account"),
  a custom booking calendar, prepaid bookings through Stripe Checkout, or a
  place to keep orders from a shop (e.g. Shopify) against the same customer.
  Covers the Supabase setup, database tables, row level security, the Stripe
  Checkout + webhook flow with idempotency, env vars and safe rollout (test
  mode first, preview first). Pair with "Shop with Shopify (headless)" when the
  site also sells products.
---
# User accounts and bookings with Supabase

Supabase is the site's back office: it owns **customer accounts**, the **booking calendar** and the **record of every booking and order**. Stripe takes the booking money. If the site also has a shop, Shopify holds the stock and runs product checkout, and its orders are copied into Supabase against the same customer (see the Shopify recipe).

## Who owns what (the split)
| Job | Owner |
|---|---|
| Sign up, log in, password reset, "My account" page | Supabase Auth |
| Services, staff, opening hours, bookings | Supabase database |
| Taking payment for a booking | Stripe Checkout (Stripe webhook marks the booking paid) |
| Products, stock, product checkout (optional) | Shopify (orders webhook saves the order in Supabase) |

Rules that keep this simple:
- **One customer identity: the Supabase user.** Do not switch on a second login system (e.g. Shopify customer accounts). Link anything else to the Supabase user by `user_id`, falling back to email.
- **The database is the source of truth for bookings.** A booking is only "paid" when the verified Stripe webhook says so, never because the browser came back to a success page.
- **Prices come from the database, never from the browser.**

## Before you start
- Read the "Never straight to main" recipe: everything below goes branch → pull request → preview → owner's yes → merge.
- Work in **Stripe test mode / a sandbox** until the owner has made a full test booking on the preview and said yes.
- Ask the owner for nothing secret in chat. Keys go in the Grok Bot vault and in the hosting env vars.

## 1. Supabase project and keys
1. **You (the bot) create the project through the Supabase connector. The owner never does it.** The owner only makes a Supabase account (email sign-up; if Supabase forces **Create a new organization**: Name = their business, Type Personal, Plan **Free - $0/month**), saves the login in the vault and connects Supabase in Grok Bot. Then, with the connector: create the project in their organisation (name = business name, region closest to their customers, a generated database password saved straight to the vault, never shown in chat), keep the Data API on, and switch on row level security for every new table. Still write explicit RLS policies for every table; never rely on an auto setting alone. Don't ask the owner to open **Create a new project**, copy API keys or tick security boxes. Only if the connector can't do a step, explain the dashboard step in plain words: **Create a new project** (Organization, Project name, Database password → **Generate a password**, Region), Security: keep **Enable Data API**, tick **Enable automatic RLS**, then **Create new project**.
2. Keys: fetch them through the connector and write them straight to the vault and the hosting env vars; never paste keys in chat or ask the owner to copy them. For reference, the dashboard has them at project **Settings → API Keys**, tab **Publishable and secret API keys**, sections **Publishable key** and **Secret keys** (if empty, **New secret key** / **Create new API keys**). The top-bar **Connect** button shows the Project URL.
   - **Publishable key** `sb_publishable_...`: safe in the browser; row level security applies.
   - **Secret key** `sb_secret_...`: server only. Bypasses row level security. Never in client code, never in `NEXT_PUBLIC_*`, never in git, never in chat.
   - Older projects may show legacy `anon` / `service_role` keys. Prefer the new keys; legacy keys are being retired.
3. Env vars (Vercel → Project → Settings → Environment Variables; set for Production and Preview):

| Name | Value | Where used |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Project URL `https://<ref>.supabase.co` | browser + server |
| `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` | `sb_publishable_...` | browser + server |
| `SUPABASE_SECRET_KEY` | `sb_secret_...` | server only (webhooks, admin jobs) |
| `STRIPE_SECRET_KEY` | `sk_test_...` first, `sk_live_...` at go-live | server only |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` from the webhook destination | server only |
| `NEXT_PUBLIC_SITE_URL` | production URL | redirects, emails |

Use test keys in Preview and live keys in Production only after the owner approves go-live. For non-Next.js sites, drop the `NEXT_PUBLIC_` prefix and keep the same split.

## 2. Auth settings
- **Authentication → URL Configuration**: Site URL = production URL. Redirect URLs: `http://localhost:3000/**` and the hosting preview pattern, e.g. `https://*-<team-or-account-slug>.vercel.app/**`, plus the production domain.
- **Authentication → Sign In / Providers**: Email on. Keep "Confirm email" on.
- **Email sending:** Supabase's built-in email only delivers to the project's team members and is heavily rate limited. Before real customers sign up, set up custom SMTP (**Authentication → Emails → SMTP Settings**) with the site's email provider (e.g. Resend), and edit the email templates in plain words.
- Pages to build: Register, Log in, Forgot password, Reset password, My account (upcoming bookings, past bookings, orders, edit name/phone), Log out. Use `@supabase/ssr` for Next.js (cookie-based sessions, middleware refresh).

## 3. Database (run as a migration, review in the PR)
```sql
create extension if not exists btree_gist;

-- one row per customer, created automatically on sign-up
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text unique,
  full_name text,
  phone text,
  created_at timestamptz not null default now()
);

create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profiles (id, email, full_name)
  values (new.id, new.email, new.raw_user_meta_data->>'full_name');
  return new;
end $$;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

create table public.services (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  description text,
  duration_minutes int not null check (duration_minutes > 0),
  price_pence int not null check (price_pence >= 0),   -- smallest currency unit
  currency text not null default 'gbp',
  active boolean not null default true
);

create table public.staff (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  photo_url text,
  active boolean not null default true
);

-- weekly opening hours per staff member (0 = Sunday)
create table public.availability (
  id uuid primary key default gen_random_uuid(),
  staff_id uuid not null references public.staff(id) on delete cascade,
  weekday int not null check (weekday between 0 and 6),
  start_time time not null,
  end_time time not null check (end_time > start_time)
);

-- days off, holidays, one-off blocks
create table public.time_off (
  id uuid primary key default gen_random_uuid(),
  staff_id uuid references public.staff(id) on delete cascade, -- null = whole business closed
  during tstzrange not null
);

create type public.booking_status as enum ('pending', 'paid', 'cancelled');

create table public.bookings (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.profiles(id),
  service_id uuid not null references public.services(id),
  staff_id uuid not null references public.staff(id),
  during tstzrange not null,
  status public.booking_status not null default 'pending',
  price_pence int not null,
  currency text not null,
  hold_expires_at timestamptz,             -- pending holds the slot until then
  stripe_checkout_session_id text unique,
  stripe_payment_intent_id text,
  paid_at timestamptz,
  cancelled_at timestamptz,
  created_at timestamptz not null default now(),
  -- no double bookings: one staff member can't have two live bookings that overlap
  constraint no_overlap exclude using gist (staff_id with =, during with &&)
    where (status in ('pending', 'paid'))
);

-- shop orders copied in from Shopify (or another shop) by webhook
create table if not exists public.orders (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.profiles(id),
  email text,
  source text not null default 'shopify',
  external_order_id text not null,
  order_number text,
  total_pence int,
  currency text,
  financial_status text,
  line_items jsonb,
  created_at timestamptz not null default now(),
  unique (source, external_order_id)
);

-- webhook idempotency: every processed event id is stored once
create table public.webhook_events (
  id text primary key,                 -- Stripe event id or Shopify webhook id
  source text not null,
  received_at timestamptz not null default now()
);
```

### Row level security (switch it on for every table)
```sql
alter table public.profiles       enable row level security;
alter table public.services       enable row level security;
alter table public.staff          enable row level security;
alter table public.availability   enable row level security;
alter table public.time_off       enable row level security;
alter table public.bookings       enable row level security;
alter table public.orders         enable row level security;
alter table public.webhook_events enable row level security;  -- no policies: server only

create policy "own profile" on public.profiles for select to authenticated using ((select auth.uid()) = id);
create policy "edit own profile" on public.profiles for update to authenticated using ((select auth.uid()) = id) with check ((select auth.uid()) = id);

create policy "public services" on public.services for select to anon, authenticated using (active);
create policy "public staff"    on public.staff    for select to anon, authenticated using (active);
create policy "public hours"    on public.availability for select to anon, authenticated using (true);
create policy "public time off" on public.time_off for select to anon, authenticated using (true);

create policy "own bookings" on public.bookings for select to authenticated using ((select auth.uid()) = user_id);
create policy "own orders"   on public.orders   for select to authenticated using ((select auth.uid()) = user_id);
```
- Customers can **read** their own bookings and orders. They never insert or update bookings directly: the server does that with the secret key after checking the slot and price. This stops anyone booking for free or changing a price.
- Free/busy for the calendar: expose a `security definer` function (e.g. `public.busy_slots(staff_id, from, to)`) that returns only time ranges, never names or emails.
- The owner edits services, staff and hours in the Supabase Table Editor at first. Build an admin page later only if they ask, protected by an `is_admin` flag checked in RLS.

## 4. Booking flow (prepaid with Stripe Checkout)
1. **Calendar page** (public): pick service → staff (or "anyone") → day → free slot. Free slots = availability minus time off minus busy slots, in the business's time zone, sliced by service duration. Store everything as `timestamptz`.
2. **Customer must be logged in** to book (send them to Log in / Register, then back to the chosen slot).
3. **Server route `POST /api/bookings/checkout`** (secret key, never trusts the browser's price):
   - Cancel expired holds: `update bookings set status='cancelled', cancelled_at=now() where status='pending' and hold_expires_at < now()`.
   - Load the service price and duration from the database.
   - Insert the booking as `pending` with `hold_expires_at = now() + 30 minutes`. If the insert fails on `no_overlap`, the slot has just gone: tell the customer kindly and show other times.
   - Create a Stripe Checkout Session: `mode: 'payment'`, line item from the database price, `customer_email` = profile email, `client_reference_id` and `metadata.booking_id` = booking id, `expires_at` = 30 minutes from now (Stripe's minimum), `success_url` = `/account/bookings?paid=1`, `cancel_url` = back to the calendar. Pass an idempotency key (e.g. `booking-<id>`) on the create call.
   - Save `stripe_checkout_session_id` on the booking and redirect to the session URL.
4. **Success page** says "Thanks, we're confirming your payment" and reads the booking status. It never marks anything paid.

## 5. Stripe webhook (the only thing that marks a booking paid)
- **You (the bot) create the webhook yourself. The owner never does it.** Use the Stripe connector, or the Stripe API (`POST /v1/webhook_endpoints`) with the secret key from the vault: endpoint `https://<production-domain>/api/stripe/webhook`, events `checkout.session.completed`, `checkout.session.async_payment_succeeded`, `checkout.session.async_payment_failed`, `checkout.session.expired`. Do it in **test mode / sandbox first**. The signing secret (`whsec_...`) is returned only once, when the endpoint is created: write it straight to the Grok Bot vault and `STRIPE_WEBHOOK_SECRET`, never show it in chat. Check it with a test event (`stripe trigger checkout.session.completed` or the API) and confirm the booking turns `paid`. Only if you can't create it, explain the dashboard step in plain words: **Workbench → Webhooks → + Add destination**, the events and endpoint above, then save the signing secret to the vault yourself.
- Locally: `stripe listen --forward-to localhost:3000/api/stripe/webhook`.

```ts
// app/api/stripe/webhook/route.ts  (Next.js App Router)
import Stripe from 'stripe';
import { createClient } from '@supabase/supabase-js';
export const runtime = 'nodejs';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const db = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SECRET_KEY!, { auth: { persistSession: false } });

export async function POST(req: Request) {
  const raw = await req.text();                       // raw body: needed for the signature
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(raw, req.headers.get('stripe-signature')!, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch { return new Response('bad signature', { status: 400 }); }

  // idempotency: Stripe can send the same event more than once
  const { error: dup } = await db.from('webhook_events').insert({ id: event.id, source: 'stripe' });
  if (dup) return new Response('already handled', { status: 200 });

  const s = event.data.object as Stripe.Checkout.Session;
  const bookingId = s.metadata?.booking_id ?? s.client_reference_id;
  if (!bookingId) return new Response('ok', { status: 200 });

  if ((event.type === 'checkout.session.completed' && s.payment_status === 'paid') ||
      event.type === 'checkout.session.async_payment_succeeded') {
    await db.from('bookings')
      .update({ status: 'paid', paid_at: new Date().toISOString(), hold_expires_at: null,
                stripe_payment_intent_id: String(s.payment_intent ?? '') })
      .eq('id', bookingId).eq('status', 'pending');   // conditional: safe to run twice
  }
  if (event.type === 'checkout.session.expired' || event.type === 'checkout.session.async_payment_failed') {
    await db.from('bookings').update({ status: 'cancelled', cancelled_at: new Date().toISOString() })
      .eq('id', bookingId).eq('status', 'pending');
  }
  return new Response('ok', { status: 200 });
}
```
- If the event-id insert succeeds but processing then throws, delete that `webhook_events` row before returning 500 so Stripe's retry is processed.
- Check `amount_total` matches the booking's `price_pence`; if not, flag it to the owner.
- Edge case: payment arrives for a booking already cancelled (hold expired and slot taken). Don't double-book: refund in Stripe and tell the customer and owner in plain words.
- Return 2xx fast; send confirmation emails after the update (or from a database trigger), not before.

## 6. Cancellations and refunds
Start simple: when the owner asks you to cancel a booking, you refund it through the Stripe connector or API and set the booking to `cancelled` in Supabase, then tell the owner in plain words. The owner can also refund in the Stripe Dashboard; if they do, you still set the booking to `cancelled`. Add a customer "Cancel" button (with the owner's cancellation rule, e.g. 24 hours' notice) only when asked; it must run server-side and call Stripe Refunds.

## 7. Never commit secrets
- `.env*` in `.gitignore`. Only `NEXT_PUBLIC_*` values may reach the browser.
- Search the diff for `sb_secret_`, `sk_live_`, `sk_test_`, `whsec_` before every PR. If one leaks, rotate it straight away (Supabase API Keys page / Stripe API keys) and tell the owner.
- If the bot has a Supabase connection, limit it to this one project.

## 8. Rollout checklist
1. Branch + PR with: migration, auth pages, calendar, checkout route, webhook route, My account.
2. Preview link. On the preview, in Stripe test mode: register with a real inbox, confirm the email, book a slot, pay with test card `4242 4242 4242 4242`, see it as **paid** in My account and in the Supabase table. Try to book the same slot twice: the second attempt must be refused.
3. Show the owner in plain words; publish only on their yes.
4. Go-live (separate yes): swap to live Stripe keys and create the live-mode webhook destination yourself (same way as above), set Production env vars, redeploy, make one small real booking and refund it.
5. Log it in the audit log.

## Plain-language summary for the owner
"Supabase keeps your customer accounts and your diary. When someone books, they pay through Stripe; once Stripe confirms the money, the booking turns to paid. If you add a shop, Shopify keeps your stock and its orders show up in the same customer's account."
