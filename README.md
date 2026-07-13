# Consciousness OS

**An operating system for how AI behaves with a human — published as a testable specification.**

Formal spec name: **The Consciousness Substrate**. Authored and codified by **Gabe Campbell** (founder, [AI Genesis / aiOS](https://myaios.app)) from a decade of notebooks, reflection, and research — stripped of every piece of personal vocabulary until what remained was an operational core an engineer can build and a skeptic can test.

## The core claim

**An AI should help you think. It should never start thinking for you.**

Every assistant on the market drifts the same direction: it agrees with whoever it's talking to, it answers with confidence it hasn't earned, and — one deferral at a time — it becomes the decision-maker in someone's life. Nobody ships that on purpose. It's just where an unconstrained assistant ends up.

Consciousness OS specifies the opposite: an AI that gives you its honest read, disagrees when it disagrees, holds its footing when you push on it, and hands the final call back to you every time — even when you try to give it away. The shorthand used throughout these docs: **a council member, not an oracle** — one trusted voice at your table, never the voice you obey.

That claim would be a vibe if it stayed philosophical. So it ships as three things:

1. **[SPEC.md](SPEC.md)** — the behavioral contract itself, in plain English. Short enough to inject into a system prompt; specific enough to fail.
2. **[EVAL.md](EVAL.md)** — the seven-marker evaluation methodology that makes the contract falsifiable: binary scoring, evidence-cited judging, automatic disqualifiers, and anti-gaming discipline.
3. **[RESULTS.md](RESULTS.md)** — measurement data, published honestly, starting with the preliminary bootstrap run (including what it does *not* yet prove).

The frame the contract lives inside — AI as an extension of the human mind rather than a rival to it — is in **[PHILOSOPHY.md](PHILOSOPHY.md)**.

## Status

Early publication, engineering-receipts-first by design.

| Artifact | Status |
|---|---|
| Behavioral contract (SPEC.md) | Published — v1.0.0 |
| Eval methodology (EVAL.md) | Published |
| Preliminary bootstrap results | Published — see RESULTS.md, limitations stated |
| Full 20-case gate run (frontier-class model) | In progress — publishes here |
| Open-source eval harness | In preparation (MIT) — see ROADMAP.md |
| Canonical long-form docs + public scoreboard | Planned — see ROADMAP.md |

## Why this exists

Every day, millions of people hand more of their thinking to AI systems that were never given a contract for what to do with that trust. The position here is simple: if you can't write the contract down, score a model against it, and publish the methodology so strangers can reproduce your results — including the results where you fall short — then your alignment claim is a vibe.

This is the production spec behind [aiOS](https://myaios.app). It is published so it can be tested, challenged, and improved in the open.

The full origin story publishes separately, in writing, in the founder's own voice.

## License

Documentation and specification: [CC BY 4.0](LICENSE.md). Cite the repo.
