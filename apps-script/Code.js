/**
 * TNT QUOTE BACKEND — Google Apps Script (free, runs on your Google account)
 * Receives quote submissions from the website and emails them to the lab
 * as a formatted HTML table (plus a plain-text fallback).
 *
 * ─── UPDATE DEPLOYMENT (when this file changes) ─────────────────────────
 * 1. Sign in to texas.nuclear.technologies@gmail.com
 * 2. Open https://script.google.com → your project → paste this file → Save
 * 3. Deploy → Manage deployments → pencil icon → Version: "New version"
 * 4. Deploy — the /exec URL stays the same, no site changes needed
 * ───────────────────────────────────────────────────────────────────────
 * First-time deploy: see the previous version's notes or ask Devin.
 * Test: open the /exec URL in a browser → {"status":"ok","service":"tnt-quote"}
 */

var NOTIFY = "texas.nuclear.technologies@gmail.com";
var TZ = "America/Chicago";

function doGet(e) {
  var p = (e && e.parameter) || {};
  if (p.action === "checkout" || p.action === "invoice") return checkoutJsonp(p);
  if (p.action === "diag") {
    var keys = PropertiesService.getScriptProperties().getKeys();
    return ContentService
      .createTextOutput(JSON.stringify({ keys: keys }))
      .setMimeType(ContentService.MimeType.JSON);
  }
  return ContentService
    .createTextOutput(JSON.stringify({ status: "ok", service: "tnt-quote", version: 2 }))
    .setMimeType(ContentService.MimeType.JSON);
}

function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/\n/g, "<br>");
}

function row(label, value, opts) {
  if (!value) return "";
  var bg = (opts && opts.bg) || "";
  var bold = (opts && opts.bold) ? "font-weight:700;" : "";
  var size = (opts && opts.size) || "14px";
  return '<tr>' +
    '<td style="padding:11px 16px;width:130px;vertical-align:top;' +
      'font-family:Arial,sans-serif;font-size:11px;letter-spacing:2px;' +
      'color:#d4af37;background:' + (bg || '#101e38') + ';' +
      'border-bottom:1px solid #1c2d4d;">' + label + '</td>' +
    '<td style="padding:11px 16px;vertical-align:top;' +
      'font-family:Arial,sans-serif;font-size:' + size + ';' + bold +
      'color:#c0c6ce;background:' + (bg || '#0a1428') + ';' +
      'border-bottom:1px solid #1c2d4d;">' + esc(value) + '</td></tr>';
}

function quoteTable(p, stamp) {
  return '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" ' +
    'style="max-width:560px;border:1px solid #1c2d4d;background:#0a1428;">' +
    '<tr><td colspan="2" style="padding:16px 18px;' +
      'font-family:Arial,sans-serif;font-size:13px;letter-spacing:3px;' +
      'color:#d4af37;background:#060d1b;border-bottom:2px solid #d4af37;">' +
      'TNT — NEW QUOTE REQUEST</td></tr>' +
    row("NAME", p.name) +
    row("COMPANY", p.company) +
    row("EMAIL", p.email || p.contact) +
    row("PHONE", p.phone) +
    '<tr><td colspan="2" style="height:8px;background:#060d1b;padding:0;"></td></tr>' +
    row("TEST", p.test) +
    row("QUANTITY", p.quantity) +
    row("TURNAROUND", p.turnaround) +
    row("ESTIMATE", p.estimate, { bold: true, size: "20px", bg: "#14233f" }) +
    row("NOTES", p.notes) +
    row("SUBMITTED", stamp) +
    '</table>';
}

function plainBody(p, stamp) {
  var keys = ["name", "company", "email", "phone", "test", "quantity",
              "turnaround", "estimate", "notes"];
  var lines = ["NEW QUOTE REQUEST — tnt-testing.github.io/website", ""];
  keys.forEach(function (k) {
    if (p[k]) lines.push(k.toUpperCase() + ": " + p[k]);
  });
  lines.push("SUBMITTED: " + stamp);
  return lines.join("\n");
}

/* ─── STRIPE CHECKOUT ─────────────────────────────────────────────────
 * Creates a Stripe Checkout Session via the REST API and returns the
 * hosted checkout URL. Called from checkout.html on tnt-labs.com via
 * JSONP: GET ?action=checkout&amount=1450&service=ICP-MS%20x3&callback=fn
 * (JSONP is used because Apps Script responses are not CORS-readable.)
 * Secret key: Apps Script project → Project Settings → Script
 * Properties → STRIPE_SECRET_KEY = rk_live_... / sk_live_...
 * ──────────────────────────────────────────────────────────────────── */
var STRIPE_API = "https://api.stripe.com/v1/checkout/sessions";

function stripeKey() {
  var props = PropertiesService.getScriptProperties();
  return props.getProperty("STRIPE_SECRET_KEY") || props.getProperty("stripe_key");
}

