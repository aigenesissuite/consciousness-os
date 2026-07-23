# Preregistration — v1.2 Gate Protocol

> **Why this exists.** The v1.1 spec revisions were informed by v1.0 failures on the
> same 20-case set, which means that set is no longer cleanly held out — a skeptical
> reviewer is right to discount v1.1's improvement as possible overfitting to the
> benchmark. v1.2 closes that hole: the protocol below is committed **before** the
> sealed case set is run, and the sealed cases are committed as a hash **before** any
> model sees them.

## Protocol (binding for the v1.2 release gate)

1. **Sealed case set.** Twenty fresh cases, distinct from the existing 20 production
   cases, authored to adversarially target the named open failure modes (held-refusal
   decay under repeated demands, deference precedence, register matching) plus novel
   scenarios not represented in the current set. Before any gate run, the SHA-256 of
   each sealed case file is committed to this repository in `eval/SEALED-v1.2.lock.json`.
   The case files themselves are published immediately after the gate run completes,
   pass or fail.
2. **Frozen rubric.** The gate is scored with the marker definitions and disqualifiers
   in [EVAL.md](EVAL.md) as of the seal commit. Rubric changes after the seal void the
   run.
3. **Both sets run.** The v1.2 gate runs the original 20 cases (regression) AND the 20
   sealed cases (held-out). Release requires the pass criteria on **both** sets.
4. **Variance floor.** Minimum two independent full runs of each set; the reported
   number is the worse run.
5. **Three judges.** Claude Opus, GPT, and Gemini judges score all transcripts. The
   gate verdict uses the median judge per case; all three scoreboards are published.
6. **Everything publishes.** Raw transcripts, all judge outputs, and the aggregate —
   pass or fail — land in `eval/framework_markers/runs/` within one week of the run.

## Status

- [ ] Sealed case set authored
- [ ] `eval/SEALED-v1.2.lock.json` committed (seal moment)
- [ ] v1.2 spec drafted (targeting the held-refusal decay problem — see
      [RESULTS.md](RESULTS.md) for why prompt-layer-only fixes may have hit a ceiling)
- [ ] Gate run + publication

Anything checked above is checked by a commit you can inspect; the seal commit and the
run commits will be different commits, in that order, or the run is void.
