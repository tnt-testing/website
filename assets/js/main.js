/* ============================================================
   TNT — main.js
   Nav state · mobile menu · scroll reveals
   Note: quote engine lives in assets/js/quote.js and is also
   side-effect imported via <script type="module"> in index.html
   (import './assets/js/quote.js') — quote.js is import-safe.
   ============================================================ */

(function () {
  "use strict";

  if (window.__TNT_BOOTED) return;
  window.__TNT_BOOTED = true;

  function init() {
    /* --- nav state on scroll --- */
    var nav = document.querySelector(".nav");
    var onScroll = function () {
      nav.classList.toggle("scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    /* --- mobile menu --- */
    var toggle = document.querySelector(".nav-toggle");
    var menu = document.getElementById("mobileMenu");
    if (toggle && menu) {
      var setMenu = function (open) {
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        menu.hidden = !open;
      };
      toggle.addEventListener("click", function () {
        setMenu(toggle.getAttribute("aria-expanded") !== "true");
      });
      menu.querySelectorAll("a").forEach(function (a) {
        a.addEventListener("click", function () { setMenu(false); });
      });
      window.addEventListener("resize", function () {
        if (window.innerWidth > 1150) setMenu(false);
      });
    }

    /* --- scroll reveals --- */
    var els = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add("in");
            io.unobserve(en.target);
          }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
      els.forEach(function (el) { io.observe(el); });
    } else {
      els.forEach(function (el) { el.classList.add("in"); });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
