#!/usr/bin/env python3
"""Build Sam News Reporter Teleprompts static site from topic-pack JSON."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from money_articles import (
    MONEY_ARTICLES,
    MONEY_EDITION,
    MONEY_SECTION,
    MONEY_SECTION_KEY,
    money_markdown,
)

SITE_ROOT = Path(__file__).resolve().parent.parent


def _resolve_topic_packs() -> Path:
    """Cloud form uses /cursor/stores/self; Jarvis maps the Project store under agent-stores."""
    candidates = [
        Path("/cursor/stores/self/internal/topic-packs"),
        Path("/cursor/stores/bc-3c8fd4a3-1d76-4b8f-b89a-57d64f841d5b/internal/topic-packs"),
        Path(
            "/home/sandcastle/.local/state/cursor/agent-stores/cursor_agent_stores/"
            "bc-3c8fd4a3-1d76-4b8f-b89a-57d64f841d5b/files/internal/topic-packs"
        ),
        SITE_ROOT.parent.parent / "internal" / "topic-packs",
    ]
    for c in candidates:
        if c.is_dir() and any(c.glob("*.json")):
            return c
    return candidates[0]


TOPIC_PACKS = _resolve_topic_packs()
EDITION_DATE = "Tuesday, October 27, 2026"
EDITION_SHORT = "Oct 27, 2026"
EDITION_ISO = "2026-10-27"
BRAND = "Sam News Reporter Teleprompts"
BYLINE = "Sam Castillo"
SITE_TAGLINE = "Teleprompt briefings distilled from the day's research wire."
SITE_URL = "https://sam-news-reporter-teleprompts.vercel.app"
# After rebuild, run scripts/patch_seo_meta.py for per-article keywords, OG/Twitter,
# canonical URLs, and Topics chips (preserves hand-curated pages like disney-fox).

SECTION_MAP = {
    "artificial-intelligence-in-fiction": ("Science & Ideas", "science"),
    "quantum-entanglement": ("Science & Ideas", "science"),
    "molecular-biology-central-dogma": ("Science & Ideas", "science"),
    "base-rate-fallacy-in-politics": ("Politics & Media", "politics"),
    "election-misinformation-and-media": ("Politics & Media", "politics"),
    "us-saudi-arabia-and-houthi-conflict": ("World", "world"),
    "public-safety-and-crime-news": ("World", "world"),
    "fifa-world-cup-2026": ("Sport", "sport"),
    "running-and-fitness": ("Sport", "sport"),
    "hawaii-travel": ("Travel & Life", "life"),
    "creative-donut-flavors": ("Travel & Life", "life"),
    "christian-faith-and-family": ("Travel & Life", "life"),
    "homeowners-and-mortgage-rates": ("Economy", "economy"),
    "guitar-songwriting-and-rock-music": ("Arts & Culture", "arts"),
    "iconic-artists-and-folk-heroes": ("Arts & Culture", "arts"),
    "dolphins-and-ocean-life": ("Environment", "environment"),
    "titanic-and-famous-maritime-disasters": ("Environment", "environment"),
    "federal-money-patterns-ma": ("Follow the Money", "money"),
    "party-line-voting-99-percent": ("Follow the Money", "money"),
    "ma-ocpf-sabadosa-comerford-healey": ("Follow the Money", "money"),
    "congress-rollcalls-markey-warren-pac": ("Follow the Money", "money"),
    "how-to-read-campaign-finance-db": ("Follow the Money", "money"),
    "actblue-winred-vs-direct": ("Follow the Money", "money"),
}

SECTION_ORDER = [
    "Follow the Money",
    "Politics & Media",
    "World",
    "Science & Ideas",
    "Sport",
    "Economy",
    "Arts & Culture",
    "Travel & Life",
    "Environment",
]


def slugify_title(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s[:80] or "article"


def clean_snippet(snippet: str) -> str:
    if not snippet:
        return ""
    text = snippet.replace("\r\n", "\n").replace("\r", "\n")
    # Drop markdown-ish heading markers and bullet ornaments from scrapes
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^#+\s*", "", line)
        line = re.sub(r"^[-*]\s+\*?\*?", "", line)
        line = line.replace("**", "")
        lines.append(line)
    # Deduplicate near-identical consecutive lines; drop mid-cut scraps
    deduped = []
    seen = set()
    for line in lines:
        if len(line) < 28 and not line.endswith((".", "?", "!", '"', "”")):
            # Likely truncated scrape fragment (e.g. "The research, le")
            continue
        key = re.sub(r"\s+", " ", line.lower())[:120]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(line)
    return "\n\n".join(deduped)


def human_topic_title(slug: str, query: str) -> str:
    # Prefer a clean topic title from the slug
    words = slug.replace("-", " ").title()
    # Fix small words / acronyms
    fixes = {
        "Ai": "AI",
        "Fifa": "FIFA",
        "Us": "US",
        "And": "and",
        "In": "in",
        "Of": "of",
        "The": "the",
    }
    parts = words.split()
    out = []
    for i, p in enumerate(parts):
        if i == 0:
            out.append(fixes.get(p, p) if p != "The" else "The")
        else:
            out.append(fixes.get(p, p))
    title = " ".join(out)
    # Capitalize first letter always
    return title[0].upper() + title[1:] if title else query


def clean_headline(title: str) -> str:
    t = (title or "").strip()
    t = re.split(r"\s+[|]\s+", t)[0].strip()
    t = re.sub(r"^(title|abstract)\s*:\s*", "", t, flags=re.I)
    # Drop common publisher / database suffixes
    t = re.sub(
        r"\s+[-–—]\s+(PubMed|CERN|The Economic Times|Reuters|News and features|Florida Atlantic University|Beacon Press|PMC)\s*$",
        "",
        t,
        flags=re.I,
    )
    # Collapse scrape truncations ending in ellipsis dots
    t = re.sub(r"\s*\.{2,}\s*$", "", t)
    t = re.sub(r"\s*[–—]\s*$", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    # Tidy leftover comma spacing from slugs
    t = re.sub(r"\s+,", ",", t)
    return t


def headline_from_snippet(snippet: str) -> list[str]:
    """Collect markdown-style headings buried in the scrape."""
    found: list[str] = []
    if not snippet:
        return found
    for line in snippet.replace("\r\n", "\n").split("\n"):
        line = line.strip()
        m = re.match(r"^#{1,3}\s+(.+)$", line)
        if m:
            h = clean_headline(m.group(1))
            if h:
                found.append(h)
    return found


def headline_from_url(url: str) -> str | None:
    """Recover a full title from a descriptive slug when the scrape title was truncated."""
    if not url:
        return None
    path = re.sub(r"[?#].*$", "", url).rstrip("/")
    slug = path.split("/")[-1]
    slug = re.sub(r"\.html?$", "", slug, flags=re.I)
    if slug.count("-") < 5:
        return None
    if re.fullmatch(r"[\d-]+", slug):
        return None
    # Skip arXiv / repository path crumbs
    if any(x in path.lower() for x in ("/abs/", "/pdf/", "arxiv.org", "research-portal", "beaconpress")):
        return None
    words = [w for w in slug.split("-") if w]
    if len(words) < 6:
        return None
    # Title-case while keeping short tokens / digits
    titled = []
    for w in words:
        if w.isdigit():
            titled.append(w)
        elif w.lower() in {"a", "an", "the", "and", "or", "of", "for", "to", "in", "on", "by", "as", "at"}:
            titled.append(w.lower())
        elif w.isupper() or w in {"ATLAS", "CMS", "FIFA", "LED", "UH", "UK", "US"}:
            titled.append(w)
        else:
            titled.append(w.capitalize())
    if titled:
        titled[0] = titled[0].capitalize() if not titled[0].isdigit() else titled[0]
    return clean_headline(" ".join(titled))


def looks_truncated(title: str) -> bool:
    t = title.strip()
    if t.endswith(("...", "…")):
        return True
    # Ends mid-phrase: single capital letter / bare connector
    if re.search(r"\b(Z|A|The|and|of|for|to|in|on|between)\s*$", t):
        return True
    if t.endswith(("'", "'s", "’s")) and len(t) < 90:
        # "Governor Newsom's" cut off
        return True
    return False


def is_weak_headline(title: str) -> bool:
    if not title or len(title) < 16:
        return True
    if looks_truncated(title):
        return True
    low = title.lower().strip()
    weak_patterns = [
        r"^september:",
        r"^running\s*[–—-]",
        r"news,? research and analysis",
        r"^woody guthrie$",
        r"^\'?snooping\'? on dolphins$",
        r"^www\.",
        r"press releases?$",
        r"computer science\s*>",
        r"research portal",
        r"beacon press",
        r"^hotspots for food",
        r"^crime and society$",
        r"^crime prevention$",
        r"computation and language",
        r"^(abstract|biography|personal profile)$",
        r"^an intimate life$",
        r"^jan herbst$",
        r"evocaciones del",
        r"바닷속|코리아|bbc news",
    ]
    if any(re.search(p, low) for p in weak_patterns):
        return True
    # Skip headings that are mostly non-Latin if we have alternatives later
    letters = re.findall(r"[A-Za-z]", title)
    if len(letters) < 8 and re.search(r"[^\x00-\x7F]", title):
        return True
    return False


def score_headline(title: str, hit_index: int) -> tuple:
    """Lower tuple sorts first — favor earlier hits and readable length."""
    length = len(title)
    length_penalty = 0
    if length < 22:
        length_penalty = 2
    elif length > 125:
        length_penalty = 1
    return (1 if is_weak_headline(title) else 0, hit_index, length_penalty, -min(length, 90))


def article_headline(pack: dict) -> str:
    hits = pack.get("hits") or []
    topic_fallback = human_topic_title(pack["slug"], pack.get("query", ""))

    scored: list[tuple[tuple, str]] = []
    seen: set[str] = set()

    def add(title: str, hit_index: int) -> None:
        t = clean_headline(title)
        if not t:
            return
        key = t.lower()
        if key in seen:
            return
        seen.add(key)
        scored.append((score_headline(t, hit_index), t))

    for i, hit in enumerate(hits):
        snips = headline_from_snippet(hit.get("snippet") or "")
        # Pair H1 + following H2 when H1 is a short proper name
        if len(snips) >= 2 and len(snips[0].split()) <= 3 and not is_weak_headline(f"{snips[0]}: {snips[1]}"):
            add(f"{snips[0]}: {snips[1]}", i)
        for snip_h in snips:
            add(snip_h, i)
        raw_title = hit.get("title") or ""
        add(raw_title, i)
        t = clean_headline(raw_title)
        if looks_truncated(t) or looks_truncated(raw_title):
            url_h = headline_from_url(hit.get("url") or "")
            if url_h:
                add(url_h, i)

    if scored:
        scored.sort(key=lambda x: x[0])
        best = scored[0][1]
        if not is_weak_headline(best):
            if len(best) > 160:
                return best[:157].rsplit(" ", 1)[0] + "…"
            return best
        for _, t in scored:
            if not is_weak_headline(t):
                return t if len(t) <= 160 else t[:157].rsplit(" ", 1)[0] + "…"

    return f"{topic_fallback}: research wire briefing"


def article_dek(pack: dict) -> str:
    hits = pack.get("hits") or []
    if hits:
        snip = clean_snippet(hits[0].get("snippet") or "")
        if snip:
            first = snip.split("\n\n")[0]
            # Cap dek length
            if len(first) > 220:
                first = first[:217].rsplit(" ", 1)[0] + "…"
            return first
    q = pack.get("query", "")
    return f"A research wire briefing on {q}."


def build_markdown(pack: dict) -> str:
    slug = pack["slug"]
    section, _ = SECTION_MAP.get(slug, ("Briefings", "briefings"))
    headline = article_headline(pack)
    dek = article_dek(pack)
    topic = human_topic_title(slug, pack.get("query", ""))
    lines = [
        f"# {headline}",
        "",
        f"**{BRAND}** · {BYLINE} · {EDITION_SHORT}",
        "",
        f"*Section:* {section}  ",
        f"*Topic:* {topic}  ",
        f"*Wire query:* {pack.get('query', '')}",
        "",
        dek,
        "",
        "## On the wire",
        "",
        "The following items are drawn directly from the research seed for this topic. "
        "Headlines and excerpts below reflect source material; no additional facts have been invented.",
        "",
    ]
    for i, hit in enumerate(pack.get("hits") or [], 1):
        title = (hit.get("title") or f"Source {i}").strip()
        url = (hit.get("url") or "").strip()
        body = clean_snippet(hit.get("snippet") or "")
        lines.append(f"### {i}. {title}")
        lines.append("")
        if body:
            for para in body.split("\n\n"):
                lines.append(para)
                lines.append("")
        if url:
            lines.append(f"[Source link]({url})")
            lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        f"*Teleprompt edition for {EDITION_DATE}. Reporting brand: {BYLINE} / {BRAND}.*"
    )
    lines.append("")
    return "\n".join(lines)



def is_md_table_separator(line: str) -> bool:
    s = line.strip()
    if "|" not in s:
        return False
    cells = [c.strip() for c in s.strip("|").split("|")]
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells)


def parse_md_table_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def render_md_table(header: str, rows: list[str], render_inline) -> str:
    heads = parse_md_table_row(header)
    out = ['<div class="table-wrap"><table>', "<thead><tr>"]
    for h in heads:
        out.append(f"<th>{render_inline(h)}</th>")
    out.append("</tr></thead><tbody>")
    for row in rows:
        cells = parse_md_table_row(row)
        out.append("<tr>")
        for i, h in enumerate(heads):
            cell = cells[i] if i < len(cells) else ""
            out.append(f"<td>{render_inline(cell)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def md_to_article_html_body(md: str) -> str:
    """Minimal markdown → HTML for our generated files only."""
    lines = md.split("\n")
    out = []
    in_p = False
    skip_meta = True
    meta_buf = []

    def close_p():
        nonlocal in_p
        if in_p:
            out.append("</p>")
            in_p = False

    i = 0
    # Skip title (# ...) — rendered in template
    if lines and lines[0].startswith("# "):
        i = 1
        while i < len(lines) and not lines[i].strip():
            i += 1

    # Skip bold masthead line and *Section* meta block into a aside
    while i < len(lines):
        line = lines[i]
        if line.startswith("**") and BRAND in line:
            i += 1
            continue
        if line.startswith("*Section:*") or line.startswith("*Topic:*") or line.startswith("*Wire query:*"):
            meta_buf.append(line.strip("*").strip() if False else line)
            i += 1
            continue
        if skip_meta and not line.strip():
            i += 1
            if meta_buf:
                skip_meta = False
            continue
        break

    def render_inline(s: str) -> str:
        parts = []
        pos = 0
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", s):
            parts.append(html.escape(s[pos : m.start()]))
            parts.append(
                f'<a href="{html.escape(m.group(2), quote=True)}" rel="noopener noreferrer" target="_blank">{html.escape(m.group(1))}</a>'
            )
            pos = m.end()
        parts.append(html.escape(s[pos:]))
        text = "".join(parts)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        return text

    # First non-empty paragraph is dek
    dek_done = False
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            close_p()
            i += 1
            continue
        if line.startswith("## "):
            close_p()
            out.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
            i += 1
            continue
        if line.startswith("### "):
            close_p()
            out.append(f"<h3>{html.escape(line[4:].strip())}</h3>")
            i += 1
            continue
        if line.strip() == "---":
            close_p()
            out.append("<hr />")
            i += 1
            continue
        # GFM tables
        if "|" in line and i + 1 < len(lines) and is_md_table_separator(lines[i + 1]):
            close_p()
            header = line
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip() and not lines[i].startswith("#"):
                rows.append(lines[i])
                i += 1
            out.append(render_md_table(header, rows, render_inline))
            continue
        # unordered lists
        if re.match(r"^[-*]\s+", line):
            close_p()
            out.append("<ul>")
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                item = re.sub(r"^[-*]\s+", "", lines[i])
                out.append(f"<li>{render_inline(item)}</li>")
                i += 1
            out.append("</ul>")
            continue

        if line.startswith("*") and line.endswith("*") and not line.startswith("* "):
            close_p()
            out.append(f"<p class=\"article-footer\">{render_inline(line)}</p>")
            i += 1
            continue

        content = render_inline(line)
        if not dek_done and not line.startswith("#"):
            out.append(f'<p class="dek">{content}</p>')
            dek_done = True
            i += 1
            continue

        if not in_p:
            out.append("<p>")
            in_p = True
            out.append(content)
        else:
            out.append("<br />" + content)
        i += 1

    close_p()
    return "\n".join(out)


ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — {brand}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="author" content="{byline}" />
  <meta name="robots" content="index,follow" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:site_name" content="{brand}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title} — {brand}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:locale" content="en_US" />
  <meta property="article:published_time" content="{published}" />
  <meta property="article:author" content="{byline}" />
  <meta property="article:section" content="{section}" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{title} — {brand}" />
  <meta name="twitter:description" content="{description}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=Syne:wght@700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../css/site.css" />
</head>
<body class="page-article">
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="header-inner">
      <p class="eyebrow">{edition}</p>
      <a class="brand-mark" href="../index.html">{brand}</a>
      <p class="byline-line">Briefings by {byline}</p>
      <nav class="site-nav" aria-label="Primary">
        <a href="../index.html">Home</a>
        <a href="../index.html#headlines">Headlines</a>
        <a href="../index.html#follow-the-money">Follow the Money</a>
        <a href="../index.html#sections">Sections</a>
      </nav>
    </div>
  </header>

  <main id="main" class="article-main">
    <article class="article">
      <header class="article-header">
        <p class="section-kicker">{section}</p>
        <h1>{title}</h1>
        <p class="article-meta"><time datetime="{published}">{edition}</time> · {byline}</p>
      </header>
      <div class="article-body">
{body}
      </div>
    </article>
  </main>

  <nav class="topics-row" aria-label="Topics">
    <p class="topics-label">Topics</p>
    <div class="topics-chips">
{topic_chips}
    </div>
  </nav>

  <aside class="tip-strip tip-strip--article" aria-label="Tip the reporter">
    <div class="tip-inner tip-inner--compact">
      <p class="tip-compact-label">Tip · <span class="tip-preferred">X Money preferred</span></p>
      <div class="tip-actions tip-actions--compact">
        <a class="tip-btn tip-btn--x tip-btn--sm" href="https://x.com/SamCast65215624" rel="noopener noreferrer" target="_blank">X Money</a>
        <a class="tip-btn tip-btn--cash tip-btn--sm" href="https://cash.app/$samiamcastillo" rel="noopener noreferrer" target="_blank">Cash App</a>
        <a class="tip-btn tip-btn--paypal tip-btn--sm" href="mailto:castillo.sam.d@gmail.com" title="PayPal · castillo.sam.d@gmail.com">PayPal</a>
      </div>
      <p class="tip-email-note">PayPal: <a href="mailto:castillo.sam.d@gmail.com">castillo.sam.d@gmail.com</a></p>
    </div>
  </aside>

  <footer class="site-footer">
    <div class="footer-inner">
      <p class="footer-brand">{brand}</p>
      <p>Teleprompt editions for {byline}. Sources linked in each briefing.</p>
      <p><a href="../index.html">← Back to homepage</a></p>
    </div>
  </footer>
  <script src="../js/nav.js" defer></script>
</body>
</html>
"""


INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{brand}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="author" content="{byline}" />
  <meta name="robots" content="index,follow" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:site_name" content="{brand}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{brand}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:locale" content="en_US" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{brand}" />
  <meta name="twitter:description" content="{description}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=Syne:wght@700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/site.css" />
</head>
<body class="page-home">
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="hero">
    <div class="hero-atmosphere" aria-hidden="true">
      <div class="hero-sky"></div>
      <div class="hero-wire"></div>
      <div class="hero-horizon"></div>
    </div>
    <div class="hero-inner">
      <p class="hero-date">{edition}</p>
      <h1 class="hero-brand" aria-label="{brand}">
        <span class="brand-line">Sam News</span>
        <span class="brand-line">Reporter</span>
        <span class="brand-line">Teleprompts</span>
      </h1>
      <p class="hero-tagline">{tagline}</p>
      <div class="hero-cta">
        <a class="btn-primary" href="#headlines">Read today's briefings</a>
        <a class="btn-ghost" href="#follow-the-money">Follow the Money</a>
        <a class="btn-ghost" href="#sections">Browse by section</a>
      </div>
      <p class="hero-credit">Reporting brand · {byline}</p>
    </div>
  </header>

  <nav class="topics-row" aria-label="Topics">
    <p class="topics-label">Topics</p>
    <div class="topics-chips">
{home_topic_chips}
    </div>
  </nav>

  <main id="main">
    <section id="headlines" class="headline-grid-section" aria-labelledby="headlines-title">
      <div class="section-inner">
        <h2 id="headlines-title">Today's teleprompts</h2>
        <p class="section-lede">{count} briefings — research wire plus Follow the Money.</p>
        <ol class="headline-grid">
{headline_items}
        </ol>
      </div>
    </section>

    <section id="follow-the-money" class="money-section" aria-labelledby="money-title">
      <div class="section-inner">
        <h2 id="money-title">Follow the Money</h2>
        <p class="section-lede">Public FEC, OCPF, and VoteView patterns for Massachusetts officials. Correlation is not corruption.</p>
        <ol class="headline-grid money-grid">
{money_items}
        </ol>
      </div>
    </section>

    <section id="sections" class="by-section" aria-labelledby="sections-title">
      <div class="section-inner">
        <h2 id="sections-title">By section</h2>
{section_blocks}
      </div>
    </section>
  </main>

  <section id="support" class="tip-strip tip-strip--home" aria-labelledby="support-title">
    <div class="tip-inner">
      <p class="tip-kicker">Support</p>
      <h2 id="support-title">Tip the reporter</h2>
      <p class="tip-lede">If these briefings help, tip via X Money (preferred), Cash App, or PayPal.</p>
      <div class="tip-actions">
        <a class="tip-btn tip-btn--x" href="https://x.com/SamCast65215624" rel="noopener noreferrer" target="_blank">
          <span class="tip-btn-label">X Money</span>
          <span class="tip-btn-hint">Preferred · tip via X</span>
        </a>
        <a class="tip-btn tip-btn--cash" href="https://cash.app/$samiamcastillo" rel="noopener noreferrer" target="_blank">
          <span class="tip-btn-label">Cash App</span>
          <span class="tip-btn-hint">$samiamcastillo</span>
        </a>
        <a class="tip-btn tip-btn--paypal" href="mailto:castillo.sam.d@gmail.com">
          <span class="tip-btn-label">PayPal</span>
          <span class="tip-btn-hint">castillo.sam.d@gmail.com</span>
        </a>
      </div>
    </div>
  </section>

  <footer class="site-footer">
    <div class="footer-inner">
      <p class="footer-brand">{brand}</p>
      <p>Static teleprompt site · {edition} · {byline}</p>
      <p>{count} articles · open <code>index.html</code> locally</p>
    </div>
  </footer>
  <script src="js/nav.js" defer></script>
