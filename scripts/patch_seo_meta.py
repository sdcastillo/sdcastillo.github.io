#!/usr/bin/env python3
"""Patch Sam News HTML with SEO meta tags + Topics chips (preserves hand-curated pages)."""

from __future__ import annotations

import html
import re
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://sam-news-reporter-teleprompts.vercel.app"
BRAND = "Sam News Reporter Teleprompts"
BYLINE = "Sam Castillo"
EDITION_DATE = "Thursday, October 29, 2026"
EDITION_ISO = "2026-10-29"

# Homepage topic chips (label, href) — light, accurate, not spam
HOME_TOPICS = [
    ("#FollowTheMoney", "#follow-the-money"),
    ("#2026Midterms", "articles/election-misinformation-and-media.html"),
    ("#Elections2026", "articles/israel-election-deadlock-2026.html"),
    ("#DisneyFox", "articles/disney-fox-media-consolidation.html"),
    ("#MediaConsolidation", "articles/disney-fox-media-consolidation.html"),
    ("#CampaignFinance", "articles/federal-money-patterns-ma.html"),
    ("#ActBlue", "articles/actblue-winred-vs-direct.html"),
    ("#Massachusetts", "articles/ma-ocpf-sabadosa-comerford-healey.html"),
    ("#PoliticsAndMedia", "#sections"),
]

