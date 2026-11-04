/**
 * TNT QUOTE BACKEND — Google Apps Script (free, runs on your Google account)
 * Receives quote submissions from the website and emails them to the lab.
 *
 * ─── DEPLOY (one time, ~5 min) ───────────────────────────────────────────
 * 1. Sign in to texas.nuclear.technologies@gmail.com
 * 2. Open https://script.google.com → "New project"
 * 3. Delete the default code, paste this entire file, press Save
 * 4. Click "Deploy" → "New deployment"
 * 5. Gear icon → type: "Web app"
 *      Execute as:        Me
 *      Who has access:    Anyone        ← required, the site posts here
 * 6. Click "Deploy" → authorize the app on the Gmail account →
 *    click "Advanced" → "Go to … (unsafe)" if Google warns → Allow
 * 7. Copy the Web app URL — it ends in  /exec
 *    Paste it into  assets/js/quote.js  where marked  GOOGLE_ENDPOINT
 *    (or send it to Devin and it will be wired + pushed for you)
 * ───────────────────────────────────────────────────────────────────────
 * Test after deploy: open the /exec URL in a browser →
 * you should see  {"status":"ok","service":"tnt-quote"}
 */

var NOTIFY = "texas.nuclear.technologies@gmail.com";

function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ status: "ok", service: "tnt-quote" }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  var p = (e && e.parameter) || {};

  var fields = ["name", "company", "contact", "test", "quantity",
                "turnaround", "estimate", "notes"];
  var lines = [];
  fields.forEach(function (k) {
    if (p[k]) lines.push(k.toUpperCase() + ":\t" + p[k]);
  });
  lines.push("SUBMITTED:\t" +
    Utilities.formatDate(new Date(), "America/Chicago", "MMM d, yyyy h:mm a") + " CT");

  /* notify the lab */
  MailApp.sendEmail({
    to: NOTIFY,
    replyTo: (p.contact && p.contact.indexOf("@") > -1) ? p.contact : NOTIFY,
    subject: "TNT QUOTE — " + (p.name || "?") + " / " + (p.company || "?"),
    body: "NEW QUOTE REQUEST — tnt-testing.github.io/website\n\n" +
          lines.join("\n") +
          "\n\n— submitted via live quote engine"
  });

  /* auto-acknowledge to the requester when they left an email */
  if (p.contact && p.contact.indexOf("@") > -1) {
    MailApp.sendEmail({
      to: p.contact,
      subject: "TNT — quote request received",
      body: "We received your request:\n\n" + lines.join("\n") +
            "\n\nOur lab desk responds within 1 business hour.\n\n" +
            "— Texas Nuclear Technologies"
    });
  }

  return ContentService
    .createTextOutput(JSON.stringify({ success: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