</body>
</html>
"""


CSS = """/* Sam News Reporter Teleprompts — site styles */
:root {
  --ink: #152028;
  --ink-soft: #2c3a45;
  --muted: #5c6b76;
  --paper: #e9eef2;
  --paper-2: #f4f7f9;
  --panel: rgba(255, 255, 255, 0.55);
  --line: rgba(21, 32, 40, 0.12);
  --accent: #0b6e6a;
  --accent-deep: #084f4c;
  --signal: #a33b2b;
  --shadow: 0 18px 50px rgba(21, 32, 40, 0.08);
  --font-brand: "Syne", "Fraunces", Georgia, serif;
  --font-display: "Fraunces", "Newsreader", Georgia, serif;
  --font-body: "Newsreader", Georgia, serif;
  --max: 72rem;
  --measure: 40rem;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 1.125rem;
  line-height: 1.65;
  background:
    radial-gradient(1200px 600px at 10% -10%, rgba(11, 110, 106, 0.12), transparent 55%),
    radial-gradient(900px 500px at 100% 0%, rgba(44, 58, 69, 0.1), transparent 50%),
    linear-gradient(180deg, var(--paper) 0%, var(--paper-2) 45%, #e2e8ee 100%);
  min-height: 100vh;
}

body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0.035;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  z-index: 0;
}

