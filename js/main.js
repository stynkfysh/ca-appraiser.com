/* CA-Appraiser.com — shared behavior */
(function () {
  // Mobile nav toggle
  var toggle = document.querySelector(".mobile-nav-toggle");
  var nav = document.querySelector(".top-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
})();
