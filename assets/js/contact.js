/* TNT — Contact modal. Injects floating CONTACT US button + inquiry modal on every page. */
(function () {
  "use strict";

  var FS_ENDPOINT = "https://formsubmit.co/ajax/texas.nuclear.technologies@gmail.com";
  var MAIL = "texas.nuclear.technologies@gmail.com";

  function build() {
    var fab = document.createElement("button");
    fab.className = "contact-fab";
    fab.type = "button";
    fab.textContent = "CONTACT US";
    fab.setAttribute("aria-haspopup", "dialog");
    document.body.appendChild(fab);

    var modal = document.createElement("div");
    modal.className = "tnt-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-label", "Contact the lab");
    modal.innerHTML =
      '<div class="tnt-modal-back"></div>' +
      '<div class="tnt-modal-card">' +
        '<div class="tnt-modal-head"><b>CONTACT THE LAB</b><button type="button" class="tnt-modal-x" aria-label="Close">✕</button></div>' +
        '<div class="tnt-modal-body">' +
          '<p class="mm-note">TELL US ABOUT THE SAMPLE — RESPONSE WITHIN 1 BUSINESS HOUR</p>' +
          '<form class="mm-form" novalidate>' +
            '<div class="mm-grid">' +
              '<label class="mm-field"><span>NAME *</span><input type="text" name="name" required autocomplete="name"></label>' +
              '<label class="mm-field"><span>COMPANY</span><input type="text" name="company" autocomplete="organization"></label>' +
              '<label class="mm-field"><span>EMAIL *</span><input type="email" name="email" required autocomplete="email"></label>' +
              '<label class="mm-field"><span>PHONE</span><input type="tel" name="phone" autocomplete="tel"></label>' +
              '<label class="mm-field"><span>SAMPLE TYPE *</span>' +
                '<select name="sample_type" required>' +
                  '<option value="">SELECT…</option>' +
                  '<option>SUPPLEMENT / NUTRACEUTICAL</option>' +
                  '<option>FOOD / INGREDIENT</option>' +
                  '<option>BEVERAGE</option>' +
                  '<option>COSMETIC / PERSONAL CARE</option>' +
                  '<option>WATER / WASTEWATER</option>' +
                  '<option>OIL &amp; GAS / PETROLEUM</option>' +
                  '<option>SOIL / ENVIRONMENTAL</option>' +
                  '<option>PHARMA / OTC LOT</option>' +
                  '<option>UNKNOWN / OTHER</option>' +
                '</select></label>' +
              '<label class="mm-field"><span>SAMPLE COUNT</span><input type="number" name="quantity" min="1" value="1"></label>' +
              '<label class="mm-field full"><span>WHAT DO YOU NEED TESTED? *</span><textarea name="details" rows="3" required spellcheck="false"></textarea></label>' +
            '</div>' +
            '<button type="submit" class="mm-submit">SEND INQUIRY</button>' +
            '<input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">' +
          '</form>' +
          '<div class="mm-done" hidden>INQUIRY RECEIVED<br><b>RESPONSE WITHIN 1 BUSINESS HOUR</b><br>OR REACH US AT (972) 822-6494</div>' +
        '</div>' +
      '</div>';
    document.body.appendChild(modal);

    function open() { modal.classList.add("open"); document.body.style.overflow = "hidden"; }
    function close() { modal.classList.remove("open"); document.body.style.overflow = ""; }

    var pre = document.body.getAttribute("data-sample");
    if (pre) {
      var sel = form.querySelector('select[name="sample_type"]');
      if (sel) { for (var i = 0; i < sel.options.length; i++) {
        if (sel.options[i].text === pre) { sel.value = sel.options[i].text || sel.options[i].value; sel.selectedIndex = i; break; }
      } }
    }
    window.tntContact = open;
    fab.addEventListener("click", open);
    modal.querySelector(".tnt-modal-back").addEventListener("click", close);
    modal.querySelector(".tnt-modal-x").addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });

    var form = modal.querySelector(".mm-form");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = {};
      Array.prototype.forEach.call(new FormData(form).entries(), function (kv) { data[kv[0]] = kv[1]; });
      data._subject = "TNT Website Inquiry — " + (data.sample_type || "General");
      var btn = form.querySelector(".mm-submit");
      btn.textContent = "SENDING…"; btn.disabled = true;
      fetch(FS_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw 0;
        form.hidden = true;
        modal.querySelector(".mm-note").hidden = true;
        modal.querySelector(".mm-done").hidden = false;
      }).catch(function () {
        window.location.href = "mailto:" + MAIL + "?subject=" + encodeURIComponent(data._subject) +
          "&body=" + encodeURIComponent(JSON.stringify(data, null, 2));
        btn.textContent = "SEND INQUIRY"; btn.disabled = false;
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
