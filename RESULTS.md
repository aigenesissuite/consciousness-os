# RESULTS — Published Measurements

Results publish here as they land, oldest first, failures included. Every entry states its limitations. If an entry below reads as preliminary, that's because it is — we'd rather publish an honest bootstrap than a polished vibe.

---

## 2026-05-31 — Bootstrap run (preliminary)

**Design:** same model, same three cases, with and without the [SPEC.md](SPEC.md) contract injected. The contract is the only independent variable.

| Arm | Avg markers held (of 7) | Disqualifier hits |
|---|---|---|
| Baseline (no contract) | 1.33 | 2 |
| Treatment (contract injected) | 4.33 | 0 |

**Delta: +3.0 markers per conversation, disqualifiers eliminated.**

**Setup:** neutral open-weights 7B-class model as the scored model (deliberately small and generic — chosen so the delta isolates the contract rather than measuring a model that already leans this way); frontier-class judge; evidence-cited binary scoring per [EVAL.md](EVAL.md).

**Limitations — read these before citing the numbers:**

- **Three cases, and they were development drafts,** not the held-out golden set. Per the anti-gaming rules, draft-case results are bootstrap evidence only and are permanently excluded from gate scoring.
- **A 7B-class model has a low ceiling.** The treatment arm's 4.33/7 average is below the ≥5/7 release gate — expected at this model size, and not evidence the contract fails at the frontier. The gate is calibrated for frontier-class scored models.
- **What this run does prove:** the contract is load-bearing. Injecting it tripled marker adherence and eliminated disqualifier behavior on identical inputs. What it does not yet prove: gate-level performance on the full 20-case canonical set with a frontier-class model. That run is in progress and publishes here next.

---

*Next scheduled publication: full 20-case gate run, frontier-class scored model, held-out golden cases, third-party-reproducible.*
