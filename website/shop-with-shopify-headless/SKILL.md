---
name: Shop with Shopify (headless)
description: >-
  Use when a website needs to sell physical products (stock, variants,
  shipping) while keeping its own design, and the owner manages products in
  Shopify. Covers the Headless channel and Storefront API tokens, reading
  products, handing the buyer to Shopify checkout with their email prefilled,
  saving orders into the site's database (e.g. Supabase) with an HMAC-verified
  orders webhook, env vars, and safe rollout. Pair with "User accounts and
  bookings with Supabase" when customers log in on the site.
---
# Shop with Shopify (headless)

Shopify is the **stockroom and till for products**: the owner adds products, prices, photos and stock in Shopify admin, and Shopify runs the product checkout, payments, tax and shipping. The website shows the products in its own design and sends buyers to Shopify's checkout. "Headless" just means Shopify's own theme isn't used; the website is the shop window.

## Who owns what (the split)
| Job | Owner |
|---|---|
| Products, stock, prices, discounts, shipping, refunds | Shopify admin |
| Product checkout and card payments for products | Shopify checkout |
| Showing products on the site | Website, via the Storefront API |
| Customer accounts and "My account" | The site's own accounts (e.g. Supabase). **Do not switch on Shopify customer accounts** as a second login. |
| Record of orders per customer | Site database, filled by the Shopify orders webhook |
| Bookings / services (if any) | Not Shopify. Use the Supabase recipe (Stripe Checkout). |

Trade-off to tell the owner: products are paid out by Shopify, bookings by Stripe, so there are two payouts and two dashboards. That's normal and keeps each tool doing what it's good at.

## Before you start
- "Never straight to main": branch → pull request → preview → owner's yes → merge.
- Use a development store, or the owner's store with payments in **test mode**, until the owner has made a full test order on the preview and said yes.
- Plan: Shopify **Basic or higher** for a headless shop (check current plans at https://www.shopify.com/pricing; prices vary by country and billing period).

## 1. Owner setup in Shopify (guide them, don't ask for passwords)
1. Install the free **Headless** sales channel: https://apps.shopify.com/headless → Install → **Create storefront**.
2. In **Sales channels → Headless → (storefront) → Storefront API permissions → Edit**, allow at least products, product listings, inventory (read), and checkouts/cart. Save.
3. The storefront page shows a **public access token** and a **private access token**. Owner saves both in the Grok Bot vault, then adds them to the hosting env vars (or shares them with the bot through the vault, never in chat).
4. **Publish products to the Headless channel** (product page → Publishing / Sales channels). Products not published there won't appear on the site.

## 2. Env vars (Vercel → Settings → Environment Variables, Production + Preview)
| Name | Value | Where used |
|---|---|---|
| `SHOPIFY_STORE_DOMAIN` | `your-store.myshopify.com` | server |
| `SHOPIFY_STOREFRONT_API_VERSION` | a current stable version, e.g. `2026-10` | server |
| `SHOPIFY_STOREFRONT_PRIVATE_TOKEN` | private Storefront token | server only, never `NEXT_PUBLIC_*` |
| `NEXT_PUBLIC_SHOPIFY_STOREFRONT_PUBLIC_TOKEN` | public Storefront token (only if the browser calls Shopify directly) | browser |
| `SHOPIFY_WEBHOOK_SECRET` | signing key shown under Settings → Notifications → Webhooks | server only |
| `SUPABASE_SECRET_KEY`, `NEXT_PUBLIC_SUPABASE_URL` | from the Supabase recipe | server (webhook writes orders) |

Prefer server-side calls with the private token (headers: `Shopify-Storefront-Private-Token`, and `Shopify-Storefront-Buyer-IP` with the shopper's IP when acting for a shopper). Browser calls use the public token in `X-Shopify-Storefront-Access-Token`.

## 3. Read products (Storefront API, GraphQL)
Endpoint: `https://${SHOPIFY_STORE_DOMAIN}/api/${SHOPIFY_STOREFRONT_API_VERSION}/graphql.json`
```ts
// lib/shopify.ts
export async function shopify<T>(query: string, variables: Record<string, unknown> = {}): Promise<T> {
  const res = await fetch(`https://${process.env.SHOPIFY_STORE_DOMAIN}/api/${process.env.SHOPIFY_STOREFRONT_API_VERSION}/graphql.json`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Shopify-Storefront-Private-Token': process.env.SHOPIFY_STOREFRONT_PRIVATE_TOKEN! },
    body: JSON.stringify({ query, variables }),
    next: { revalidate: 60 },          // cache product pages; stock still checked at checkout
  });
  const json = await res.json();
  if (json.errors) throw new Error(JSON.stringify(json.errors));
  return json.data;
}

