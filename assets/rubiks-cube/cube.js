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

  function $(sel) {
    if (!sel) return null;
    if (sel.charAt(0) === "#") return document.getElementById(sel.slice(1));
    return (root || document).querySelector(sel);
  }
  function $all(sel) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }
  function on(sel, ev, fn) {
    var el = $(sel);
    if (el) el.addEventListener(ev, fn);
  }

  function showSlide(i) {
    if (!slides.length) return;
    slideIndex = (i + slides.length) % slides.length;
    var img = $("#cube-slide-img") || document.querySelector(".cube-slide-img");
    var cap = $("#cube-caption");
    if (img) {
      img.src = slides[slideIndex].src;
      img.alt = slides[slideIndex].caption;
    }
    if (cap) cap.textContent = (slideIndex + 1) + " / " + slides.length + " — " + slides[slideIndex].caption;
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
    var btn = $("#cube-flip");
    if (btn) {
      btn.classList.remove("is-flipped");
      btn.setAttribute("aria-pressed", "false");
    }
    var qEl = $("#cube-q") || document.querySelector(".cube-q");
    var aEl = $("#cube-a") || document.querySelector(".cube-a");
    if (qEl) qEl.textContent = c.q;
    if (aEl) aEl.textContent = c.a;
    $all(".cube-kicker-q, .cube-kicker-a").forEach(function (el) {
      el.textContent = stepLabel(c.step);
    });
    var prog = $("#cube-progress");
    if (prog) prog.textContent = (cardIndex + 1) + " of " + list.length;
  }

  function flip() {
    var btn = $("#cube-flip");
    if (!btn) return;
    var flipped = !btn.classList.contains("is-flipped");
    btn.classList.toggle("is-flipped", flipped);
    btn.setAttribute("aria-pressed", flipped ? "true" : "false");
  }

  var dots = $("#cube-dots") || document.querySelector(".cube-dots");
  if (dots) {
    slides.forEach(function (_, n) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Slide " + (n + 1));
      b.addEventListener("click", function () { showSlide(n); });
      dots.appendChild(b);
    });
  }
  on("#cube-prev-slide", "click", function () { showSlide(slideIndex - 1); });
  on("#cube-next-slide", "click", function () { showSlide(slideIndex + 1); });
  showSlide(0);

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
  on("#cube-flip", "click", flip);
  on("#cube-prev-card", "click", function () {
    var list = filtered();
    cardIndex = (cardIndex - 1 + list.length) % list.length;
    renderCard();
  });
  on("#cube-next-card", "click", function () {
    var list = filtered();
    cardIndex = (cardIndex + 1) % list.length;
    renderCard();
  });
  on("#cube-shuffle", "click", function () {
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
      var next = $("#cube-next-card");
      if (next) next.click();
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      var prev = $("#cube-prev-card");
      if (prev) prev.click();
    }
  });
  renderCard();
})();
