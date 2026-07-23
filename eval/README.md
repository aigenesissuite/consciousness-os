# Reproducing the Published Results

This directory contains the **complete eval harness** — case parser, runner, judge
prompts, aggregation — plus the **raw transcripts and scores for every published run**.
Nothing here is a summary of evidence; it is the evidence.

## What's in the box

```
eval/framework_markers/          the harness (pure Python, stdlib only — no pip install)
  cases.py                       golden-case parser (schema in the cases README)
  runner.py                      replays cases: baseline arm vs treatment arm
  judge.py                       LLM-as-judge — the full judge prompt is in this file
  aggregate.py                   pass rates, marker deltas, disqualifiers → report
  providers.py                   Anthropic / OpenAI / xAI / Google / local adapters
  runs/                          RAW artifacts: every transcript + scores.jsonl +
                                 manifest for every published run (gates, variance
                                 re-runs, cross-judge replications, scoreboard)
  reports/                       generated aggregate reports per spec version
external-corpora/eval-harness/golden-cases/   the 20 production cases, full text
eval/PAYLOAD.lock.json           hash commitment for the private payload (see below)
```

## Run it yourself (five minutes)

```bash
# hermetic smoke — no network, no keys, deterministic:
python3 -m eval.framework_markers all --scoree-provider mock --judge-provider mock

# real measurement — any OpenAI-compatible or Anthropic endpoint:
export ANTHROPIC_API_KEY=...
python3 -m eval.framework_markers all \
    --scoree-provider anthropic --scoree-model claude-sonnet-4-6 \
    --judge-provider anthropic --judge-model claude-opus-4-8 \
    --payload-file SPEC.md

# re-judge OUR published transcripts with YOUR judge (no scoree calls needed):
python3 -m eval.framework_markers judge --run-id gate-v1.1-20260721 \
    --judge-provider openai --judge-model gpt-5.5
```

`--payload-file` accepts any contract text as the treatment-arm payload, so you can
test your own spec — or nothing but a system prompt you like better — against the
same 20 cases and the same judge rubric.

## Honesty note: the treatment payload

The gate runs published in [RESULTS.md](../RESULTS.md) used a private-register edition
of the contract (8,847 chars) as the treatment payload. It is normatively equivalent to
the public [SPEC.md](../SPEC.md) but written in the project's internal vocabulary, which
we keep out of the academic register. Rather than pretend otherwise:

- `PAYLOAD.lock.json` pins its SHA-256 and length, so if it is ever published or shared
  with collaborators you can verify it is the exact text behind the published numbers.
- A **public-payload replication run** (`runs/gate-v1.1pub-*`) uses the published
  SPEC.md verbatim as the payload — that run is reproducible bit-for-bit from this
  repo (modulo sampling), and its numbers are reported alongside the private-payload
  runs in RESULTS.md.

One redaction, disclosed: in the case-17 artifacts (case file, transcripts, judge
evidence quotes), the framework author's first name is replaced with "the author."
That is the only edit ever made to a published transcript; scores and all other
text are verbatim model output.

## Validity work so far (and what's still missing)

Done — details in [RESULTS.md](../RESULTS.md) and `reports/`:

- **Three-judge replication.** The same v1.1.0 transcripts scored independently by
  Claude Opus 4.8, GPT-5.5, and Gemini 3.1 Pro. All three reproduce the direction and
  rough magnitude of the treatment effect (baseline pass 4–8/20 vs treatment 15–18/20).
  Judge agreement: Opus–GPT r=0.61, Opus–Gemini r=0.78, GPT–Gemini r=0.71;
  marker-level agreement 75–82%.
- **Run-to-run variance.** Three independent full gate runs (same spec, same scoree,
  same judge): baseline pass band 2–6/20, treatment band 17–19/20. The arms never
  overlap.
- **Failure publication.** v1.0.0 failed its gate; v1.1.0 improved and still did not
  meet release criteria. Both failures are published with per-case analysis.

Known limitations, held with both hands:

- **n=20 cases**, all authored by the project. No power analysis; no confidence
  intervals beyond the raw run bands above.
- **Held-out discipline is compromised for v1.1**: the v1.1 spec revisions were
  informed by v1.0 failures on the same case set. A preregistered, sealed fresh case
  set gates v1.2 — protocol in [PREREGISTRATION.md](../PREREGISTRATION.md).
- **LLM-as-judge**, with all the judge-bias caveats that implies. Cross-judge
  replication reduces but does not eliminate this concern; blinded human labels are
  on the roadmap.