body > * {
  position: relative;
  z-index: 1;
}

a {
  color: var(--accent-deep);
  text-underline-offset: 0.15em;
}

a:hover {
  color: var(--accent);
}

.skip-link {
  position: absolute;
  left: 1rem;
  top: -3rem;
  background: var(--ink);
  color: var(--paper-2);
  padding: 0.5rem 0.75rem;
  z-index: 10;
}

.skip-link:focus {
  top: 1rem;
}

/* —— Hero (homepage, one full-viewport composition) —— */
.hero {
  position: relative;
  isolation: isolate;
  min-height: 100vh;
  min-height: 100dvh;
  min-height: max(100dvh, 36rem);
  display: grid;
  align-items: center;
  overflow: hidden;
  color: var(--ink);
  background: #c2d4da;
}

.hero-atmosphere {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.hero-sky {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 85% 65% at 82% 12%, rgba(11, 110, 106, 0.42), transparent 56%),
    radial-gradient(ellipse 60% 40% at 20% 8%, rgba(11, 110, 106, 0.18), transparent 50%),
    radial-gradient(ellipse 50% 45% at 8% 92%, rgba(163, 59, 43, 0.16), transparent 52%),
    linear-gradient(118deg, rgba(236, 243, 246, 0.78) 0%, rgba(236, 243, 246, 0.42) 38%, rgba(236, 243, 246, 0.08) 68%),
    linear-gradient(155deg, #c9dde4 0%, #a8c4ce 42%, #7ea3ae 78%, #5f8894 100%);
  animation: atmosphere-drift 18s ease-in-out infinite alternate;
}

.hero-wire {
  position: absolute;
  inset: 0;
  opacity: 0.85;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 800' preserveAspectRatio='xMidYMid slice'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop stop-color='%230b6e6a' stop-opacity='0.45'/%3E%3Cstop offset='0.55' stop-color='%232c3a45' stop-opacity='0.28'/%3E%3Cstop offset='1' stop-color='%23a33b2b' stop-opacity='0.22'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='1200' height='800' fill='url(%23g)' fill-opacity='0.5'/%3E%3Cpath d='M0 420 Q260 340 540 450 T1200 390' fill='none' stroke='%23152028' stroke-opacity='0.2' stroke-width='2.5'/%3E%3Cpath d='M0 480 Q280 400 560 500 T1200 440' fill='none' stroke='%23084f4c' stroke-opacity='0.28' stroke-width='2'/%3E%3Cpath d='M0 520 Q300 440 600 540 T1200 480 V800 H0Z' fill='%23152028' fill-opacity='0.14'/%3E%3Cpath d='M0 600 Q400 520 700 610 T1200 560 V800 H0Z' fill='%23084f4c' fill-opacity='0.2'/%3E%3Cpath d='M90 90 H1110 M90 130 H860 M90 170 H720' stroke='%23152028' stroke-opacity='0.12' stroke-width='1'/%3E%3Ccircle cx='980' cy='180' r='120' fill='%230b6e6a' fill-opacity='0.12'/%3E%3C/svg%3E");
  background-size: cover;
  background-position: center;
  animation: atmosphere-drift 22s ease-in-out infinite alternate-reverse;
}

.hero-horizon {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: min(38vh, 20rem);
  background:
    linear-gradient(180deg, transparent 0%, rgba(21, 32, 40, 0.08) 50%, rgba(21, 32, 40, 0.2) 100%);
}

@keyframes atmosphere-drift {
  from { transform: scale(1) translate3d(0, 0, 0); }
  to { transform: scale(1.05) translate3d(-1.8%, -1.2%, 0); }
}

.hero-inner {
  position: relative;
  z-index: 1;
  width: min(var(--max), calc(100% - 2.5rem));
  max-width: 100%;
  margin: 0 auto;
  padding: clamp(3rem, 8vh, 5.5rem) 0;
  animation: rise-in 0.9s ease-out both;
}

@keyframes rise-in {
  from { opacity: 0; transform: translateY(1.25rem); }
  to { opacity: 1; transform: translateY(0); }
}

.hero-date {
  margin: 0 0 1rem;
  font-family: var(--font-body);
  font-size: 0.95rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}

.hero-brand {
  margin: 0;
  font-family: var(--font-brand);
  font-weight: 800;
  font-size: clamp(2.75rem, 8.5vw, 5.5rem);
  line-height: 0.96;
  letter-spacing: -0.035em;
  max-width: 12ch;
  color: #101820;
}

.hero-brand .brand-line {
  display: block;
}

.hero-tagline {
  margin: 1.25rem 0 0;
  max-width: 34ch;
  font-size: clamp(1.15rem, 2.4vw, 1.45rem);
  color: var(--ink-soft);
}

.hero-cta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem 1rem;
  margin-top: 2rem;
}

