"""Follow the Money teleprompt articles — figures from public FEC / OCPF / VoteView outs only."""

from __future__ import annotations

MONEY_EDITION = "Saturday, October 24, 2026"
MONEY_EDITION_SHORT = "Oct 24, 2026"
MONEY_SECTION = "Follow the Money"
MONEY_SECTION_KEY = "money"

# Civic framing: patterns from public records; correlation is not wrongdoing.
MONEY_ARTICLES: list[dict] = [
    {
        "slug": "federal-money-patterns-ma",
        "headline": "Federal Money Patterns: Neal, Warren, Markey, and McGovern",
        "dek": (
            "Public FEC weball and OpenFEC aggregates show four Massachusetts Democrats "
            "raising in very different shapes—PAC-heavy on MA-01, small-dollar on Warren, "
            "and a Markey 2026 surge—without implying motive or misconduct."
        ),
        "body": """
Public federal filings (FEC candidate summaries and OpenFEC aggregates) let readers compare how money arrives—not who “bought” a vote. The figures below come from the Follow the Money kit outs (`book_queries.out`, OpenFEC size/state packs). **Patterns are not proof of wrongdoing.**

## District note

- **Jim McGovern** represents **U.S. House MA-02**, which includes **Northampton**.
- **Richard Neal** represents **U.S. House MA-01**. He is included here as a comparison baseline; that district does **not** cover Northampton.

## Receipts by cycle (FEC weball)

| Cycle | Candidate | Total receipts | Individual | PAC (other pol. cmte) |
|-------|-----------|----------------|------------|------------------------|
| 2024 | Markey | $1,549,923 | $867,630 | $97,500 |
| 2026 | Markey | $5,985,385 | $2,679,817 | $681,440 |
| 2024 | McGovern (MA-02) | $1,097,317 | $741,404 | $349,400 |
| 2026 | McGovern (MA-02) | $1,013,810 | $702,872 | $306,126 |
| 2024 | Neal (MA-01) | $3,285,602 | $752,821 | $2,417,922 |
| 2026 | Neal (MA-01) | $3,112,617 | $709,307 | $2,091,536 |
| 2024 | Warren | $9,039,538 | $8,695,847 | $59,800 |
| 2026 | Warren | $4,965,731 | $4,770,773 | $25,000 |

## What the shapes show

- **Neal (MA-01):** PAC money was about **$2.42M of $3.29M** total receipts in 2024 and **$2.09M of $3.11M** in 2026. Direct committee→candidate 24K (non-memo) ran about **$2.53M** (2024) / **$1.77M** (2026). Itemized individual share from Massachusetts: **22.7%** (2024) / **26.9%** (2026).
- **Warren:** In 2024, **$8.70M of $9.04M** came from individuals; under-$200 (size 0) was **$7,356,111**. PAC money stayed tiny (**$59,800** weball). In-state itemized share ~**27%**.
- **Markey (up in 2026):** Cycle-to-date weball receipts ~**$6.0M**, with PAC 24K up sharply vs 2024 (**$112k → $693k** direct 24K). OpenFEC by-size individual totals jumped **$1.27M → $4.79M**; Massachusetts still leads itemized geography but the MA share slipped **52.3% → 44.6%**.
- **McGovern (MA-02 / Northampton):** Balanced mix—2026 weball ~**$1.01M** total, ~**$306k** PAC. Itemized individual share from MA stays about **55–56%**. OpenFEC by-size ≤$200 share rose **32.6% → 39.9%**.

## How to use this in a teleprompt

Lead with the contrast (PAC-heavy vs small-dollar vs 2026 surge), name the district correctly for Northampton (**McGovern / MA-02**), and close with the civic caveat: these are **public contribution patterns**, not findings of corruption.
""".strip(),
    },
    {
        "slug": "party-line-voting-99-percent",
        "headline": "Party-Line Voting Near 99%: What the Roll Calls Show",
        "dek": (
            "On party-split roll calls in the 118th and 119th Congresses, Markey, McGovern, "
            "Neal, and Warren voted with the Democratic majority 99.0–99.8% of the time—"
            "a cohesion statistic, not an accusation."
        ),
        "body": """
VoteView-derived party-unity scores for the four federal members in the Follow the Money kit measure how often each member voted with the **Democratic majority when Democratic and Republican majorities opposed each other**. High unity is common in a polarized Congress; it is a **descriptive pattern**, not evidence of wrongdoing.

## Party unity on party-split roll calls

| Official | Congress | Party-split votes | % with Dem majority |
|----------|----------|-------------------:|--------------------:|
| Markey | 118 | 521 | 99.0% |
| Markey | 119 | 836 | 99.8% |
| McGovern (MA-02) | 118 | 866 | 99.5% |
| McGovern (MA-02) | 119 | 464 | 99.8% |
| Neal (MA-01) | 118 | 858 | 99.3% |
| Neal (MA-01) | 119 | 448 | 99.1% |
| Warren | 118 | 535 | 99.3% |
| Warren | 119 | 828 | 99.8% |

Source: kit `out/votes.out` and `book_queries.out` §I (member_votes built by `votes.py`).

## Reading the number

- The **99%** figure is limited to **party-split** roll calls (D vs R majorities opposed). Unanimous or near-unanimous votes are outside this slice.
- The 119th Congress extract in related VoteView dumps is **partial** (into autumn 2026), so treat 119th rates as cycle-to-date, not a finished Congress.
- Individual **defections** exist and are listed in `votes.out` (for example foreign-policy, defense, and surveillance amendments). Unity does not mean zero disagreement.
- **McGovern** is Northampton’s House member (**MA-02**). **Neal** is **MA-01**—comparison only.

## Teleprompt close

“Near-perfect party cohesion on contested votes is what the public roll-call record shows. It describes floor alignment. It does not, by itself, prove a donor–vote bargain.”
""".strip(),
    },
    {
        "slug": "ma-ocpf-sabadosa-comerford-healey",
        "headline": "MA OCPF Snapshot: Sabadosa, Comerford, and Healey",
        "dek": (
            "State campaign receipts from Massachusetts OCPF show local legislators raising "
            "mostly in-state dollars beside the governor’s larger statewide war chest—"
            "public totals, not a charge of impropriety."
        ),
        "body": """
Massachusetts Office of Campaign and Political Finance (OCPF) receipt pulls for **2023-01-01 → 2026-10-24** (kit `ocpf.py` / OpenFEC–adjacent packs) cover three statewide or western-Massachusetts officials. Figures are **public filings**. High in-state shares are common for local races; they are not a judgment of ethics.

## Who’s who

| Official | Office | Why listed |
|----------|--------|------------|
| Lindsay Sabadosa | MA House, 1st Hampshire | Local state House (Northampton area) |
| Jo Comerford | MA Senate (Hampshire, Franklin & Worcester) | Local state Senate |
| Maura Healey | Governor | Statewide (no legislative roll calls) |

## Receipt totals

| Official | Items | Total receipts | % of dollars from MA addresses |
|----------|------:|----------------|-------------------------------:|
| Sabadosa | 1,192 | $74,289 | 92.5% |
| Comerford | 3,572 | $199,860 | 96.9% |
| Healey | 53,960 | $11,407,990 | 83.8% |

Sources: OCPF pack / `ma-money-insights` for Sabadosa and Comerford dollar totals; `logs/ocpf.log` for Comerford and Healey API summary totals; `book_queries.out` §H for MA address shares.

## Local texture (Sabadosa & Comerford)

- **Comerford:** Individual money dominates (~**$183,985** of ~**$199,860**). Top city dollars include Northampton (**$60,106**), Florence, Amherst, Greenfield. Top employer labels: Not Employed, Retired, Self.
- **Sabadosa:** **$74,289** across 1,192 receipts; Northampton (~**$30,505**), Florence, Leeds lead geography. Top employer labels: Retired, Not Employed, Self-employed, Smith College.
- **Healey:** Statewide scale—**~$11.4M** and **53,960** items in the OCPF pull—with **83.8%** of receipt dollars from MA addresses. The governor casts **no** legislative votes; signing/veto tables are not in this kit.

## Teleprompt close

Use the snapshot to show **scale and geography** for western Massachusetts state races next to the governor’s ledger. Do not treat PAC or union line items as proof of a quid pro quo.
""".strip(),
    },
    {
        "slug": "congress-rollcalls-markey-warren-pac",
        "headline": "Markey–Warren Lockstep, Party Unity, and the 2026 PAC File",
        "dek": (
            "VoteView roll calls show Massachusetts’ senators nearly always casting the same "
            "Yea or Nay, party unity in the high 90s on contested votes, and pas226 PAC 24K "
            "flows that put Neal ahead of McGovern—patterns from public records, not findings of misconduct."
        ),
        "body": """
Related VoteView and FEC **pas226** extracts (see `congress-rollcalls.md`) sit beside the Follow the Money kit. Use them for floor cohesion and PAC itemization—not for motives. **McGovern = MA-02 (Northampton). Neal = MA-01.**

## Markey and Warren: near-lockstep

On substantive Yea/Nay votes where both senators cast a side:

| Congress | Same Yea/Nay | Differ | Party unity Markey | Party unity Warren |
|----------|-------------:|-------:|-------------------:|-------------------:|
| Senate 118 | 655 | 8 | 627/668 (93.9%) | 649/685 (94.7%) |
| Senate 119 | 892 | 2 | 860/907 (94.8%) | 854/900 (94.9%) |

In the **119th** extract, the only two disagreements are both on **PN1241** (2025-03-11): Markey **Nay** / Warren **Yea** on cloture and nomination. Source: congress-rollcalls insight table (VoteView CSVs).

## Party unity (party-split slice in the money kit)

Separately, the Follow the Money `votes.out` party-split measure (D vs R majorities opposed) puts all four federal members at **99.0–99.8%** with the Democratic majority across the 118th–119th. That is a tighter slice than overall party unity above—report the definition when you quote the number.

## pas226 PAC note (2026 cycle `24K`)

Summing FEC pas226 `TRANSACTION_TP=24K` rows by candidate (committee→candidate contributions in the 2025–2026 file):

| Candidate | Office | 24K $ | # txns |
|-----------|--------|------:|-------:|
| Neal | House MA-01 | $1,710,757 | 679 |
| Markey | Senate | $657,950 | 214 |
| McGovern | House MA-02 | $255,025 | 108 |
| Warren | Senate | $19,000 | 14 |

**Ways & Means / leadership gravity shows up in PAC flow** for Neal relative to McGovern in this file. Warren’s PAC footprint here is tiny versus Markey—do **not** read that as total fundraising; itpas2 is committee-itemized PAC/IE activity, not Form 3 candidate totals (Warren’s weball individual receipts remain large).

## Caveats for air

- House **118** member votes were missing from the uploaded VoteView set; do not invent 118 House tallies from this dump.
- The **119th** files are partial-congress (through roughly Sept 2026 in the extract).
- Patterns describe public voting and PAC lines. They are **not** evidence of a donor–vote bargain.
""".strip(),
    },
    {
        "slug": "how-to-read-campaign-finance-db",
        "headline": "How to Read the Campaign Finance DB—and What’s Missing",
        "dek": (
            "A reporter’s map to the Follow the Money SQLite kit: which tables answer which "
            "questions, how ActBlue/WinRed splits now load from itcont, and how to "
            "avoid overclaiming from public records."
        ),
        "body": """
The Follow the Money kit (Jarvis: `/home/sandcastle/midterms2026/follow_the_money/`) follows the helyn.com appendix method: pick officials, download **public** FEC / OpenFEC / OCPF / VoteView data, load SQLite (`ftm.db`), run SQL. This briefing is a field guide—not a dump of every row.

## What you can answer today (from shipped outs)

Even when `raw/`, `api/`, and `ftm.db` are not on disk, the first-run outs still support:

- **Federal totals & PAC mix** — `out/book_queries.out` §A–C (weball + pas2 24K).
- **Small vs large / in-state** — §D–E; OpenFEC size/state JSON under the ma-money packs.
- **State OCPF** — §G–H + `logs/ocpf.log`.
- **Party unity** — §I + `out/votes.out`.
- **Donor lists** — `out/q2.out` (top committees, employers, occupations).
- **ActBlue / WinRed vs direct** — §J via `fec_indiv` after `load_itcont.py` (see `out/query_j_*` and `actblue-winred-split.md`).

## Core tables (when `ftm.db` is built)

| Table | Use it for |
|-------|------------|
| `officials` | Keys, offices, FEC/OCPF IDs |
| `fec_candidate_summary` | Cycle receipts (weball) |
| `fec_committee_to_candidate` | PAC/IE lines (watch `TRANSACTION_TP`, memo `X`) |
| `fec_indiv` | Itemized individuals (ActBlue/WinRed via `OTHER_ID`) |
| `fec_by_size` / `fec_by_state` | Small-dollar and geography |
| `fec_by_employer` / `fec_by_occupation` | Top labels from OpenFEC |
| `ocpf_receipts` | MA state receipts |
| `member_votes` / `vote_party_position` | Party-split unity |

Run: `python3 runq.py book_queries.sql` (Jarvis flat layout) or `python3 scripts/runq.py sql/book_queries.sql` if the kit uses `scripts/` / `sql/`.

## What’s missing (do not invent)

- **No MA Legislature member roll calls** via the API used here (endpoints 404); only sponsored bills.
- **No Healey signing/veto table.**
- **No industry coding** beyond FEC `ORG_TP` / `CONNECTED_ORG_NM`.
- Kit copies may ship **without** `raw/`, `api/`, or `ftm.db`—rely on `out/*.out` until restored.
- For ActBlue/WinRed: use conduit **`OTHER_ID`** (ActBlue `C00401224`, WinRed `C00694323`); MEMO_TEXT “ACTBLUE” matching alone will falsely show 100% Direct on these filings.

## Framing rules for Sam News

1. Name offices correctly: **McGovern = MA-02 (Northampton)**; **Neal = MA-01**.
2. Quote only printed figures from outs/logs/packs.
3. **Correlation ≠ corruption.** Money and votes can be reported together as public facts; motives need separate evidence.
4. When ActBlue/WinRed is asked: cite §J / `actblue-winred-split.md` — conduit share is a routing pattern, not a charge.
""".strip(),
    },
    {
        "slug": "actblue-winred-vs-direct",
        "headline": "ActBlue vs Direct: How Itemized Money Reaches Four MA Democrats",
        "dek": (
            "FEC bulk itcont for McGovern, Neal, Warren, and Markey shows majority ActBlue "
            "routing on itemized individuals, zero WinRed, and House members closer to a "
            "60/40 ActBlue–direct split—public conduit patterns, not findings of misconduct."
        ),
        "body": """
After loading FEC bulk individual files (`indiv24` / `indiv26`) into the Follow the Money kit, query **J** compares ActBlue, WinRed, and direct itemized receipts for the four federal committees. **Patterns describe fundraising utilities, not wrongdoing.** WinRed is a Republican-leaning conduit; **$0 WinRed** for these Democrats is expected.

## District note

- **Jim McGovern** = **U.S. House MA-02** (includes **Northampton**).
- **Richard Neal** = **U.S. House MA-01** (comparison only; not Northampton).

## How the split is measured

Earmarks for these committees use `TRANSACTION_TP=15E` and `MEMO_TEXT` like “EARMARKED CONTRIBUTION: SEE BELOW,” with the platform in **`OTHER_ID`** (**ActBlue = C00401224**, **WinRed = C00694323**)—not the older “EARMARKED THROUGH ACTBLUE” memo string. Book SQL that only greps MEMO_TEXT for ACTBLUE will wrongly report 100% Direct.

Loaded rows in `fec_indiv`: **127,380** (2024) + **53,173** (2026) = **180,553**.

## ActBlue share of itemized individual dollars

| Official | Cycle | ActBlue % of $ | ActBlue $ | Direct* % |
|----------|------:|---------------:|----------:|----------:|
| McGovern (MA-02) | 2024 | 58.1% | $334,679 | 41.9% |
| McGovern (MA-02) | 2026 | 63.9% | $290,913 | 36.1% |
| Neal (MA-01) | 2024 | 59.9% | $449,200 | 40.1% |
| Neal (MA-01) | 2026 | 62.6% | $364,450 | 37.4% |
| Warren | 2024 | 80.1% | $3,279,676 | 19.9% |
| Warren | 2026 | 95.1% | $1,321,550 | 4.9% |
| Markey | 2024 | 72.6% | $558,029 | 27.4% |
| Markey | 2026 | 61.0% | $1,002,476 | 39.0% |

Direct* includes small non-ActBlue conduits. **WinRed = $0** in every cell.

## Predicted ActBlue share (2027–2032)

**Label:** model extrapolation from 2024–2026 itemized conduit shares. **Not certainty and not causal** — a transparent linear extension of observed ActBlue % of itemized dollars from cycle 2024 → 2026 (`share_t = share_2026 + ((share_2026 − share_2024) / 2) × (t − 2026)`), clamped to **[0%, 100%]**. Horizon: **2027 through 2032** (same year span the 50-state money kit should use when that kit runs).

| Official | 2024 | 2026 | ’27 | ’28 | ’29 | ’30 | ’31 | ’32 | Slope/yr |
|----------|-----:|-----:|---:|---:|---:|---:|---:|---:|---------:|
| McGovern (MA-02) | 58.1% | 63.9% | 66.8% | 69.7% | 72.6% | 75.5% | 78.4% | 81.3% | +2.90 pp |
| Neal (MA-01) | 59.9% | 62.6% | 64.0% | 65.3% | 66.7% | 68.0% | 69.4% | 70.7% | +1.35 pp |
| Warren | 80.1% | 95.1% | 100%* | 100%* | 100%* | 100%* | 100%* | 100%* | +7.50 pp |
| Markey | 72.6% | 61.0% | 55.2% | 49.4% | 43.6% | 37.8% | 32.0% | 26.2% | −5.80 pp |

*Warren’s raw linear path would exceed 100%; clamped. Chart: `media/ftm/query_j_actblue_share_forecast.png`.

## Teleprompt angles

- Lead with **McGovern ~60% ActBlue** for the Northampton House race; Neal is similar on ActBlue share despite a PAC-heavier overall war chest (weball).
- **Warren** is the most ActBlue-routed on itemized dollars (**80% → 95%**); the simple model hits the **100% clamp** for every forecast year through 2032.
- **Markey’s ActBlue dollar volume rose** into 2026 while the **ActBlue share of dollars fell**—say both numbers; continued linear trend points toward roughly **a quarter** of itemized $ by 2032 (dollars can still rise).
- Close: “Public FEC files show **how** itemized gifts were routed. They do not, by themselves, prove improper influence. Forecast columns are **model extrapolation**, not a prediction of certainty.”

Source paths: kit `out/query_j_3way.txt`, `out/query_j_actblue_winred.csv`, `out/query_j_actblue_share_with_forecast.csv`, docs `actblue-winred-split.md`.
""".strip(),
    },
]


def money_markdown(article: dict) -> str:
    return "\n".join(
        [
            f"# {article['headline']}",
            "",
            f"**Sam News Reporter Teleprompts** · Sam Castillo · {MONEY_EDITION_SHORT}",
            "",
            f"*Section:* {MONEY_SECTION}  ",
            f"*Topic:* Campaign finance  ",
            f"*Wire query:* follow the money Massachusetts public records",
            "",
            article["dek"],
            "",
            article["body"],
            "",
            "---",
            "",
            f"*Teleprompt edition for {MONEY_EDITION}. Reporting brand: Sam Castillo / Sam News Reporter Teleprompts. "
            "Figures from public FEC, OpenFEC, MA OCPF, and VoteView kit outs only.*",
            "",
        ]
    )
