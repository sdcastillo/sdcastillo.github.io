# Sam News Reporter Teleprompts

Static news teleprompt site branded for **Sam Castillo**.

## Edition

Wednesday, October 21, 2026

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
├── md/                 # Markdown source per article (22 files)
├── articles/           # HTML article pages (22 files)
└── scripts/build.py    # Regenerate site from topic-pack JSON
```

## Article count

**22** articles.

## Rebuild

Topic packs live at `/cursor/stores/self/internal/topic-packs/`.

```bash
python3 scripts/build.py
```

Rebuild writes `md/`, `articles/`, `index.html`, `css/site.css`, and `js/nav.js` from the JSON seeds. Article copy stays faithful to source hit titles and snippets — no invented news facts.

## Sample headlines

- The mystery is missing
- Perceived class positions and opinion-based polarisation: experimental evidence from the UK
- How Parents Can Help Their Kids Build a Faith That Lasts
- The 30 Best Donut Flavors, Ranked by a Nation of Donut Lovers
- ‘Snooping’ on Dolphins: Hotspots for Food and Friends
- Legislating Uncertainty: Election Policies and the Amplification of Misinformation
- World Cup viewers exposed to junk food, alcohol and gambling branding every seven seconds, study finds
- “They’re Scared of Becoming Creatively Impotent”: Rock Musicians’ Perspectives on Music Theory in Creative and Other Work Processes

