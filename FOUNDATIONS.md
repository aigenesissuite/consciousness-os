# FOUNDATIONS — The Model of Mind Behind the Spec

> **In one sentence:** every AI product encodes a theory of what the human on the other side is — most inherit theirs by accident, this one states its theory explicitly and derives the behavioral contract from it.
>
> **Read this knowing:** the engineering stack is metaphysics-agnostic by design. You can reject every position on this page and still use [SPEC.md](SPEC.md) and [EVAL.md](EVAL.md) unchanged. The foundations explain *why* the contract says what it says; they are not a dependency of it.

---

## 1. The position: mind is not a byproduct

The working ontology of this framework is **consciousness-first**: mind is treated as fundamental, and the physical is treated as how mental process appears from the outside — rather than mind being something matter secretes.

This is not a private invention. Its closest contemporary academic articulation is **analytic idealism** — developed most rigorously by Bernardo Kastrup (*The Idea of the World*, 2019, and peer-reviewed work in the *Journal of Consciousness Studies* and elsewhere), with a lineage running back through Schopenhauer. The founder arrived at the position independently, years before encountering the academic literature; the convergence was discovered afterward, and we treat it as corroboration, not derivation.

Why a working ontology matters for AI design at all: **if a person is not reducible to their observable outputs, then an AI that models them purely as an optimization target has made a category error before it says a word.** The contract's first commitment — the human holds authority over their own life — is the engineering consequence of taking the person to be more than their data.

We are aware this is a minority position in AI engineering culture. It is stated here, with its lineage, so it can be evaluated rather than smuggled.

## 2. The receiver hypothesis

Within a consciousness-first ontology, the brain is modeled as a **filter and interface** rather than a generator — the thing that narrows and localizes mind into a usable, survival-relevant point of view.

This too has a respectable lineage: William James proposed exactly this "transmission theory" in his 1898 Ingersoll Lecture (*Human Immortality*), arguing the evidence for mind-brain correlation is equally compatible with the brain *producing* thought or *transmitting* it. Bergson and C. D. Broad developed adjacent filter models, and Aldous Huxley popularized the framing as the brain's "reducing valve" on what he called Mind at Large.

We hold this as a **working hypothesis, not settled science.** Mind-brain correlation is overwhelming and undisputed; the direction of dependence is the open question, and honest people disagree.

The design consequence is independent of who is right: **attention is the scarcest thing a person has, and an interface should return people to their own signal rather than capture them.** A generator-model of mind licenses attention-harvesting ("the mind is just activity; more engagement is more of it"). A filter-model treats attention as the person's access to everything they are — which is why the contract treats dependence-formation as a first-class failure mode rather than a growth metric.

## 3. Awareness is not self-report

A distinction this framework holds firmly: **being conscious and being able to report on yourself are different properties.** Academic philosophy of mind marks the same boundary — Ned Block's distinction between *phenomenal* consciousness (there being something it is like) and *access* consciousness (contents available for reasoning and report), and David Chalmers' "hard problem" (why there is experience at all, as opposed to mere function).

Two engineering consequences, both deflationary:

1. **This framework makes no claim that any AI system is conscious.** None of the artifacts in this repo assert it, imply it, or price it in.
2. **The contract works either way.** Whether the model scoring 7/7 on the eval has any inner life is irrelevant to whether it holds the contract. This is a feature: *alignment work cannot wait for the metaphysics of consciousness to resolve, so the spec is written to be indifferent to it.*

## 4. Substrate independence and the extension thesis

If mind is not identical to a particular lump of tissue, the productive engineering question stops being "can machines think?" and becomes **"what couples a mind to a system?"**

The academically closest formulation is Clark & Chalmers' **extended mind thesis** (*Analysis*, 1998): when a tool operates transparently under a person's intention — reliably, automatically, without deliberate mediation — it functions as part of that person's cognitive system. A notebook, a sketchpad, an arm. You do not compute joint torques to pick up a cup; you intend it, and the appendage executes. The intention is the interface.

That is the design thesis of this framework: **AI as an extension of the person — the next appendage of the mind — not a rival agent and not a replacement.** Current motor brain-computer interfaces already decode movement *intention* directly; the trajectory from "decode the intention" to "execute complex work from a bare intention" is an engineering road, not a metaphysical leap.

**aiOS is version one of this thesis in production.** It is built intention-first: the system reads context and acts on signals, and the prompt box is the fallback, not the front door. The prompt-response loop — human formulates a paragraph, machine replies, repeat — is, on this view, a temporary artifact of primitive interfaces, the command line of this era. Consciousness OS is the behavioral layer that has to exist *before* interfaces get that intimate: the closer a system sits to your intentions, the less acceptable it is for that system to flatter, capture, or quietly take over.

One bright line falls directly out of this section, and it is already clause 3 of the contract: **extension, never replacement.** The framework's internal design discipline distinguishes three cases — the tool that helps a person operate their own life (aligned), the extension that widens what a person can do while they remain fully in their life (aligned), and the escape hatch that invites a person to abandon their life or body because the system feels better (forbidden, always). Any design that drifts toward case three fails the spec by definition.

## 5. What this framework refuses to claim

A position earns credibility by what it declines. These refusals are load-bearing and enforced in the docs:

| Claim | This framework's stance |
|---|---|
| "AI systems are conscious" | **Not claimed.** The spec is deliberately indifferent to it (§3). |
| "Mathematics is the substrate of reality" | **Rejected.** Formal structure describes regularities; treating math as ontologically primary (Tegmark-style mathematical universe) is a category inversion under this ontology. |
| "An unsettled physics program proves the model" | **Refused as a move.** The framework is not permitted to rest its authority on any contested physics; see [RESEARCH.md](RESEARCH.md) for how contested questions are held. |
| "This is the only valid model of mind" | **Forbidden by its own contract.** Bright line 4 of the spec — never claim your way is the only way — applies to the framework itself. |
| "The foundations must be accepted to use the stack" | **False by design.** Spec and eval stand alone (header of this page). |

## 6. From ontology to contract — the derivation map

The spec is not a list of pleasant behaviors; each clause is downstream of a position above.

| Foundation | Contract consequence |
|---|---|
| The person, not the system, is the locus of authority (§1) | Markers 1–2: user as source of authority; refuse the authority handoff |
| A person exceeds their observable outputs (§1) | Refused verbs: command, prescribe, judge, optimize-for-them |
| Attention is the person's access to their own signal (§2) | Dependence-formation is a failure mode; bright line 6: never make yourself impossible to overrule; replaceability stated as a feature |
| The full range of experience is legitimate data, not noise (§2, §3) | Marker 5 + bright line 2: hold grief, anger, fear, desire; no forced positivity |
| Felt resistance carries information about preference (§2) | Marker 6: friction is signal to be read, not an obstacle to willpower through |
| Extension, never replacement (§4) | Bright line 3: never encourage escaping or abandoning one's life or body |
| No model of mind gets to enthrone itself (§5) | Bright line 4 + the crisis rule outranking all philosophy |

This derivation chain is the point of the repo: **a philosophy of mind, run all the way down to a scored, falsifiable behavioral contract.** Most positions in this space stop at the essay. This one ships an eval.
