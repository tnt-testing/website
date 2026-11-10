/* ============================================================
   TNT — quote.js
   Live quote request builder (client-side — no pricing shown;
   every request is priced and confirmed by the lab desk).
   Isomorphic: contains no import/export tokens so it can be
   loaded as a classic script (file://) OR side-effect imported
   as an ES module.
   ============================================================ */

(function () {
  "use strict";

  /* ---------- CATALOG (edit here) ---------- */
  var TESTS = [
    { id: "oilgas",   name: "OIL & GAS IMPURITY",         sub: "ORBITRAP HRAM" },
    { id: "unknown",  name: "UNKNOWN COMPOUND ID",        sub: "ORBITRAP HRAM" },
    { id: "water",    name: "WATER & WASTEWATER",         sub: "ICP-MS"        },
    { id: "pharma",   name: "PHARMA & SUPPLEMENTS",       sub: "LC-MS/MS"      },
    { id: "soil",     name: "SOIL & DIRT",                sub: "ICP-MS"        },
    { id: "metals",   name: "HEAVY METALS",               sub: "ICP-MS"        },
    { id: "minerals", name: "MINERALS & NUTRIENTS",       sub: "ICP-MS"        },
    { id: "pfas",     name: "PESTICIDES · PFAS",          sub: "LC-MS/MS"      },
    { id: "solvents", name: "SOLVENTS · VOCs · TERPENES", sub: "GC-MS"         },
    { id: "cosmetics",name: "COSMETICS & CARE",           sub: "GC-MS"         }
  ];

  var TAT = { standard: "24–48 HR", rush: "< 24 HR" };

  var pad = function (n) {
    return n < 10 ? "0" + n : String(n);
  };

  /* ---------- ENGINE ---------- */
  function initQuote(root) {
    if (!root || root.__tntBound) return;
    root.__tntBound = true;

    var state = { test: TESTS[0], qty: 1, tat: "standard" };

    var $ = function (sel) { return root.querySelector(sel); };

    var testBox  = $("#testOptions"),
        qtyRange = $("#qtyRange"),
        qtyOut   = $("#qtyOut"),
        roScreen = $("#roScreen"),
        roTest   = $("#roTest"),
        roMethod = $("#roMethod"),
        roQty    = $("#roQty"),
        roTat    = $("#roTat"),
        roTatBig = $("#roTatBig"),
        form     = $("#quoteForm"),
        done     = $("#quoteDone"),
        submitBtn= $("#submitBtn"),
        resetBtn = $("#resetBtn"),
        qdRef    = $("#qdRef"),
        qdEst    = $("#qdEst");

    /* --- build test selector --- */
    TESTS.forEach(function (t, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "test-opt" + (i === 0 ? " is-on" : "");
      b.setAttribute("role", "radio");
      b.setAttribute("aria-checked", i === 0 ? "true" : "false");
      b.dataset.test = t.id;
      b.innerHTML =
        '<span class="led"></span>' +
        '<span class="to-name">' + t.name + "<small>" + t.sub + "</small></span>" +
        '<span class="to-arrow">&rsaquo;</span>';
      b.addEventListener("click", function () {
        state.test = t;
        testBox.querySelectorAll(".test-opt").forEach(function (el) {
          var on = el === b;
          el.classList.toggle("is-on", on);
          el.setAttribute("aria-checked", on ? "true" : "false");
        });
        render();
      });
      testBox.appendChild(b);
    });

    /* --- qty slider --- */
    var syncFill = function () {
      var min = +qtyRange.min, max = +qtyRange.max, v = +qtyRange.value;
      qtyRange.style.setProperty("--fill", ((v - min) / (max - min)) * 100 + "%");
    };
    qtyRange.addEventListener("input", function () {
      state.qty = +qtyRange.value;
      qtyOut.textContent = pad(state.qty);
      syncFill();
      render();
    });

    /* --- turnaround toggle --- */
    root.querySelectorAll(".tat-btn").forEach(function (b) {
      b.addEventListener("click", function () {
        state.tat = b.dataset.tat;
        root.querySelectorAll(".tat-btn").forEach(function (el) {
          var on = el === b;
          el.classList.toggle("is-on", on);
          el.setAttribute("aria-checked", on ? "true" : "false");
        });
        render();
      });
    });

    /* --- render --- */
    function render() {
      roTest.textContent = state.test.name;
      roMethod.textContent = state.test.sub;
      roQty.textContent  = "× " + pad(state.qty);
      roTat.textContent = TAT[state.tat];
      roTatBig.textContent = TAT[state.tat];

      // brief "analysis" shimmer
      roScreen.classList.remove("computing");
      void roScreen.offsetWidth;
      roScreen.classList.add("computing");
    }

    /* --- submit (Google Apps Script → lab inbox; FormSubmit fallback) --- */
    var GOOGLE_ENDPOINT = "https://script.google.com/macros/s/AKfycbxkbQmAwpDNOkrYvhp3xfjSLMXrpi4T4eBqJJm9VA6YbNzOPHFSjc0FglkG1DgCRmC7/exec";
    var FS_ENDPOINT = "https://formsubmit.co/ajax/texas.nuclear.technologies@gmail.com";
    var formError = $("#formError");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll("input[required]").forEach(function (inp) {
        var bad = !inp.value.trim();
        inp.classList.toggle("err", bad);
        if (bad) ok = false;
      });
      if (!ok) return;

      submitBtn.classList.add("working");
      if (formError) formError.hidden = true;
      var fd = new FormData(form);
      var name = (fd.get("name") || "").toString().trim();
      var company = (fd.get("company") || "").toString().trim();
      var email = (fd.get("email") || "").toString().trim();
      var phone = (fd.get("phone") || "").toString().trim();

      var payload = {
        name: name,
        company: company,
        email: email,
        phone: phone,
        contact: email,
        notes: (fd.get("notes") || "").toString().trim(),
        test: state.test.name + " (" + state.test.sub + ")",
        quantity: String(state.qty),
        turnaround: state.tat === "rush" ? "RUSH — UNDER 24 HR" : "STANDARD — 24–48 HR",
        _subject: "TNT QUOTE REQUEST — " + name + " / " + company,
        _template: "table",
        _captcha: "false",
        _honey: ""
      };
      if (email.indexOf("@") !== -1) payload._replyto = email;

      var showDone = function () {
        qdRef.textContent =
          "TNT-" + Math.random().toString(36).slice(2, 7).toUpperCase();
        qdEst.textContent =
          state.test.name + " ×" + state.qty + " · " +
          (state.tat === "rush" ? "RUSH <24 HR" : "24–48 HR");
        form.hidden = true;
        done.hidden = false;
        done.scrollIntoView({ behavior: "smooth", block: "nearest" });
      };
      var showError = function () {
        submitBtn.classList.remove("working");
        if (formError) formError.hidden = false;
      };

      if (GOOGLE_ENDPOINT) {
        /* Apps Script web app: form-encoded POST, no-cors (opaque = assume sent) */
        var ctrl = new AbortController();
        var timeout = window.setTimeout(function () { ctrl.abort(); }, 12000);
        fetch(GOOGLE_ENDPOINT, {
          method: "POST",
          mode: "no-cors",
          body: new URLSearchParams(payload),
          signal: ctrl.signal
        })
          .then(function () { window.clearTimeout(timeout); showDone(); })
          .catch(showError);
      } else {
        var ctrl2 = new AbortController();
        var timeout2 = window.setTimeout(function () { ctrl2.abort(); }, 12000);
        fetch(FS_ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/json", "Accept": "application/json" },
          body: JSON.stringify(payload),
          signal: ctrl2.signal
        })
          .then(function (res) { window.clearTimeout(timeout2); return res.json(); })
          .then(function (out) {
            if (String(out.success) !== "true") throw new Error("rejected");
            showDone();
          })
          .catch(showError);
      }
    });

    form.querySelectorAll("input").forEach(function (inp) {
      inp.addEventListener("input", function () { inp.classList.remove("err"); });
    });

    resetBtn.addEventListener("click", function () {
      done.hidden = true;
      form.hidden = false;
      form.reset();
      submitBtn.classList.remove("working");
    });

    syncFill();
    render();
  }

  /* ---------- export surface + auto-boot ---------- */
  window.TNT_QUOTE = { TESTS: TESTS, initQuote: initQuote };

  function boot() {
    initQuote(document.getElementById("quoteModule"));
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
