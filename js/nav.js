/* Lightweight active-nav helper */
document.addEventListener("DOMContentLoaded", () => {
  const path = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".site-nav a").forEach((a) => {
    const href = a.getAttribute("href") || "";
    if (href.endsWith(path) || (path === "index.html" && href.includes("index.html") && !href.includes("#"))) {
      a.setAttribute("aria-current", "page");
    }
  });
});
