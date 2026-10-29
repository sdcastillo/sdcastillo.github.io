# How to Read the Campaign Finance DB—and What’s Missing

**Sam News Reporter Teleprompts** · Sam Castillo · Oct 24, 2026

*Section:* Follow the Money  
*Topic:* Campaign finance  
*Wire query:* follow the money Massachusetts public records

A reporter’s map to the Follow the Money SQLite kit: which tables answer which questions, how ActBlue/WinRed splits now load from itcont, and how to avoid overclaiming from public records.

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

---

*Teleprompt edition for Saturday, October 24, 2026. Reporting brand: Sam Castillo / Sam News Reporter Teleprompts. Figures from public FEC, OpenFEC, MA OCPF, and VoteView kit outs only.*
