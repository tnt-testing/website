/* TNT — inline RFQ forms (.rfq-form) on sector hub pages. Posts to FormSubmit, mailto fallback. */
(function () {
  "use strict";

  var FS_ENDPOINT = "https://formsubmit.co/ajax/quotes@tnt-labs.com";
  var MAIL = "quotes@tnt-labs.com";

  function collect(form) {
    var data = {};
    Array.prototype.forEach.call(new FormData(form).entries(), function (kv) {
      var k = kv[0], v = String(kv[1]);
      if (k === "_honey" || !v) return;
      if (data[k]) data[k] = Array.isArray(data[k]) ? data[k].concat(v) : [data[k], v];
      else data[k] = v;
    });
    return data;
  }

  function bind(form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = collect(form);
      data._subject = form.getAttribute("data-subject") || "TNT Website RFQ";
      var btn = form.querySelector(".mm-submit");
      var done = form.parentNode.querySelector(".rfq-done");
      btn.textContent = "SENDING…"; btn.disabled = true;
      fetch(FS_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw 0;
        form.hidden = true;
        if (done) done.hidden = false;
      }).catch(function () {
        window.location.href = "mailto:" + MAIL + "?subject=" + encodeURIComponent(data._subject) +
          "&body=" + encodeURIComponent(JSON.stringify(data, null, 2));
        btn.textContent = "SEND REQUEST"; btn.disabled = false;
      });
    });
  }

  function init() {
    var forms = document.querySelectorAll(".rfq-form");
    Array.prototype.forEach.call(forms, bind);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
