# ActBlue vs Direct: How Itemized Money Reaches Four MA Democrats

**Sam News Reporter Teleprompts** · Sam Castillo · Oct 24, 2026

*Section:* Follow the Money  
*Topic:* Campaign finance  
*Wire query:* follow the money Massachusetts public records

FEC bulk itcont for McGovern, Neal, Warren, and Markey shows majority ActBlue routing on itemized individuals, zero WinRed, and House members closer to a 60/40 ActBlue–direct split—public conduit patterns, not findings of misconduct.

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

---

*Teleprompt edition for Saturday, October 24, 2026. Reporting brand: Sam Castillo / Sam News Reporter Teleprompts. Figures from public FEC, OpenFEC, MA OCPF, and VoteView kit outs only.*
