/* ASDG — interactions
   Kept dependency-free and progressive: everything degrades gracefully. */

(function () {
  "use strict";

  /* ----- Sticky header shadow ----- */
  const header = document.querySelector(".site-header");
  if (header) {
    const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ----- Mobile nav ----- */
  const toggle = document.querySelector(".nav__toggle");
  const menu = document.querySelector(".nav__menu");
  const overlay = document.querySelector(".nav-overlay");

  const closeMenu = () => {
    menu && menu.classList.remove("open");
    overlay && overlay.classList.remove("show");
    document.body.style.overflow = "";
  };
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const open = menu.classList.toggle("open");
      overlay && overlay.classList.toggle("show", open);
      document.body.style.overflow = open ? "hidden" : "";
    });
  }
  overlay && overlay.addEventListener("click", closeMenu);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeMenu(); });

  /* Mobile dropdown accordions (only intercept on small screens) */
  document.querySelectorAll(".nav__item.has-drop > .nav__link").forEach((link) => {
    link.addEventListener("click", (e) => {
      if (window.innerWidth <= 860) {
        e.preventDefault();
        const item = link.closest(".nav__item");
        item.classList.toggle("open-sub");
      }
    });
  });

  /* ----- Hero slider ----- */
  const slides = document.querySelectorAll(".hero__slide");
  const dots = document.querySelectorAll(".hero__dot");
  if (slides.length > 1) {
    let i = 0;
    let timer;
    const go = (n) => {
      slides[i].classList.remove("active");
      dots[i] && dots[i].classList.remove("active");
      i = (n + slides.length) % slides.length;
      slides[i].classList.add("active");
      dots[i] && dots[i].classList.add("active");
    };
    const start = () => { timer = setInterval(() => go(i + 1), 5500); };
    const stop = () => clearInterval(timer);
    dots.forEach((dot, idx) => dot.addEventListener("click", () => { stop(); go(idx); start(); }));
    start();
  }

  /* ----- Reveal on scroll ----- */
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("in"));
  }

  /* ----- Publication filter ----- */
  const filterBtns = document.querySelectorAll(".pub-filter button");
  const pubs = document.querySelectorAll(".pub");
  if (filterBtns.length && pubs.length) {
    filterBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        filterBtns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const f = btn.dataset.filter;
        pubs.forEach((p) => {
          const show = f === "all" || p.dataset.type === f;
          p.style.display = show ? "" : "none";
        });
      });
    });
  }

  /* ----- Contact form (demo only, no backend) ----- */
  const form = document.querySelector("#contact-form");
  if (form) {
    const note = form.querySelector(".form-note");
    form.querySelector("button[type=submit]").addEventListener("click", (e) => {
      e.preventDefault();
      const inputs = form.querySelectorAll("input[required], textarea[required]");
      let ok = true;
      inputs.forEach((inp) => { if (!inp.value.trim()) { inp.style.borderColor = "var(--red)"; ok = false; } });
      if (note) {
        note.textContent = ok
          ? "Thanks — this is a demo form. Connect it to Formspree, Netlify Forms, or your backend to receive messages."
          : "Please fill in the required fields.";
        note.style.color = ok ? "var(--red)" : "var(--red-dark)";
      }
    });
  }

  /* ----- Footer year ----- */
  const yearEl = document.querySelector("#year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