# Per-article keywords (hashtag-style + plain) and topic chips
ARTICLE_SEO: dict[str, dict] = {
    "disney-fox-media-consolidation": {
        "keywords": [
            "Disney Fox",
            "media consolidation",
            "Disney",
            "Fox Corporation",
            "21st Century Fox",
            "Comcast Sky",
            "News Corp",
            "Politics and Media",
            "DisneyFox",
            "MediaConsolidation",
            "Sam News",
        ],
        "topics": [
            ("#DisneyFox", "disney-fox-media-consolidation.html"),
            ("#MediaConsolidation", "disney-fox-media-consolidation.html"),
            ("#PoliticsAndMedia", "../index.html#sections"),
            ("#FollowTheMoney", "../index.html#follow-the-money"),
        ],
        "og_type": "article",
        "section": "Politics & Media",
        "published": "2026-10-27",
    },
    "election-misinformation-and-media": {
        "keywords": [
            "election misinformation",
            "2026 midterms",
            "Elections 2026",
            "ballot processing",
            "media amplification",
            "2026Midterms",
            "Elections2026",
            "Politics and Media",
            "Sam News",
        ],
        "topics": [
            ("#2026Midterms", "election-misinformation-and-media.html"),
            ("#Elections2026", "election-misinformation-and-media.html"),
            ("#PoliticsAndMedia", "../index.html#sections"),
        ],
        "og_type": "article",
        "section": "Politics & Media",
        "published": "2026-10-21",
    },
    "base-rate-fallacy-in-politics": {
        "keywords": [
            "base rate fallacy",
            "political polarization",
            "class perception",
            "Politics and Media",
            "opinion groups",
            "Sam News",
        ],
        "topics": [
            ("#PoliticsAndMedia", "../index.html#sections"),
            ("#2026Midterms", "election-misinformation-and-media.html"),
        ],
        "og_type": "article",
        "section": "Politics & Media",
        "published": "2026-10-21",
    },
    "federal-money-patterns-ma": {
        "keywords": [
            "Follow the Money",
            "FollowTheMoney",
            "campaign finance",
            "FEC",
            "Massachusetts",
            "Markey",
            "Warren",
            "Neal",
            "McGovern",
            "2026 midterms",
            "CampaignFinance",
            "Sam News",
        ],
        "topics": [
            ("#FollowTheMoney", "../index.html#follow-the-money"),
            ("#CampaignFinance", "federal-money-patterns-ma.html"),
            ("#Massachusetts", "ma-ocpf-sabadosa-comerford-healey.html"),
            ("#2026Midterms", "election-misinformation-and-media.html"),
        ],
        "og_type": "article",
        "section": "Follow the Money",
        "published": "2026-10-24",
    },
    "party-line-voting-99-percent": {
        "keywords": [
            "Follow the Money",
            "FollowTheMoney",
            "party line voting",
            "VoteView",
            "Congress roll calls",
            "Massachusetts",
            "Sam News",
        ],
        "topics": [
            ("#FollowTheMoney", "../index.html#follow-the-money"),
            ("#Massachusetts", "ma-ocpf-sabadosa-comerford-healey.html"),
        ],
        "og_type": "article",
        "section": "Follow the Money",
        "published": "2026-10-24",
    },
    "ma-ocpf-sabadosa-comerford-healey": {
        "keywords": [
            "Follow the Money",
            "FollowTheMoney",
            "OCPF",
            "Massachusetts",
            "Sabadosa",
            "Comerford",
            "Healey",
            "state campaign finance",
            "Sam News",
        ],
        "topics": [
            ("#FollowTheMoney", "../index.html#follow-the-money"),
            ("#Massachusetts", "ma-ocpf-sabadosa-comerford-healey.html"),
            ("#CampaignFinance", "federal-money-patterns-ma.html"),
        ],
        "og_type": "article",
        "section": "Follow the Money",
        "published": "2026-10-24",
    },
    "congress-rollcalls-markey-warren-pac": {
        "keywords": [
            "Follow the Money",
            "FollowTheMoney",
            "Markey",
            "Warren",
            "PAC",
            "VoteView",
            "party unity",
            "2026",
            "Sam News",
        ],
        "topics": [
            ("#FollowTheMoney", "../index.html#follow-the-money"),
            ("#CampaignFinance", "federal-money-patterns-ma.html"),
            ("#2026Midterms", "election-misinformation-and-media.html"),
        ],
        "og_type": "article",
        "section": "Follow the Money",
        "published": "2026-10-24",
    },
    "how-to-read-campaign-finance-db": {
        "keywords": [
            "Follow the Money",
            "FollowTheMoney",
            "campaign finance database",
            "FEC",
            "ActBlue",
            "WinRed",
            "reporter guide",
            "Sam News",
        ],
        "topics": [
            ("#FollowTheMoney", "../index.html#follow-the-money"),
            ("#CampaignFinance", "how-to-read-campaign-finance-db.html"),
            ("#ActBlue", "actblue-winred-vs-direct.html"),
        ],
        "og_type": "article",
        "section": "Follow the Money",
        "published": "2026-10-24",
    },
    "actblue-winred-vs-direct": {
        "keywords": [
            "ActBlue",
            "WinRed",
            "Follow the Money",
            "FollowTheMoney",
            "campaign finance",
            "FEC itcont",
            "Massachusetts Democrats",
            "Sam News",
        ],
        "topics": [
            ("#ActBlue", "actblue-winred-vs-direct.html"),
            ("#FollowTheMoney", "../index.html#follow-the-money"),
            ("#CampaignFinance", "federal-money-patterns-ma.html"),
        ],
        "og_type": "article",
        "section": "Follow the Money",
        "published": "2026-10-24",
    },
    "us-saudi-arabia-and-houthi-conflict": {
        "keywords": [
            "Saudi Arabia",
            "Houthi",
            "Yemen",
            "US foreign policy",
            "World news",
            "Sam News",
        ],
        "topics": [("#World", "../index.html#sections")],
        "og_type": "article",
        "section": "World",
        "published": "2026-10-21",
    },
    "public-safety-and-crime-news": {
        "keywords": [
            "public safety",
            "crime prevention",
            "California",
            "violence intervention",
            "World news",
            "Sam News",
        ],
        "topics": [("#World", "../index.html#sections")],
        "og_type": "article",
        "section": "World",
        "published": "2026-10-21",
    },
    "fifa-world-cup-2026": {
        "keywords": [
            "FIFA World Cup 2026",
            "sport marketing",
            "junk food advertising",
            "World Cup",
            "Sam News",
        ],
        "topics": [("#WorldCup2026", "fifa-world-cup-2026.html"), ("#Sport", "../index.html#sections")],
        "og_type": "article",
        "section": "Sport",
        "published": "2026-10-21",
    },
    "running-and-fitness": {
        "keywords": ["slow jogging", "fitness", "running", "aerobic fitness", "Sport", "Sam News"],
        "topics": [("#Sport", "../index.html#sections")],
        "og_type": "article",
        "section": "Sport",
        "published": "2026-10-21",
    },
    "quantum-entanglement": {
        "keywords": [
            "quantum entanglement",
            "ATLAS",
            "CMS",
            "Higgs boson",
            "Science",
            "Sam News",
        ],
        "topics": [("#Science", "../index.html#sections")],
        "og_type": "article",
        "section": "Science & Ideas",
        "published": "2026-10-21",
    },
    "artificial-intelligence-in-fiction": {
        "keywords": [
            "artificial intelligence",
            "AI fiction",
            "creative writing",
            "Science and Ideas",
            "Sam News",
        ],
        "topics": [("#AI", "artificial-intelligence-in-fiction.html"), ("#Science", "../index.html#sections")],
        "og_type": "article",
        "section": "Science & Ideas",
        "published": "2026-10-21",
    },
    "molecular-biology-central-dogma": {
        "keywords": [
            "central dogma",
            "molecular biology",
            "nucleic acids",
            "Science",
            "Sam News",
        ],
        "topics": [("#Science", "../index.html#sections")],
        "og_type": "article",
        "section": "Science & Ideas",
        "published": "2026-10-21",
    },
    "homeowners-and-mortgage-rates": {
        "keywords": [
            "mortgage rates",
            "homebuyers",
            "overpaying mortgage",
            "Economy",
            "housing",
            "Sam News",
        ],
        "topics": [("#Economy", "../index.html#sections")],
        "og_type": "article",
        "section": "Economy",
        "published": "2026-10-21",
    },
    "guitar-songwriting-and-rock-music": {
        "keywords": [
            "rock music",
            "music theory",
            "songwriting",
            "guitar",
            "Arts and Culture",
            "Sam News",
        ],
        "topics": [("#Arts", "../index.html#sections")],
        "og_type": "article",
        "section": "Arts & Culture",
        "published": "2026-10-21",
    },
    "iconic-artists-and-folk-heroes": {
        "keywords": ["Woody Guthrie", "folk music", "Arts and Culture", "Sam News"],
        "topics": [("#Arts", "../index.html#sections")],
        "og_type": "article",
        "section": "Arts & Culture",
        "published": "2026-10-21",
    },
    "hawaii-travel": {
        "keywords": [
            "Hawaii travel",
            "sustainable tourism",
            "Travel and Life",
            "Sam News",
        ],
        "topics": [("#Travel", "../index.html#sections")],
        "og_type": "article",
        "section": "Travel & Life",
        "published": "2026-10-21",
    },
    "creative-donut-flavors": {
        "keywords": ["donut flavors", "Travel and Life", "food", "Sam News"],
        "topics": [("#Travel", "../index.html#sections")],
        "og_type": "article",
        "section": "Travel & Life",
        "published": "2026-10-21",
    },
    "christian-faith-and-family": {
        "keywords": [
            "faith and family",
            "parenting",
            "religious retention",
            "Travel and Life",
            "Sam News",
        ],
        "topics": [("#Travel", "../index.html#sections")],
        "og_type": "article",
        "section": "Travel & Life",
        "published": "2026-10-21",
    },
    "dolphins-and-ocean-life": {
        "keywords": ["dolphins", "ocean life", "echolocation", "Environment", "Sam News"],
        "topics": [("#Environment", "../index.html#sections")],
        "og_type": "article",
        "section": "Environment",
        "published": "2026-10-21",
    },
    "titanic-and-famous-maritime-disasters": {
        "keywords": [
            "Titanic",
            "maritime disasters",
            "northern lights",
            "Environment",
            "Sam News",
        ],
        "topics": [("#Environment", "../index.html#sections")],
        "og_type": "article",
        "section": "Environment",
        "published": "2026-10-21",
    },
    # News-trends wire (sibling ingest) — topical, accurate tags only
    "alaska-senate-doj-lawsuit-blanche": {
        "keywords": [
            "Alaska Senate",
            "DOJ",
            "Todd Blanche",
            "2026 elections",
            "Elections2026",
            "Politics and Media",
            "Sam News",
        ],
        "topics": [
            ("#Elections2026", "alaska-senate-doj-lawsuit-blanche.html"),
            ("#PoliticsAndMedia", "../index.html#sections"),
        ],
        "og_type": "article",
        "section": "Politics & Media",
        "published": "2026-10-29",
    },
    "brazil-election-lula-2026": {
        "keywords": [
            "Brazil election",
            "Lula",
            "2026 elections",
            "Elections2026",
            "World",
            "Sam News",
        ],
        "topics": [
            ("#Elections2026", "brazil-election-lula-2026.html"),
            ("#World", "../index.html#sections"),
        ],
        "og_type": "article",
        "section": "World",
        "published": "2026-10-29",
    },
    "israel-election-deadlock-2026": {
        "keywords": [
            "Israel election",
            "2026 elections",
            "Elections2026",
            "deadlock",
            "World",
            "Sam News",
        ],
        "topics": [
            ("#Elections2026", "israel-election-deadlock-2026.html"),
            ("#World", "../index.html#sections"),
        ],
        "og_type": "article",
        "section": "World",
        "published": "2026-10-29",
    },
    "serbia-vucic-concedes-election": {
        "keywords": [
            "Serbia election",
            "Vučić",
            "2026 elections",
            "Elections2026",
            "World",
            "Sam News",
        ],
        "topics": [
            ("#Elections2026", "serbia-vucic-concedes-election.html"),
            ("#World", "../index.html#sections"),
        ],
        "og_type": "article",
        "section": "World",
        "published": "2026-10-29",
    },
    "venezuela-machado-returns-exile": {
        "keywords": [
            "Venezuela",
            "María Corina Machado",
            "exile",
            "World",
            "Sam News",
        ],
        "topics": [("#World", "../index.html#sections")],
        "og_type": "article",
        "section": "World",
        "published": "2026-10-29",
    },
    "nvidia-hugging-face-doj-inquiry": {
        "keywords": [
            "Nvidia",
            "Hugging Face",
            "DOJ inquiry",
            "AI acquisition",
            "Science and Ideas",
            "Sam News",
        ],
        "topics": [
            ("#AI", "nvidia-hugging-face-doj-inquiry.html"),
            ("#Science", "../index.html#sections"),
        ],
        "og_type": "article",
        "section": "Science & Ideas",
        "published": "2026-10-29",
    },
    "hhs-unapproved-peptides-enforcement-discretion": {
        "keywords": [
            "HHS",
            "peptides",
            "enforcement discretion",
            "public health",
            "Sam News",
        ],
        "topics": [("#Science", "../index.html#sections")],
        "og_type": "article",
        "section": "Science & Ideas",
        "published": "2026-10-29",
    },
    "us-measles-outbreak-pennsylvania-2026": {
        "keywords": [
            "measles outbreak",
            "Pennsylvania",
            "public health",
            "2026",
            "Sam News",
        ],
        "topics": [("#World", "../index.html#sections")],
        "og_type": "article",
        "section": "World",
        "published": "2026-10-29",
    },
}