.btn-primary,
.btn-ghost {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.9rem 1.35rem;
  font-family: var(--font-brand);
  font-weight: 700;
  font-size: 0.95rem;
  text-decoration: none;
  border-radius: 0.2rem;
  transition: transform 0.2s ease, background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

.btn-primary {
  background: var(--ink);
  color: var(--paper-2);
}

.btn-primary:hover {
  background: var(--accent-deep);
  color: #fff;
  transform: translateY(-1px);
}

.btn-ghost {
  background: rgba(255, 255, 255, 0.45);
  color: var(--ink);
  border: 1px solid rgba(21, 32, 40, 0.28);
}

.btn-ghost:hover {
  border-color: var(--accent-deep);
  color: var(--accent-deep);
  background: rgba(255, 255, 255, 0.7);
}

.hero-credit {
  margin: 2.25rem 0 0;
  font-size: 0.95rem;
  color: var(--muted);
}

@media (max-width: 560px) {
  .hero {
    min-height: 100svh;
    min-height: max(100svh, 34rem);
    align-items: center;
  }

  .hero-inner {
    width: calc(100% - 1.75rem);
    max-width: none;
    padding: 2.5rem 0 2.75rem;
  }

  .hero-brand {
    /* Syne is very wide — size to keep "Teleprompts" on one line */
    font-size: clamp(1.9rem, 9.2vw, 2.45rem);
    max-width: none;
    width: 100%;
    letter-spacing: -0.045em;
    line-height: 1.02;
  }

  .hero-tagline {
    max-width: 28ch;
  }

  .hero-cta {
    flex-direction: column;
    align-items: stretch;
  }

  .btn-primary,
  .btn-ghost {
    width: 100%;
  }
}

/* —— Sections —— */
.section-inner {
  width: min(var(--max), calc(100% - 2.5rem));
  margin: 0 auto;
  padding: 3.5rem 0 4rem;
}

.headline-grid-section h2,
.by-section h2 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3.5vw, 2.4rem);
  font-weight: 700;
  letter-spacing: -0.02em;
}

.section-lede {
  margin: 0.5rem 0 2rem;
  color: var(--muted);
  max-width: 36ch;
}

.headline-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 0;
  border-top: 1px solid var(--line);
}

@media (min-width: 720px) {
  .headline-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.headline-grid li {
  border-bottom: 1px solid var(--line);
  padding: 1.25rem 0;
}

@media (min-width: 720px) {
  .headline-grid li:nth-child(odd) {
    padding-right: 1.5rem;
  }
  .headline-grid li:nth-child(even) {
    padding-left: 1.5rem;
    border-left: 1px solid var(--line);
  }
}

.headline-grid a {
  text-decoration: none;
  color: inherit;
  display: block;
}

.headline-grid a:hover .hl-title {
  color: var(--accent-deep);
}

.hl-kicker {
  margin: 0 0 0.35rem;
  font-size: 0.8rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--accent);
  font-family: var(--font-brand);
}

.hl-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(1.15rem, 2vw, 1.35rem);
  line-height: 1.25;
  font-weight: 700;
  transition: color 0.2s ease;
}

.hl-dek {
  margin: 0.5rem 0 0;
  color: var(--muted);
  font-size: 0.98rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.section-block {
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--line);
}

.section-block h3 {
  margin: 0 0 0.75rem;
  font-family: var(--font-brand);
  font-size: 1rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--accent-deep);
}

.section-block ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.section-block li {
  margin: 0.4rem 0;
}

.section-block a {
  font-family: var(--font-display);
  font-weight: 600;
  text-decoration: none;
  color: var(--ink);
}

.section-block a:hover {
  color: var(--accent);
  text-decoration: underline;
}

/* —— Article page —— */
.site-header {
  border-bottom: 1px solid var(--line);
  background: rgba(244, 247, 249, 0.85);
  backdrop-filter: blur(8px);
}

.header-inner {
  width: min(var(--max), calc(100% - 2.5rem));
  margin: 0 auto;
  padding: 1.25rem 0 1.1rem;
}

.eyebrow {
  margin: 0;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}

.brand-mark {
  display: inline-block;
  margin-top: 0.35rem;
  font-family: var(--font-brand);
  font-weight: 800;
  font-size: clamp(1.35rem, 3vw, 1.85rem);
  letter-spacing: -0.02em;
  text-decoration: none;
  color: var(--ink);
  line-height: 1.1;
}

.byline-line {
  margin: 0.25rem 0 0;
  color: var(--muted);
  font-size: 0.95rem;
}

.site-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.85rem;
}

.site-nav a {
  font-family: var(--font-brand);
  font-size: 0.85rem;
  font-weight: 700;
  text-decoration: none;
  color: var(--ink-soft);
}

.site-nav a:hover {
  color: var(--accent);
}

.article-main {
  width: min(var(--measure), calc(100% - 2.5rem));
  margin: 0 auto;
  padding: 2.5rem 0 4rem;
}

