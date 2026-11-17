# Stripe Integration — Remaining Setup

Hosted Stripe Checkout for tnt-labs.com with **variable pricing** — pay any
service, any amount, via a shareable payment link you can drop into invoices.

The site is static (GitHub Pages); the server side is the existing Google
Apps Script web app (`google-apps-script.gs`), which creates the Checkout
Session via the Stripe REST API and returns the hosted URL to
`checkout.html` via JSONP.

## Values to Replace

The following values are placeholders and must be updated before going live.

**Files containing placeholders:**
- [google-apps-script.gs](google-apps-script.gs)

| Field | Current Value | What to Set |
|-------|--------------|-------------|
| mode | `payment` | `"payment"` for one-time charges or `"subscription"` for recurring billing. |
| success_url | `https://tnt-labs.com/checkout.html?paid=1&session_id={CHECKOUT_SESSION_ID}` | Your actual post-payment success page. Keep the `{CHECKOUT_SESSION_ID}` template. |
| cancel_url | `https://tnt-labs.com/checkout.html?cancelled=1` | Your actual cancel/return page URL. |
| line_items[].price_data | built from `amount` + `service` params | Prices are set per-request (USD). Switch to a fixed `price_...` Price ID if you ever want catalog pricing. |
| STRIPE_SECRET_KEY | *(not set)* | Add as a Script Property — see below. Never put it in the site's HTML/JS. |
| INVOICE_TOKEN | *(optional, not set)* | Optional shared secret for the `action=invoice` staff endpoint. Set it in Script Properties, then pass `&token=...` on invoice requests. |

## Configured Parameters

These parameters were configured in Checkout Studio and are already set correctly.

**Files containing these parameters:**
- [google-apps-script.gs](google-apps-script.gs)

| Parameter | Value |
|-----------|-------|
| ui_mode | `hosted_page` |
| billing_address_collection | `auto` |
| phone_number_collection.enabled | `true` |
| automatic_tax.enabled | `false` |
| allow_promotion_codes | `false` |
| submit_type | `auto` |
| integration_identifier | `hosted_web_0001` |
| origin_context | `web` |
| client_reference_id | invoice # (when supplied) — appears on the Stripe payment |
| payment_method_collection | `always` — included only when `mode` is `"subscription"` |

## Setup and next steps

1. **Set the secret key.** Apps Script project → Project Settings →
   Script Properties → add `STRIPE_SECRET_KEY` = `sk_test_...`
   (from https://dashboard.stripe.com/test/apikeys). Use `sk_live_...` when
   going live.
2. **Redeploy Apps Script** (the one manual step — requires your Google
   login): paste the updated `google-apps-script.gs` into the project →
   Deploy → Manage deployments → pencil → New version → Deploy. The
   `/exec` URL stays the same — no site changes needed.
3. **Publish the site.** Commit and push `checkout.html` to the GitHub
   Pages repo so `https://tnt-labs.com/checkout.html` is live.

### Sending an invoice payment link

Build a link with the amount, service, and invoice number, and paste it
into the invoice email:

```
https://tnt-labs.com/checkout.html?amount=1450.00&service=ICP-MS%20heavy%20metals%20x3&invoice=INV-0042
```

The customer opens it, sees the pre-filled details, clicks pay, and lands
on Stripe's hosted checkout. The invoice number is attached to the Stripe
payment as `client_reference_id` for reconciliation.

### Sending a real Stripe invoice (staff use)

`action=invoice` creates a proper Stripe Invoice — hosted page, PDF,
automatic email to the customer, 30-day terms:

```
https://script.google.com/macros/s/…/exec?action=invoice&token=YOURTOKEN&email=client@co.com&name=Acme%20Corp&amount=1450.00&service=ICP-MS%20heavy%20metals%20x3
```

Returns `{ success, url, invoice }` — `url` is the `hosted_invoice_url`
you can paste anywhere; Stripe also emails it to the customer
automatically. Set `INVOICE_TOKEN` in Script Properties first so strangers
can't raise invoices on your account.

### Project structure (new/changed files)

- `WEBSITE/checkout.html` — "Pay Online" page: amount/service/invoice
  fields (pre-filled from the URL), JSONP call to Apps Script, redirect to
  Stripe; shows paid/cancelled states on return.
- `WEBSITE/google-apps-script.gs` — `createCheckoutSession(p)` builds a
  `price_data` line item from the request params; `action=checkout`
  handlers in `doGet` (JSONP) and `doPost`.

### How it works

1. Customer opens `checkout.html` (or an invoice link with params).
2. The page calls the Apps Script `/exec` URL via JSONP with the amount,
   service description, and optional invoice number.
3. Apps Script calls `POST /v1/checkout/sessions` and returns
   `{ success: true, url: "https://checkout.stripe.com/…" }`.
4. The browser redirects to Stripe; on completion Stripe sends the
   customer back to `success_url` / `cancel_url` on tnt-labs.com.

### Testing

Use Stripe test mode (`sk_test_...` key). Test card: `4242 4242 4242 4242`,
any future expiry, any CVC/ZIP. More cards (declines, 3DS):
https://docs.stripe.com/testing

### Next steps

- Optional: add a `checkout.session.completed` webhook for automated
  fulfillment/receipts — Apps Script can't verify webhook signatures
  easily; consider a small server endpoint if needed.
- Switch to live keys before accepting real payments.

Resources: https://support.stripe.com · https://docs.stripe.com/mcp
