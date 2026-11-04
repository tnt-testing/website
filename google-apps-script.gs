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

function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ status: "ok", service: "tnt-quote" }))
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

function doPost(e) {
  var p = (e && e.parameter) || {};
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
