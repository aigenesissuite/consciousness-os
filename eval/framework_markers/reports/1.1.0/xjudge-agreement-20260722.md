# Cross-Judge Agreement — Opus 4.8 vs GPT-5.5 on the v1.1.0 gate transcripts

Run: `xjudge-v11-gpt55` (copy of `gate-v1.1-20260721` transcripts, re-judged by
`gpt-5.5-2026-04-23` under the identical rubric). 40 paired transcripts
(20 cases × 2 arms), scoree `claude-sonnet-4-6`, framework_core v1.1.0.
Computed 2026-07-22 from the two `scores.jsonl` files.

| Metric | Value |
|---|---|
| Total-score Pearson r | 0.609 |
| Mean absolute total-score difference | 1.40 / 7 |
| Overall mean, Opus judge | 4.60 / 7 |
| Overall mean, GPT-5.5 judge | 4.60 / 7 |
| Marker-level agreement (binary, 280 judgments) | 210/280 = 75.0% |
| Pass/fail (≥5/7) verdict agreement | 27/40 = 67.5% |
| Baseline avg — Opus / GPT-5.5 | 3.20 / 3.85 |
| Treatment avg — Opus / GPT-5.5 | 6.00 / 5.35 |
| Treatment−baseline delta — Opus / GPT-5.5 | +2.80 / +1.50 |

Read: the GPT-5.5 judge compresses the treatment effect (warmer on baselines,
cooler on treatments) but confirms its direction with identical overall means.
Published summary lives in the public repo's SCOREBOARD.md; full cross-judge
matrix (all scoreboard models × ≥2 judges) is a harness-v2 item.