function createCheckoutSession(p) {
  var key = stripeKey();
  if (!key) return { success: false, error: "Stripe not configured" };

  // Variable pricing: amount in dollars, service = line-item description.
  var amount = Math.round(parseFloat(p.amount) * 100);
  if (!amount || amount < 50) return { success: false, error: "Invalid amount" };
  var service = String(p.service || "TNT analytical testing services").slice(0, 250);
  var invoice = String(p.invoice || "").replace(/[^\w-]/g, "").slice(0, 60);

  // TODO: Set mode to "subscription" if selling recurring products.
  var mode = "payment";

  var payload = {
    ui_mode: "hosted",
    mode: mode,
    billing_address_collection: "auto",
    "phone_number_collection[enabled]": "true",
    "automatic_tax[enabled]": "false",
    allow_promotion_codes: "false",
    submit_type: "auto",
    integration_identifier: "hosted_web_0001",
    origin_context: "web",
    success_url: "https://tnt-labs.com/checkout.html?paid=1&session_id={CHECKOUT_SESSION_ID}",
    cancel_url: "https://tnt-labs.com/checkout.html?cancelled=1",
    "line_items[0][price_data][currency]": "usd",
    "line_items[0][price_data][product_data][name]": service,
    "line_items[0][price_data][unit_amount]": String(amount),
    "line_items[0][quantity]": "1"
  };
  if (invoice) payload.client_reference_id = invoice;
  // Only include payment_method_collection when mode is "subscription".
  if (mode === "subscription") payload.payment_method_collection = "always";

  var resp = UrlFetchApp.fetch(STRIPE_API, {
    method: "post",
    payload: payload,
    headers: { Authorization: "Bearer " + key },
    muteHttpExceptions: true
  });
  var session = JSON.parse(resp.getContentText());
  if (!session.url) {
    return { success: false, error: (session.error && session.error.message) || "Stripe error" };
  }
  return { success: true, url: session.url };
}

/* ─── STRIPE INVOICES ─────────────────────────────────────────────────
 * Creates + finalizes a real Stripe Invoice and returns its hosted
 * payment page URL — Stripe also emails it to the customer
 * (collection_method=send_invoice, 30-day terms).
 * GET ?action=invoice&token=...&email=client@co.com&amount=1450&service=...
 * ──────────────────────────────────────────────────────────────────── */
function stripePost(path, payload) {
  var key = stripeKey();
  var resp = UrlFetchApp.fetch("https://api.stripe.com/v1/" + path, {
    method: "post",
    payload: payload,
    headers: { Authorization: "Bearer " + key },
    muteHttpExceptions: true
  });
  return JSON.parse(resp.getContentText());
}

function createInvoice(p) {
  var props = PropertiesService.getScriptProperties();
  if (!stripeKey())
    return { success: false, error: "Stripe not configured" };
  // Optional staff gate: set INVOICE_TOKEN in Script Properties, then pass
  // &token=... on invoice requests. Blocks strangers from raising invoices.
  var token = props.getProperty("INVOICE_TOKEN");
  if (token && p.token !== token) return { success: false, error: "Unauthorized" };

  var email = String(p.email || "").trim();
  var amount = Math.round(parseFloat(p.amount) * 100);
  if (email.indexOf("@") < 0) return { success: false, error: "Customer email required" };
  if (!amount || amount < 50) return { success: false, error: "Invalid amount" };
  var service = String(p.service || "TNT analytical testing services").slice(0, 250);

  var customer = stripePost("customers", { email: email, name: p.name || "" });
  if (customer.error) return { success: false, error: customer.error.message };

  var item = stripePost("invoiceitems", {
    customer: customer.id,
    amount: String(amount),
    currency: "usd",
    description: service
  });
  if (item.error) return { success: false, error: item.error.message };

  var inv = stripePost("invoices", {
    customer: customer.id,
    collection_method: "send_invoice",
    days_until_due: "30",
    auto_advance: "true"
  });
  if (inv.error) return { success: false, error: inv.error.message };

  var fin = stripePost("invoices/" + inv.id + "/finalize", {});
  if (fin.error) return { success: false, error: fin.error.message };

  stripePost("invoices/" + inv.id + "/send", {}); // Stripe emails it to the customer

  return { success: true, url: fin.hosted_invoice_url, invoice: fin.number };
}

function checkoutJsonp(p) {
  var out = (p.action === "invoice") ? createInvoice(p) : createCheckoutSession(p);
  var cb = String(p.callback || "callback").replace(/[^\w$.]/g, "");
  return ContentService
    .createTextOutput(cb + "(" + JSON.stringify(out) + ");")
    .setMimeType(ContentService.MimeType.JAVASCRIPT);
}

function doPost(e) {
  var p = (e && e.parameter) || {};
  if (p.action === "checkout") {
    var out = createCheckoutSession(p);
    return ContentService
      .createTextOutput(JSON.stringify(out))
      .setMimeType(ContentService.MimeType.JSON);
  }
  var stamp = Utilities.formatDate(new Date(), TZ, "MMM d, yyyy h:mm a") + " CT";
  var email = p.email || p.contact || "";
  var html = quoteTable(p, stamp);
  var text = plainBody(p, stamp);

  /* notify the lab */
  MailApp.sendEmail({
    to: NOTIFY,
    replyTo: email.indexOf("@") > -1 ? email : NOTIFY,
    subject: "TNT QUOTE — " + (p.name || "?") + " / " + (p.company || "?"),
    body: text,
    htmlBody: html
  });

  /* auto-acknowledge to the requester when they left an email */
  if (email.indexOf("@") > -1) {
    MailApp.sendEmail({
      to: email,
      subject: "TNT — quote request received",
      body: "We received your request:\n\n" + text +
            "\n\nOur lab desk responds within 1 business hour.\n" +
            "(972) 822-6494 · 2101 Gateway Dr, Irving, TX 75038\n\n" +
            "— Texas Nuclear Technologies",
      htmlBody:
        '<div style="font-family:Arial,sans-serif;font-size:14px;color:#c0c6ce;">' +
        '<p>We received your request:</p>' + html +
        '<p style="color:#8a94a6;">Our lab desk responds within 1 business hour.<br>' +
        '(972) 822-6494 · 2101 Gateway Dr, Irving, TX 75038</p>' +
        '<p style="color:#d4af37;">— Texas Nuclear Technologies</p></div>'
    });
  }

  return ContentService
    .createTextOutput(JSON.stringify({ success: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
