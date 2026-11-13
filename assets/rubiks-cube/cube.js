
(function () {
  var root = document.getElementById("cube-lab");
  if (!root) return;
  var cfg = window.CUBE_PAGE || {};
  var slides = cfg.slides || [];
  var cards = cfg.cards || [];
  var slideIndex = 0;
  var cardIndex = 0;
  var filter = "all";
  var deck = cards.slice();

  function $(sel) { return root.querySelector(sel); }
  function $all(sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }

  function showSlide(i) {
    if (!slides.length) return;
    slideIndex = (i + slides.length) % slides.length;
    var img = $(".cube-slide-img");
    var cap = $(".cube-caption");
    img.src = slides[slideIndex].src;
    img.alt = slides[slideIndex].caption;
    cap.textContent = (slideIndex + 1) + " / " + slides.length + " — " + slides[slideIndex].caption;
    $all(".cube-dots button").forEach(function (b, n) {
      b.setAttribute("aria-current", n === slideIndex ? "true" : "false");
    });
  }

  function filtered() {
    if (filter === "all") return deck;
    var n = parseInt(filter, 10);
    return deck.filter(function (c) { return c.step === n; });
  }

  function stepLabel(step) {
    var names = {0:"Overview",1:"Step 1 · White Cross",2:"Step 2 · White Corners",3:"Step 3 · Middle Layer",4:"Step 4 · Yellow Cross",5:"Step 5 · Sune",6:"Step 6 · Niklas",7:"Step 7 · Orient Corners"};
    return names[step] || "Card";
  }

  function renderCard() {
    var list = filtered();
    if (!list.length) return;
    if (cardIndex >= list.length) cardIndex = 0;
    var c = list[cardIndex];
    var btn = $(".cube-flip");
    btn.classList.remove("is-flipped");
    btn.setAttribute("aria-pressed", "false");
    $(".cube-q").textContent = c.q;
    $(".cube-a").textContent = c.a;
    $all(".cube-kicker-q, .cube-kicker-a").forEach(function (el) {
      el.textContent = stepLabel(c.step);
    });
    $(".cube-progress").textContent = (cardIndex + 1) + " of " + list.length;
  }

  function flip() {
    var btn = $(".cube-flip");
    var on = !btn.classList.contains("is-flipped");
    btn.classList.toggle("is-flipped", on);
    btn.setAttribute("aria-pressed", on ? "true" : "false");
  }

  // slides
  var dots = $(".cube-dots");
  slides.forEach(function (_, n) {
    var b = document.createElement("button");
    b.type = "button";
    b.setAttribute("aria-label", "Slide " + (n + 1));
    b.addEventListener("click", function () { showSlide(n); });
    dots.appendChild(b);
  });
  $(".cube-prev-slide").addEventListener("click", function () { showSlide(slideIndex - 1); });
  $(".cube-next-slide").addEventListener("click", function () { showSlide(slideIndex + 1); });
  showSlide(0);

  // cards
  $all(".cube-filters button").forEach(function (b) {
    b.addEventListener("click", function () {
      filter = b.getAttribute("data-filter");
      $all(".cube-filters button").forEach(function (x) {
        x.setAttribute("aria-pressed", x === b ? "true" : "false");
      });
      cardIndex = 0;
      renderCard();
    });
  });
  $(".cube-flip").addEventListener("click", flip);
  $(".cube-prev-card").addEventListener("click", function () {
    var list = filtered();
    cardIndex = (cardIndex - 1 + list.length) % list.length;
    renderCard();
  });
  $(".cube-next-card").addEventListener("click", function () {
    var list = filtered();
    cardIndex = (cardIndex + 1) % list.length;
    renderCard();
  });
  $(".cube-shuffle").addEventListener("click", function () {
    for (var i = deck.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = deck[i]; deck[i] = deck[j]; deck[j] = t;
    }
    cardIndex = 0;
    renderCard();
  });
  root.addEventListener("keydown", function (e) {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
    if (e.key === " " || e.key === "Enter") {
      if (document.activeElement && document.activeElement.id === "cube-flip") return;
      e.preventDefault();
      flip();
    } else if (e.key === "ArrowRight") {
      e.preventDefault();
      $(".cube-next-card").click();
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      $(".cube-prev-card").click();
    }
  });
  renderCard();
})();