.section-kicker {
  margin: 0 0 0.5rem;
  font-family: var(--font-brand);
  font-size: 0.8rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent);
}

.article-header h1 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(1.9rem, 4vw, 2.75rem);
  line-height: 1.15;
  letter-spacing: -0.02em;
}

.article-meta {
  margin: 1rem 0 0;
  color: var(--muted);
  font-size: 0.95rem;
}

.article-body {
  margin-top: 1.75rem;
}

.article-body .dek {
  font-size: 1.25rem;
  color: var(--ink-soft);
  border-left: 3px solid var(--accent);
  padding-left: 1rem;
  margin: 0 0 1.75rem;
}

.article-body h2 {
  font-family: var(--font-display);
  font-size: 1.45rem;
  margin: 2.25rem 0 0.75rem;
}

.article-body h3 {
  font-family: var(--font-display);
  font-size: 1.2rem;
  margin: 1.75rem 0 0.5rem;
}

.article-body p {
  margin: 0 0 1rem;
}

.article-body hr {
  border: 0;
  border-top: 1px solid var(--line);
  margin: 2rem 0;
}

.article-footer {
  color: var(--muted);
  font-size: 0.95rem;
}

.site-footer {
  border-top: 1px solid var(--line);
  margin-top: 1rem;
}

.footer-inner {
  width: min(var(--max), calc(100% - 2.5rem));
  margin: 0 auto;
  padding: 2rem 0 2.5rem;
  color: var(--muted);
  font-size: 0.95rem;
}

.footer-brand {
  margin: 0 0 0.35rem;
  font-family: var(--font-brand);
  font-weight: 800;
  color: var(--ink);
}

code {
  font-size: 0.9em;
}


.money-section {
  background: linear-gradient(180deg, rgba(11, 110, 106, 0.06) 0%, transparent 70%);
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}

.money-section h2 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3.5vw, 2.4rem);
  font-weight: 700;
  letter-spacing: -0.02em;
}

.money-grid {
  border-top: 1px solid var(--line);
}

.article-body table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  margin: 0 0 1.25rem;
  display: block;
  overflow-x: auto;
}

.article-body thead {
  display: table;
  width: 100%;
  table-layout: fixed;
}

.article-body tbody {
  display: table;
  width: 100%;
  table-layout: fixed;
}

.article-body th,
.article-body td {
  text-align: left;
  padding: 0.45rem 0.55rem;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}

.article-body th {
  font-family: var(--font-brand);
  font-size: 0.75rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--accent-deep);
}

.article-body ul {
  margin: 0 0 1rem;
  padding-left: 1.2rem;
}

.article-body li {
  margin: 0.35rem 0;
}

@media (max-width: 560px) {
  .article-body table {
    font-size: 0.85rem;
  }
}

/* —— Tip / support strip —— */
.tip-strip {
  border-top: 1px solid var(--line);
  background:
    linear-gradient(180deg, rgba(11, 110, 106, 0.07) 0%, rgba(255, 255, 255, 0.4) 55%, transparent 100%);
}

.tip-strip--home {
  border-bottom: 1px solid var(--line);
}

.tip-inner {
  width: min(var(--max), calc(100% - 2.5rem));
  margin: 0 auto;
  padding: 2.75rem 0 3rem;
}

.tip-inner--compact {
  padding: 1.35rem 0 1.75rem;
}

.tip-kicker {
  margin: 0 0 0.35rem;
  font-size: 0.75rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--accent);
  font-family: var(--font-brand);
}

.tip-strip h2 {
  margin: 0 0 0.45rem;
  font-family: var(--font-display);
  font-size: clamp(1.45rem, 2.6vw, 1.9rem);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--ink);
}

.tip-lede {
  margin: 0 0 1.35rem;
  max-width: 40ch;
  color: var(--muted);
  font-size: 1.05rem;
}

.tip-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem 0.85rem;
  align-items: stretch;
}

.tip-btn {
  display: inline-flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 0.15rem;
  padding: 0.85rem 1.2rem;
  font-family: var(--font-brand);
  text-decoration: none;
  border-radius: 0.2rem;
  border: 1px solid rgba(21, 32, 40, 0.22);
  background: rgba(255, 255, 255, 0.55);
  color: var(--ink);
  transition: transform 0.2s ease, background 0.2s ease, border-color 0.2s ease, color 0.2s ease;
  min-width: 9.5rem;
}

.tip-btn:hover {
  transform: translateY(-1px);
  color: var(--ink);
}

.tip-btn-label {
  font-weight: 800;
  font-size: 0.95rem;
  letter-spacing: 0.01em;
  line-height: 1.15;
}

.tip-btn-hint {
  font-family: var(--font-body);
  font-weight: 400;
  font-size: 0.82rem;
  color: var(--muted);
  line-height: 1.2;
}

.tip-btn--x {
  background: var(--ink);
  color: var(--paper-2);
  border-color: var(--ink);
  box-shadow: 0 10px 28px rgba(21, 32, 40, 0.14);
  order: -1;
  min-width: 11.5rem;
}

.tip-btn--x .tip-btn-hint {
  color: rgba(244, 247, 249, 0.78);
}

.tip-btn--x:hover {
  background: var(--accent-deep);
  border-color: var(--accent-deep);
  color: #fff;
}

.tip-btn--x:hover .tip-btn-hint {
  color: rgba(255, 255, 255, 0.85);
}

.tip-btn--cash:hover,
.tip-btn--paypal:hover {
  border-color: var(--accent-deep);
  background: rgba(255, 255, 255, 0.85);
  color: var(--accent-deep);
}

.tip-btn--sm {
  flex-direction: row;
  align-items: center;
  padding: 0.55rem 0.9rem;
  min-width: 0;
  font-weight: 700;
  font-size: 0.85rem;
}

.tip-btn--x.tip-btn--sm {
  min-width: 0;
}

.tip-compact-label {
  margin: 0 0 0.65rem;
  font-family: var(--font-brand);
  font-size: 0.78rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--muted);
}

.tip-preferred {
  color: var(--accent-deep);
  font-weight: 800;
  letter-spacing: 0.02em;
}

.tip-email-note {
  margin: 0.65rem 0 0;
  font-size: 0.88rem;
  color: var(--muted);
}

.tip-email-note a {
  color: var(--accent-deep);
  text-decoration: none;
  border-bottom: 1px solid rgba(8, 79, 76, 0.28);
}