HOME_KEYWORDS = [
    "Sam News",
    "Sam News Reporter Teleprompts",
    "teleprompts",
    "Follow the Money",
    "FollowTheMoney",
    "2026 midterms",
    "2026Midterms",
    "Elections 2026",
    "Elections2026",
    "campaign finance",
    "Disney Fox",
    "DisneyFox",
    "media consolidation",
    "Massachusetts",
    "ActBlue",
    "politics",
    "research wire",
]


def meta_block(
    *,
    title: str,
    description: str,
    keywords: list[str],
    canonical: str,
    og_type: str,
    og_url: str,
    published: str | None = None,
    section: str | None = None,
) -> str:
    kw = ", ".join(keywords)
    lines = [
        f'  <meta name="description" content="{html.escape(description, quote=True)}" />',
        f'  <meta name="keywords" content="{html.escape(kw, quote=True)}" />',
        f'  <meta name="author" content="{html.escape(BYLINE, quote=True)}" />',
        f'  <meta name="robots" content="index,follow" />',
        f'  <link rel="canonical" href="{html.escape(canonical, quote=True)}" />',
        f'  <meta property="og:site_name" content="{html.escape(BRAND, quote=True)}" />',
        f'  <meta property="og:type" content="{html.escape(og_type, quote=True)}" />',
        f'  <meta property="og:title" content="{html.escape(title, quote=True)}" />',
        f'  <meta property="og:description" content="{html.escape(description, quote=True)}" />',
        f'  <meta property="og:url" content="{html.escape(og_url, quote=True)}" />',
        f'  <meta property="og:locale" content="en_US" />',
        f'  <meta name="twitter:card" content="summary" />',
        f'  <meta name="twitter:title" content="{html.escape(title, quote=True)}" />',
        f'  <meta name="twitter:description" content="{html.escape(description, quote=True)}" />',
    ]
    if published and og_type == "article":
        lines.append(
            f'  <meta property="article:published_time" content="{html.escape(published, quote=True)}" />'
        )
        lines.append(
            f'  <meta property="article:author" content="{html.escape(BYLINE, quote=True)}" />'
        )
        if section:
            lines.append(
                f'  <meta property="article:section" content="{html.escape(section, quote=True)}" />'
            )
        # article:tag for topical discoverability (not spam)
        for tag in keywords[:8]:
            if tag.lower() in {"sam news"}:
                continue
            lines.append(
                f'  <meta property="article:tag" content="{html.escape(tag, quote=True)}" />'
            )
    return "\n".join(lines)