export const PRODUCTS = /* GraphQL */ `
  query Products($first: Int!) {
    products(first: $first, sortKey: TITLE) {
      nodes {
        id handle title description availableForSale
        featuredImage { url altText width height }
        priceRange { minVariantPrice { amount currencyCode } }
        variants(first: 20) { nodes { id title availableForSale price { amount currencyCode } } }
      }
    }
  }`;
```
- Shop page: grid of products. Product page by `handle` (`productByHandle` / `product(handle:)`), variant picker, "Buy" or "Add to bag".
- Show sold-out variants as unavailable (`availableForSale: false`).
- Format money with `Intl.NumberFormat('en-GB', { style: 'currency', currency })`. For other countries, use `@inContext(country: XX)`.

## 4. Checkout handoff (cart → Shopify checkout)
Server route `POST /api/shop/checkout` with `{ lines: [{ variantId, quantity }] }`:
```ts
const CART_CREATE = /* GraphQL */ `
  mutation CartCreate($input: CartInput!) {
    cartCreate(input: $input) { cart { id checkoutUrl } userErrors { field message } }
  }`;

const user = await getSupabaseUser();               // null if logged out: guest checkout is fine
const { cartCreate } = await shopify<any>(CART_CREATE, { input: {
  lines: lines.map(l => ({ merchandiseId: l.variantId, quantity: l.quantity })),
  buyerIdentity: user?.email ? { email: user.email, countryCode: 'GB' } : { countryCode: 'GB' },
  attributes: user ? [{ key: 'supabase_user_id', value: user.id }] : [],
}});
if (cartCreate.userErrors.length) return Response.json({ error: cartCreate.userErrors }, { status: 400 });
return Response.json({ url: cartCreate.cart.checkoutUrl });   // browser redirects here
```
- `buyerIdentity.email` prefills the checkout email. Cart `attributes` come back on the order as `note_attributes`, which is how the webhook links the order to the logged-in customer.
- Keep the cart in the browser (localStorage) or create it at "Checkout" time. Never log or expose the cart's secret `key` parameter.
- After paying, Shopify shows its own thank-you page. Optionally add a "Back to <site>" link in Shopify checkout settings.
- Optional: connect a subdomain like `shop.example.com` to Shopify so checkout shows the brand's domain.

## 5. Orders webhook → site database
**You (the bot) create the webhooks yourself. The owner never does it.**
- With the store's Admin API access token from the vault, call the Admin GraphQL `webhookSubscriptionCreate` twice: topic `ORDERS_CREATE` and topic `ORDERS_PAID`, both with format JSON and callback URL `https://<production-domain>/api/shopify/orders`. Then list the subscriptions to confirm both exist.
- Webhooks made through the API are signed with the app's **client secret** (API secret key). Write it straight to the Grok Bot vault and `SHOPIFY_WEBHOOK_SECRET`; never show it in chat.
- Only if you can't use the API, explain the admin step in plain words: **Settings → Notifications → Webhooks → Create webhook**, Event **Order creation** and a second for **Order payment**, Format **JSON**, the URL above, latest stable API version → Save. Those are signed with the key shown on that page ("Your webhooks will be signed with …"), so use that key instead and save it to the vault yourself.
- URL rules: must be https and public; not localhost, not a `shopify.com` / `myshopify.com` address, and not a custom domain that's connected to the Shopify store itself. Use the website's own domain.
- Check the endpoint answers 200: place a test order on the development store (or use **Send test** for admin-made webhooks; test payloads won't match a real customer).

```ts
// app/api/shopify/orders/route.ts
import crypto from 'node:crypto';
import { createClient } from '@supabase/supabase-js';
export const runtime = 'nodejs';
const db = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SECRET_KEY!, { auth: { persistSession: false } });

export async function POST(req: Request) {
  const raw = await req.text();                                   // raw body, before JSON.parse
  const got = Buffer.from(req.headers.get('x-shopify-hmac-sha256') ?? '', 'utf8');
  const want = Buffer.from(crypto.createHmac('sha256', process.env.SHOPIFY_WEBHOOK_SECRET!).update(raw, 'utf8').digest('base64'), 'utf8');
  if (got.length !== want.length || !crypto.timingSafeEqual(got, want)) return new Response('bad signature', { status: 401 });

  const order = JSON.parse(raw);
  const topic = req.headers.get('x-shopify-topic');              // orders/create, orders/paid
  const webhookId = req.headers.get('x-shopify-webhook-id');
  if (webhookId) {
    const { error: dup } = await db.from('webhook_events').insert({ id: `shopify:${webhookId}`, source: 'shopify' });
    if (dup) return new Response('already handled', { status: 200 });
  }

  // link to the site's customer: cart attribute first, then email
  const attr = (order.note_attributes ?? []).find((a: any) => a.name === 'supabase_user_id')?.value;
  let userId: string | null = attr ?? null;
  const email = (order.email ?? order.customer?.email ?? '').toLowerCase() || null;
  if (!userId && email) {
    const { data } = await db.from('profiles').select('id').eq('email', email).maybeSingle();
    userId = data?.id ?? null;
  }

  await db.from('orders').upsert({
    source: 'shopify',
    external_order_id: String(order.id),
    order_number: order.name,                                   // e.g. "#1001"
    user_id: userId, email,
    total_pence: Math.round(Number(order.total_price) * 100),
    currency: order.currency,
    financial_status: order.financial_status,
    line_items: (order.line_items ?? []).map((l: any) => ({ title: l.title, variant: l.variant_title, qty: l.quantity, price: l.price })),
  }, { onConflict: 'source,external_order_id' });

  return new Response('ok', { status: 200 });                   // answer within 5 seconds
}
```
- Shopify retries failed deliveries (several times over a few hours) and can send the same event twice: the webhook-id check plus the upsert make that harmless.
- If processing fails after the webhook-id insert, delete that row and return 500 so the retry is processed.
- If the site has no Supabase, the same tables work in any Postgres; the `orders` + `webhook_events` SQL is below.

```sql
create table if not exists public.orders (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,                        -- references the site's customer table if there is one
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
create table if not exists public.webhook_events (id text primary key, source text not null, received_at timestamptz not null default now());
alter table public.orders enable row level security;
alter table public.webhook_events enable row level security;
-- with Supabase Auth: customers read only their own orders
create policy "own orders" on public.orders for select to authenticated using ((select auth.uid()) = user_id);
```
- "My account → Orders" lists the customer's orders (number, date, total, status). For tracking and returns, link to the Shopify order status page (`order_status_url` in the payload; store it if wanted).

## 6. Never commit secrets
- Tokens and the webhook key live in the Grok Bot vault and hosting env vars only. `.env*` in `.gitignore`.
- Only the **public** Storefront token may use `NEXT_PUBLIC_`. If the private token or webhook key leaks, rotate it (Headless storefront page / recreate webhooks) and tell the owner.

## 7. Rollout checklist
1. Branch + PR: Shopify client, shop page, product page, checkout route, orders webhook, My account orders list.
2. Preview: products and prices match Shopify admin; sold-out shows as sold out; checkout opens with the customer's email filled in.
3. Test order with payments in test mode. Within a minute the order appears in the database and in the customer's My account.
4. Show the owner in plain words; publish only on their yes. Switch payments out of test mode only on a separate yes.
5. Log it in the audit log.

## Plain-language summary for the owner
"You keep adding products and stock in Shopify like normal. The website shows them in your own design, and when someone buys, Shopify takes the payment and you send the order as usual. A copy of each order lands in the customer's account on your site."