.tip-email-note a:hover {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

.page-article .tip-strip--article {
  width: min(var(--max), calc(100% - 2.5rem));
  margin: 0 auto;
  background: transparent;
  border-top: 1px dashed var(--line);
}

@media (max-width: 560px) {
  .tip-inner {
    width: calc(100% - 1.75rem);
    padding: 2.25rem 0 2.5rem;
  }

  .tip-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .tip-btn {
    width: 100%;
    min-width: 0;
  }

  .tip-actions--compact {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .tip-actions--compact .tip-btn {
    width: auto;
    flex: 1 1 auto;
  }
}

@media (prefers-reduced-motion: reduce) {
  .tip-btn {
    transition: none;
  }
}

/* —— Topics / hashtag chips —— */
.topics-row {
  width: min(var(--max), calc(100% - 2.5rem));
  margin: 0 auto;
  padding: 1.25rem 0 0.25rem;
}

.page-home .topics-row {
  padding: 1.5rem 0 0.5rem;
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.28);
  width: 100%;
  max-width: none;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.65rem 1rem;
  padding-left: max(1.25rem, calc((100% - var(--max)) / 2));
  padding-right: max(1.25rem, calc((100% - var(--max)) / 2));
}

.page-article .topics-row {
  padding: 0 0 2rem;
}

.topics-label {
  margin: 0;
  font-family: var(--font-brand);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  flex: 0 0 auto;
}

.topics-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem 0.5rem;
  align-items: center;
}

.topic-chip {
  display: inline-block;
  font-family: var(--font-brand);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.01em;
  text-decoration: none;
  color: var(--accent-deep);
  border-bottom: 1px solid rgba(8, 79, 76, 0.28);
  padding: 0.1rem 0;
  transition: color 0.15s ease, border-color 0.15s ease;
}