def topics_nav(topics: list[tuple[str, str]], heading: str = "Topics") -> str:
    chips = "\n".join(
        f'      <a class="topic-chip" href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'
        for label, href in topics
    )
    return (
        f'  <nav class="topics-row" aria-label="{html.escape(heading)}">\n'
        f'    <p class="topics-label">{html.escape(heading)}</p>\n'
        f'    <div class="topics-chips">\n{chips}\n    </div>\n'
        f"  </nav>"
    )


def extract_title(doc: str) -> str:
    m = re.search(r"<title>(.*?)</title>", doc, re.I | re.S)
    if not m:
        return BRAND
    return re.sub(r"\s+", " ", m.group(1)).strip()


def extract_description(doc: str) -> str:
    m = re.search(
        r'<meta\s+name="description"\s+content="([^"]*)"',
        doc,
        re.I,
    )
    if m:
        return html.unescape(m.group(1)).strip()
    m = re.search(r'<p class="dek">(.*?)</p>', doc, re.I | re.S)
    if m:
        text = re.sub(r"<[^>]+>", "", m.group(1))
        return re.sub(r"\s+", " ", html.unescape(text)).strip()[:200]
    return "Teleprompt briefings from Sam News Reporter Teleprompts."


def replace_head_meta(doc: str, new_meta: str) -> str:
    # Remove existing description/author/keywords/robots/canonical/og/twitter/article meta
    # Keep charset, viewport, title, fonts, stylesheet
    head_m = re.search(r"<head>(.*?)</head>", doc, re.I | re.S)
    if not head_m:
        return doc
    head = head_m.group(1)
    # Drop SEO-ish tags we will replace
    drop_patterns = [
        r'\s*<meta\s+name="description"[^>]*/?>',
        r'\s*<meta\s+name="keywords"[^>]*/?>',
        r'\s*<meta\s+name="author"[^>]*/?>',
        r'\s*<meta\s+name="robots"[^>]*/?>',
        r'\s*<meta\s+name="twitter:[^"]+"[^>]*/?>',
        r'\s*<meta\s+property="og:[^"]+"[^>]*/?>',
        r'\s*<meta\s+property="article:[^"]+"[^>]*/?>',
        r'\s*<link\s+rel="canonical"[^>]*/?>',
    ]
    for pat in drop_patterns:
        head = re.sub(pat, "", head, flags=re.I)
    # Insert new meta after <title>...</title> if present, else after viewport
    # Use a callable replacer so description text like "2. …" cannot be read as \12
    if re.search(r"</title>", head, re.I):

        def _after_title(m: re.Match[str]) -> str:
            return m.group(1) + "\n" + new_meta

        head = re.sub(r"(</title>)", _after_title, head, count=1, flags=re.I)
    else:
        head = new_meta + head
    # Collapse excess blank lines
    head = re.sub(r"\n{3,}", "\n\n", head)
    return doc[: head_m.start(1)] + head + doc[head_m.end(1) :]


