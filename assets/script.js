// Radar IA — small interactions
document.addEventListener("DOMContentLoaded", function () {
  // reveal cards on scroll
  var cards = document.querySelectorAll(".card");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("reveal");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    cards.forEach(function (c) {
      io.observe(c);
    });
  } else {
    cards.forEach(function (c) {
      c.classList.add("reveal");
    });
  }

  // mobile nav toggle
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector("nav.main");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.style.display = nav.style.display === "flex" ? "none" : "flex";
      nav.style.flexDirection = "column";
      nav.style.position = "absolute";
      nav.style.top = "64px";
      nav.style.right = "24px";
      nav.style.background = "#14161f";
      nav.style.border = "1px solid #22242f";
      nav.style.borderRadius = "12px";
      nav.style.padding = "16px 20px";
    });
  }

  // reading progress bar (article pages only)
  var bar = document.querySelector(".reading-progress");
  if (bar) {
    window.addEventListener("scroll", function () {
      var h = document.documentElement;
      var scrolled = (h.scrollTop) / (h.scrollHeight - h.clientHeight) * 100;
      bar.style.width = scrolled + "%";
    });
  }
});
