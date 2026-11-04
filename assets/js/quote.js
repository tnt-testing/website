/* ============================================================
   TNT — quote.js
   Live pricing engine (client-side, indicative estimates only)
   Isomorphic: contains no import/export tokens so it can be
   loaded as a classic script (file://) OR side-effect imported
   as an ES module. All pricing data lives in PRICING below.
   ============================================================ */

(function () {
  "use strict";

  /* ---------- PRICING CONFIG (edit here) ---------- */
  var PRICING = {
    currency: "USD",
    rushMultiplier: 1.5,
    volumeDiscounts: [
      { min: 25, off: 0.10 },
      { min: 10, off: 0.05 }
    ],
    tests: [
      { id: "oilgas",   name: "OIL & GAS IMPURITY",         sub: "ORBITRAP HRAM", fee: 1000 },
      { id: "unknown",  name: "UNKNOWN COMPOUND ID",        sub: "ORBITRAP HRAM", fee: 600  },
      { id: "metals",   name: "HEAVY METALS",               sub: "ICP-MS",        fee: 250  },
      { id: "minerals", name: "MINERALS & NUTRIENTS",       sub: "ICP-MS",        fee: 250  },
      { id: "pfas",     name: "PESTICIDES · PFAS",          sub: "LC-MS/MS",      fee: 300  },
      { id: "solvents", name: "SOLVENTS · VOCs · TERPENES", sub: "GC-MS",         fee: 200  }
    ]
  };

  var money = function (n) {
    return "$" + Math.round(n).toLocaleString("en-US");
  };
  var pad = function (n) {
    return n < 10 ? "0" + n : String(n);
  };

  function discountFor(qty) {
    for (var i = 0; i < PRICING.volumeDiscounts.length; i++) {
      if (qty >= PRICING.volumeDiscounts[i].min) return PRICING.volumeDiscounts[i].off;
    }
    return 0;
  }

  /* ---------- ENGINE ---------- */
  function initQuote(root) {
    if (!root || root.__tntBound) return;
    root.__tntBound = true;

    var state = { test: PRICING.tests[0], qty: 1, tat: "standard", shown: 0 };

    var $ = function (sel) { return root.querySelector(sel); };

    var testBox  = $("#testOptions"),
        qtyRange = $("#qtyRange"),
        qtyOut   = $("#qtyOut"),
        discHint = $("#discHint"),
        roScreen = $("#roScreen"),
        roTest   = $("#roTest"),
        roUnit   = $("#roUnit"),
        roQty    = $("#roQty"),
        roDisc   = $("#roDisc"),
        roMult   = $("#roMult"),
        roTotal  = $("#roTotal"),
        form     = $("#quoteForm"),
        done     = $("#quoteDone"),
        submitBtn= $("#submitBtn"),
        resetBtn = $("#resetBtn"),
        qdRef    = $("#qdRef"),
        qdEst    = $("#qdEst");

    /* --- build test selector --- */
    PRICING.tests.forEach(function (t, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "test-opt" + (i === 0 ? " is-on" : "");
      b.setAttribute("role", "radio");
      b.setAttribute("aria-checked", i === 0 ? "true" : "false");
      b.dataset.test = t.id;
      b.innerHTML =
        '<span class="led"></span>' +
        '<span class="to-name">' + t.name + "<small>" + t.sub + "</small></span>" +
        '<span class="to-fee">' + money(t.fee) + "</span>";
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

    /* --- compute + render --- */
    var raf = null;
    function compute() {
      var unit = state.test.fee;
      var disc = discountFor(state.qty);
      var mult = state.tat === "rush" ? PRICING.rushMultiplier : 1;
      var total = unit * state.qty * mult * (1 - disc);
      return { unit: unit, disc: disc, mult: mult, total: total };
    }

    function countUp(from, to) {
      if (raf) cancelAnimationFrame(raf);
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        roTotal.textContent = money(to);
        state.shown = to;
        return;
      }
      var t0 = performance.now(), dur = 520;
      var step = function (t) {
        var p = Math.min((t - t0) / dur, 1);
        var e = 1 - Math.pow(1 - p, 3); // ease-out cubic
        var v = from + (to - from) * e;
        roTotal.textContent = money(v);
        if (p < 1) raf = requestAnimationFrame(step);
        else state.shown = to;
      };
      raf = requestAnimationFrame(step);
    }

    function render() {
      var r = compute();
      roTest.textContent = state.test.name;
      roUnit.textContent = money(r.unit);
      roQty.textContent  = "× " + pad(state.qty);
      roDisc.textContent = r.disc > 0 ? "−" + Math.round(r.disc * 100) + "%" : "—";
      roMult.textContent = "×" + r.mult.toFixed(2);
      discHint.classList.toggle("active", r.disc > 0);

      // brief "analysis" shimmer + count-up
      roScreen.classList.remove("computing");
      void roScreen.offsetWidth;
      roScreen.classList.add("computing");
      countUp(state.shown, r.total);
    }

    /* --- submit (Google Apps Script → lab inbox; FormSubmit fallback) --- */
    var GOOGLE_ENDPOINT = ""; // ← paste deployed Apps Script /exec URL here
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
      var r = compute();
      var fd = new FormData(form);
      var name = (fd.get("name") || "").toString().trim();
      var company = (fd.get("company") || "").toString().trim();
      var contact = (fd.get("contact") || "").toString().trim();

      var payload = {
        name: name,
        company: company,
        contact: contact,
        notes: (fd.get("notes") || "").toString().trim(),
        test: state.test.name + " (" + state.test.sub + ")",
        quantity: String(state.qty),
        turnaround: state.tat === "rush" ? "RUSH — 24 HR" : "STANDARD — 48 HR",
        estimate: money(r.total),
        _subject: "TNT QUOTE REQUEST — " + name + " / " + company,
        _template: "table",
        _captcha: "false",
        _honey: ""
      };
      if (contact.indexOf("@") !== -1) payload._replyto = contact;

      var showDone = function () {
        qdRef.textContent =
          "TNT-" + Math.random().toString(36).slice(2, 7).toUpperCase();
        qdEst.textContent =
          state.test.name + " ×" + state.qty +
          (state.tat === "rush" ? " · RUSH" : "") + " — " + money(r.total);
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
  window.TNT_QUOTE = { PRICING: PRICING, initQuote: initQuote };

  function boot() {
    initQuote(document.getElementById("quoteModule"));
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