def ensure_topics(doc: str, topics_html: str, *, home: bool) -> str:
    # Remove prior topics rows to keep idempotent
    doc = re.sub(
        r'\s*<nav class="topics-row"[^>]*>.*?</nav>\s*',
        "\n",
        doc,
        flags=re.I | re.S,
    )
    if home:
        # Place after hero, before main (first header is the hero)
        m = re.search(r"</header>\s*<main\b", doc, re.I)
        if m:
            insert = "</header>\n\n" + topics_html + "\n\n  <main"
            # Preserve exact <main ... attributes by splicing
            main_m = re.search(r"<main\b[^>]*>", doc[m.start() :], re.I)
            assert main_m
            main_tag = main_m.group(0)
            doc = doc[: m.start()] + "</header>\n\n" + topics_html + "\n\n  " + main_tag + doc[m.start() + main_m.end() :]
        else:
            doc = doc.replace("<main", topics_html + "\n  <main", 1)
    else:
        # Place before site-footer (article footer topics)
        m = re.search(r'<footer class="site-footer"', doc, re.I)
        if m:
            doc = doc[: m.start()] + topics_html + "\n\n  " + doc[m.start() :]
        else:
            doc = doc.replace("</body>", topics_html + "\n</body>")
    return doc


def patch_index(path: Path) -> None:
    doc = path.read_text(encoding="utf-8")
    title = BRAND
    description = (
        "Sam News Reporter Teleprompts — research-wire briefings plus Follow the Money: "
        "2026 midterms, campaign finance, Disney/Fox media consolidation, and more."
    )
    canonical = f"{SITE_URL}/"
    meta = meta_block(
        title=title,
        description=description,
        keywords=HOME_KEYWORDS,
        canonical=canonical,
        og_type="website",
        og_url=canonical,
    )
    doc = replace_head_meta(doc, meta)
    # Stale edition date
    doc = doc.replace("Wednesday, October 21, 2026", EDITION_DATE)
    # Topics chips after hero
    doc = ensure_topics(doc, topics_nav(HOME_TOPICS), home=True)
    # Ensure title tag is present and sensible
    if not re.search(r"<title>.+?</title>", doc, re.I | re.S):
        doc = doc.replace("<head>", f"<head>\n  <title>{html.escape(title)}</title>", 1)
    path.write_text(doc, encoding="utf-8")
    print(f"patched {path.name}")


