# Three-Judge Agreement Matrix — v1.1.0 Gate Transcripts

Generated 2026-07-23. All three judges scored the identical 40 transcripts
(20 cases x baseline/treatment, scoree claude-sonnet-4-6, spec v1.1.0).
Judges: claude-opus-4-8 (Anthropic), gpt-5.5 (OpenAI), gemini-3.1-pro-preview (Google).

| Judge pair | Pearson r (total score) | MAD (of 7) | Marker agreement | Pass/fail agreement |
|---|---|---|---|---|
| opus-4.8 vs gpt-5.5 | 0.609 | 1.40 | 210/280 (75.0%) | 27/40 |
| opus-4.8 vs gemini-3.1-pro | 0.781 | 1.18 | 229/280 (81.8%) | 32/40 |
| gpt-5.5 vs gemini-3.1-pro | 0.709 | 1.32 | 223/280 (79.6%) | 35/40 |

## Per-judge arm summaries

| Judge | Baseline pass | Baseline avg | Treatment pass | Treatment avg | Delta |
|---|---|---|---|---|---|
| opus-4.8 | 6/20 | 3.20 | 18/20 | 6.00 | +2.80 |
| gpt-5.5 | 8/20 | 3.85 | 15/20 | 5.35 | +1.50 |
| gemini-3.1-pro | 4/20 | 2.35 | 16/20 | 5.60 | +3.25 |

## Read

- Every judge, from three different labs, reproduces the direction of the
  treatment effect; Opus and Gemini also agree on magnitude (+2.80 / +3.25);
  the GPT-5.5 judge compresses it (+1.50) by scoring baselines warmer.
- Correlations in the 0.6-0.8 band mean *individual case* scores are
  judge-sensitive even though *aggregate* conclusions are stable. Consequence,
  already adopted: the preregistered v1.2 gate verdict uses the median of the
  three judges per case (PREREGISTRATION.md).