.topic-chip:hover {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

@media (max-width: 560px) {
  .page-home .topics-row {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .hero-sky,
  .hero-wire,
  .hero-inner {
    animation: none !important;
  }
}
"""

JS = """/* Lightweight active-nav helper */
document.addEventListener("DOMContentLoaded", () => {
  const path = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".site-nav a").forEach((a) => {
    const href = a.getAttribute("href") || "";
    if (href.endsWith(path) || (path === "index.html" && href.includes("index.html") && !href.includes("#"))) {
      a.setAttribute("aria-current", "page");
    }
  });
});
"""


def load_packs() -> list[dict]:
    packs = []
    for path in sorted(TOPIC_PACKS.glob("*.json")):
        with path.open(encoding="utf-8") as f:
            packs.append(json.load(f))
    return packs


def main() -> None:
    packs = load_packs()
    if not packs:
        raise SystemExit(f"No topic packs found in {TOPIC_PACKS}")

    (SITE_ROOT / "css").mkdir(parents=True, exist_ok=True)
    (SITE_ROOT / "js").mkdir(parents=True, exist_ok=True)
    (SITE_ROOT / "md").mkdir(parents=True, exist_ok=True)
    (SITE_ROOT / "articles").mkdir(parents=True, exist_ok=True)

    (SITE_ROOT / "css" / "site.css").write_text(CSS, encoding="utf-8")
    (SITE_ROOT / "js" / "nav.js").write_text(JS, encoding="utf-8")

    articles_meta = []
    for pack in packs:
        slug = pack["slug"]
        section, section_key = SECTION_MAP.get(slug, ("Briefings", "briefings"))
        headline = article_headline(pack)
        dek = article_dek(pack)
        md = build_markdown(pack)
        (SITE_ROOT / "md" / f"{slug}.md").write_text(md, encoding="utf-8")
        body = md_to_article_html_body(md)
        canonical = f"{SITE_URL}/articles/{slug}.html"
        keywords = ", ".join(
            [
                section,
                human_topic_title(slug, pack.get("query", "")),
                "Sam News",
                "teleprompts",
                "2026 midterms",
            ]
        )
        topic_chips = "\n".join(
            [
                f'      <a class="topic-chip" href="../index.html#sections">#{html.escape(section_key.title())}</a>',
                '      <a class="topic-chip" href="../index.html#follow-the-money">#FollowTheMoney</a>',
                '      <a class="topic-chip" href="../index.html">#SamNews</a>',
            ]
        )
        page = ARTICLE_TEMPLATE.format(
            title=html.escape(headline),
            brand=html.escape(BRAND),
            description=html.escape(dek[:220]),
            keywords=html.escape(keywords),
            byline=html.escape(BYLINE),
            edition=html.escape(EDITION_DATE),
            section=html.escape(section),
            body=body,
            canonical=html.escape(canonical),
            published=EDITION_ISO,
            topic_chips=topic_chips,
        )
        (SITE_ROOT / "articles" / f"{slug}.html").write_text(page, encoding="utf-8")
        articles_meta.append(
            {
                "slug": slug,
                "headline": headline,
                "dek": dek,
                "section": section,
                "section_key": section_key,
                "topic": human_topic_title(slug, pack.get("query", "")),
            }
        )

    # Money articles (Follow the Money) — curated from public FEC/OCPF/VoteView outs
    money_meta = []
    for article in MONEY_ARTICLES:
        slug = article["slug"]
        headline = article["headline"]
        dek = article["dek"]
        md = money_markdown(article)
        (SITE_ROOT / "md" / f"{slug}.md").write_text(md, encoding="utf-8")
        body = md_to_article_html_body(md)
        canonical = f"{SITE_URL}/articles/{slug}.html"
        keywords = (
            "Follow the Money, FollowTheMoney, campaign finance, Massachusetts, "
            "FEC, 2026 midterms, Sam News"
        )
        topic_chips = "\n".join(
            [
                '      <a class="topic-chip" href="../index.html#follow-the-money">#FollowTheMoney</a>',
                '      <a class="topic-chip" href="federal-money-patterns-ma.html">#CampaignFinance</a>',
                '      <a class="topic-chip" href="../index.html">#SamNews</a>',
            ]
        )
        page = ARTICLE_TEMPLATE.format(
            title=html.escape(headline),
            brand=html.escape(BRAND),
            description=html.escape(dek[:220]),
            keywords=html.escape(keywords),
            byline=html.escape(BYLINE),
            edition=html.escape(MONEY_EDITION),
            section=html.escape(MONEY_SECTION),
            body=body,
            canonical=html.escape(canonical),
            published="2026-10-24",
            topic_chips=topic_chips,
        )
        (SITE_ROOT / "articles" / f"{slug}.html").write_text(page, encoding="utf-8")
        meta = {
            "slug": slug,
            "headline": headline,
            "dek": dek,
            "section": MONEY_SECTION,
            "section_key": MONEY_SECTION_KEY,
            "topic": "Campaign finance",
        }
        money_meta.append(meta)
        articles_meta.append(meta)

    # Lead with a few stronger wires for homepage ordering: politics, world, sport first then rest
    priority = [
        "election-misinformation-and-media",
        "us-saudi-arabia-and-houthi-conflict",
        "fifa-world-cup-2026",
        "public-safety-and-crime-news",
        "homeowners-and-mortgage-rates",
        "quantum-entanglement",
        "artificial-intelligence-in-fiction",
    ]
    money_slugs = {a["slug"] for a in money_meta}
    rank = {s: i for i, s in enumerate(priority)}
    wire_meta = [a for a in articles_meta if a["slug"] not in money_slugs]
    wire_meta.sort(key=lambda a: (rank.get(a["slug"], 100), a["section"], a["headline"]))

    headline_items = []
    for a in wire_meta:
        headline_items.append(
            "          <li>\n"
            f'            <a href="articles/{html.escape(a["slug"])}.html">\n'
            f'              <p class="hl-kicker">{html.escape(a["section"])}</p>\n'
            f'              <h3 class="hl-title">{html.escape(a["headline"])}</h3>\n'
            f'              <p class="hl-dek">{html.escape(a["dek"])}</p>\n'
            "            </a>\n"
            "          </li>"
        )

    money_items = []
    for a in money_meta:
        money_items.append(
            "          <li>\n"
            f'            <a href="articles/{html.escape(a["slug"])}.html">\n'
            f'              <p class="hl-kicker">{html.escape(a["section"])}</p>\n'
            f'              <h3 class="hl-title">{html.escape(a["headline"])}</h3>\n'
            f'              <p class="hl-dek">{html.escape(a["dek"])}</p>\n'
            "            </a>\n"
            "          </li>"
        )

    by_section: dict[str, list] = {s: [] for s in SECTION_ORDER}
    for a in articles_meta:
        by_section.setdefault(a["section"], []).append(a)

    section_blocks = []
    for section in SECTION_ORDER:
        items = by_section.get(section) or []
        if not items:
            continue
        lis = "\n".join(
            f'            <li><a href="articles/{html.escape(a["slug"])}.html">{html.escape(a["headline"])}</a></li>'
            for a in items
        )
        section_blocks.append(
            f'        <div class="section-block">\n'
            f"          <h3>{html.escape(section)}</h3>\n"
            f"          <ul>\n{lis}\n          </ul>\n"
            f"        </div>"
        )

    total_count = len(articles_meta)
    index_description = (
        "Sam News Reporter Teleprompts — research-wire briefings plus Follow the Money: "
        "2026 midterms, campaign finance, Disney/Fox media consolidation, and more."
    )
    index_keywords = (
        "Sam News, Sam News Reporter Teleprompts, teleprompts, Follow the Money, "
        "FollowTheMoney, 2026 midterms, 2026Midterms, Elections 2026, Elections2026, "
        "campaign finance, Disney Fox, DisneyFox, media consolidation, Massachusetts, "
        "ActBlue, politics, research wire"
    )
    home_topic_chips = "\n".join(
        [
            '      <a class="topic-chip" href="#follow-the-money">#FollowTheMoney</a>',
            '      <a class="topic-chip" href="articles/election-misinformation-and-media.html">#2026Midterms</a>',
            '      <a class="topic-chip" href="articles/election-misinformation-and-media.html">#Elections2026</a>',
            '      <a class="topic-chip" href="articles/disney-fox-media-consolidation.html">#DisneyFox</a>',
            '      <a class="topic-chip" href="articles/disney-fox-media-consolidation.html">#MediaConsolidation</a>',
            '      <a class="topic-chip" href="articles/federal-money-patterns-ma.html">#CampaignFinance</a>',
            '      <a class="topic-chip" href="articles/actblue-winred-vs-direct.html">#ActBlue</a>',
            '      <a class="topic-chip" href="articles/ma-ocpf-sabadosa-comerford-healey.html">#Massachusetts</a>',
            '      <a class="topic-chip" href="#sections">#PoliticsAndMedia</a>',
        ]
    )
    index = INDEX_TEMPLATE.format(
        brand=html.escape(BRAND),
        tagline=html.escape(SITE_TAGLINE),
        description=html.escape(index_description),
        keywords=html.escape(index_keywords),
        canonical=html.escape(f"{SITE_URL}/"),
        byline=html.escape(BYLINE),
        edition=html.escape(EDITION_DATE),
        count=total_count,
        headline_items="\n".join(headline_items),
        money_items="\n".join(money_items),
        section_blocks="\n".join(section_blocks),
        home_topic_chips=home_topic_chips,
    )
    (SITE_ROOT / "index.html").write_text(index, encoding="utf-8")

    readme = f"""# {BRAND}

Static news teleprompt site branded for **{BYLINE}**.

## Edition

{EDITION_DATE}

## How to open

Open the homepage in a browser (no server required):

```bash
open index.html
# or: xdg-open index.html
# or: double-click index.html
```

All article links are relative (`articles/*.html`, `css/site.css`, `js/nav.js`).

## File map

```
sam-news-reporter-teleprompts/
├── index.html          # Homepage
├── README.md           # This file
├── css/site.css        # Shared styles
├── js/nav.js           # Optional nav helper
├── md/                 # Markdown source per article ({len(articles_meta)} files)
├── articles/           # HTML article pages ({len(articles_meta)} files)
└── scripts/build.py    # Regenerate site from topic-pack JSON
```

## Article count

**{len(articles_meta)}** articles.

## Rebuild

Topic packs live at `/cursor/stores/self/internal/topic-packs/`.

```bash
python3 scripts/build.py
```

Rebuild writes `md/`, `articles/`, `index.html`, `css/site.css`, and `js/nav.js` from the JSON seeds. Article copy stays faithful to source hit titles and snippets — no invented news facts.

## Publish gate

**No deploy unless tests pass.** This `build.py` runs midterms functional tests first.

```bash
python3 /home/sandcastle/midterms2026/scripts/functional_build_tests.py
bash /home/sandcastle/midterms2026/scripts/build_and_publish.sh --build
```

See Project store `docs/functional-build-tests.md`.

## Sample headlines

"""
    for a in articles_meta[:8]:
        readme += f"- {a['headline']}\n"
    readme += "\n"
    (SITE_ROOT / "README.md").write_text(readme, encoding="utf-8")

    print(f"Built {len(articles_meta)} articles → {SITE_ROOT}")
    for a in articles_meta[:5]:
        print(f"  • {a['headline']}")


if __name__ == "__main__":
    import os
    import subprocess
    import sys
    from pathlib import Path as _Path

    # Publish gate: no Sam News rebuild unless midterms functional tests pass.
    if os.environ.get("SKIP_FUNCTIONAL_BUILD_TESTS") != "1":
        candidates = [
            _Path("/home/sandcastle/midterms2026/scripts/functional_build_tests.py"),
            _Path("/home/ubuntu/midterms2026/scripts/functional_build_tests.py"),
        ]
        test_script = next((c for c in candidates if c.is_file()), None)
        if test_script is None:
            print(
                "ERROR: functional_build_tests.py not found under midterms2026; "
                "refusing to build (publish gate).",
                file=sys.stderr,
            )
            raise SystemExit(1)
        print(f"==> Publish gate: {test_script}")
        rc = subprocess.call([sys.executable, str(test_script)])
        if rc != 0:
            print("ERROR: functional build tests failed — refusing to build/publish.", file=sys.stderr)
            raise SystemExit(rc)
    main()