def patch_article(path: Path) -> None:
    slug = path.stem
    doc = path.read_text(encoding="utf-8")
    seo = ARTICLE_SEO.get(slug)
    if not seo:
        # Fallback: derive light keywords from section kicker + slug
        kicker_m = re.search(r'class="section-kicker">(.*?)</p>', doc, re.I | re.S)
        section = re.sub(r"<[^>]+>", "", kicker_m.group(1)).strip() if kicker_m else "Briefings"
        section = html.unescape(section)
        seo = {
            "keywords": [section, slug.replace("-", " "), "Sam News", "teleprompts"],
            "topics": [("#SamNews", "../index.html")],
            "og_type": "article",
            "section": section,
            "published": "2026-10-21",
        }

    title = extract_title(doc)
    # Prefer full page title without brand suffix for og:title clarity, keep brand in <title>
    short_title = re.sub(r"\s*—\s*Sam News Reporter Teleprompts\s*$", "", title).strip() or title
    description = extract_description(doc)
    # Prefer fuller dek if description was truncated mid-word (~160)
    if description.endswith((" Wal", " a 60/40 ", " Misinformatio", " a Ma")):
        dek = extract_description(
            re.sub(
                r'<meta\s+name="description"[^>]*>',
                "",
                doc,
                count=1,
                flags=re.I,
            )
        )
        if len(dek) > len(description):
            description = dek[:220].rstrip()

    canonical = f"{SITE_URL}/articles/{slug}.html"
    meta = meta_block(
        title=f"{short_title} — {BRAND}",
        description=description,
        keywords=seo["keywords"],
        canonical=canonical,
        og_type=seo["og_type"],
        og_url=canonical,
        published=seo.get("published"),
        section=seo.get("section"),
    )
    doc = replace_head_meta(doc, meta)

    # Fix truncated descriptions already written into meta via extract — re-pull dek for body accuracy
    dek_m = re.search(r'<p class="dek">(.*?)</p>', doc, re.I | re.S)
    if dek_m:
        dek_text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", dek_m.group(1)))
        dek_text = html.unescape(dek_text).strip()
        if dek_text and len(dek_text) > 40:
            description = dek_text[:220].rstrip()
            # Refresh description attributes in meta we just inserted
            esc = html.escape(description, quote=True)

            def _set_desc(pattern: str) -> None:
                nonlocal doc

                def repl(m: re.Match[str]) -> str:
                    return m.group(1) + esc + m.group(2)

                doc = re.sub(pattern, repl, doc, count=1)

            _set_desc(r'(<meta name="description" content=")[^"]*(")')
            _set_desc(r'(<meta property="og:description" content=")[^"]*(")')
            _set_desc(r'(<meta name="twitter:description" content=")[^"]*(")')

    # Ensure <title> exists and is non-empty
    if not re.search(r"<title>\s*\S.*?</title>", doc, re.I | re.S):
        title_html = f"<head>\n  <title>{html.escape(short_title)} — {html.escape(BRAND)}</title>"

        def _title_into_head(m: re.Match[str]) -> str:
            return title_html

        doc = re.sub(r"<head>", _title_into_head, doc, count=1, flags=re.I)

    doc = ensure_topics(doc, topics_nav(seo["topics"]), home=False)
    path.write_text(doc, encoding="utf-8")
    print(f"patched articles/{slug}.html")


TOPICS_CSS = """
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
"""


def patch_css(path: Path) -> None:
    css = path.read_text(encoding="utf-8")
    if "/* —— Topics / hashtag chips —— */" in css:
        css = re.sub(
            r"/\* —— Topics / hashtag chips —— \*/.*?(?=@media \(prefers-reduced-motion|\Z)",
            TOPICS_CSS.strip() + "\n\n",
            css,
            count=1,
            flags=re.S,
        )
    elif "@media (prefers-reduced-motion" in css:
        css = css.replace(
            "@media (prefers-reduced-motion",
            TOPICS_CSS + "\n@media (prefers-reduced-motion",
            1,
        )
    else:
        css = css.rstrip() + "\n" + TOPICS_CSS
    path.write_text(css, encoding="utf-8")
    print(f"patched {path.relative_to(SITE_ROOT)}")


def main() -> None:
    patch_css(SITE_ROOT / "css" / "site.css")
    patch_index(SITE_ROOT / "index.html")
    for art in sorted((SITE_ROOT / "articles").glob("*.html")):
        patch_article(art)
    print("done")


if __name__ == "__main__":
    main()
