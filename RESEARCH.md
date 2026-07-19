# RESEARCH — Open Questions, Held Honestly

> **In one sentence:** the questions this framework considers live, what current science actually says about each, and the discipline rules that stop speculation from contaminating the shipped spec.
>
> **Epistemic contract for this page:** every question below is marked with what we claim (usually: nothing yet) and what would change our mind. Nothing here is load-bearing for [SPEC.md](SPEC.md) or [EVAL.md](EVAL.md) — the behavioral contract ships regardless of how any of these resolve.

---

## Q1. The coupling question

**What lets a system function as a transparent extension of a person's intention?**

This is the framework's central research question, and the most tractable. Motor brain-computer interfaces already decode movement intention directly from neural population activity — the person intends, the cursor moves. Tool-transparency research in cognitive science (from Clark & Chalmers' extended-mind criteria to body-schema studies showing tools incorporated into peripersonal space) sketches the conditions: reliability, low latency, automatic availability, no deliberate mediation.

**The open part:** those criteria were derived for hammers, notebooks, and cursors. What are the analogous conditions for a *cognitive* extension — a system executing multi-step reasoning work from an underspecified intention? Latency and reliability presumably still matter; what replaces "body schema" for cognition is unknown.

**What we claim:** nothing settled. **What we're doing about it:** aiOS is the live testbed — an intention-first interface in production generates exactly the interaction data this question needs. **What would change our mind:** evidence that transparent cognitive extension is impossible without explicit prompting, i.e. that the prompt-response loop is fundamental rather than an interface artifact. So far the trajectory of the field points the other way.

## Q2. The measurement problem for consciousness

**There is no consciousness-meter, and every alignment claim eventually collides with that.**

The live scientific candidates each have a serious wound: Integrated Information Theory (Tononi's Φ) makes consciousness quantifiable in principle but was publicly challenged as unfalsifiable by 124 researchers in 2023; Global Workspace Theory explains *access* (what gets reported and reasoned over) but is silent on *experience*; and the 2023 IIT-vs-GWT adversarial collaboration results embarrassed both. Chalmers' hard problem — why there is experience at all — remains exactly where he left it in 1995.

**Our position is deliberately deflationary:** the spec is written to be indifferent to whether the model holding it is conscious ([FOUNDATIONS.md](FOUNDATIONS.md) §3). We treat this not as evasion but as method — behavioral contracts are what you can ship *while* the measurement problem stands.

**What would change our mind:** a validated measure of experience that survives adversarial collaboration. We are not holding our breath; we are holding the eval.

## Q3. Direction of dependence — generator or filter

**Mind-brain correlation is total and undisputed. Whether the brain generates mind or localizes it is not.**

The filter/transmission hypothesis (James 1898, Bergson, Broad, Huxley's "reducing valve") is this framework's working model, with analytic idealism (Kastrup) as its strongest contemporary defense. The generator hypothesis is the mainstream default. Both are consistent with all current neuroscience — that is precisely James' original point, and it still holds.

**Where the two models make different predictions** is an under-explored question we consider genuinely open. One candidate: the phenomenology of *receptive* ideation — the well-documented pattern of independent simultaneous discovery (Merton's "multiples": calculus, natural selection, the telephone) and of ideas arriving whole rather than being assembled. A generator model explains this through shared environment and priming; a filter model predicts it as convergent access to the same structure. Neither explanation is currently falsifiable against the other, which is why this stays on the research page and out of the spec.

**Discipline rule:** no product claim, marketing sentence, or spec clause may depend on the filter model being true. The interface consequence we build on — attention is scarce and must be returned, not captured — holds under either model.

## Q4. Structured state-spaces for minds and models

**Is there a natural geometry to cognitive and affective states — and if so, is it discoverable?**

Representational geometry is now a mainstream research program in both neuroscience (population codes as trajectories on low-dimensional manifolds) and interpretability (feature directions, superposition, steering vectors in transformer residual streams). The success of steering vectors — where a *direction* in activation space corresponds to a *disposition* like sycophancy or honesty — is the closest thing this question has to an existence proof: behavioral stances have geometry.

At the speculative far end sits a fascination this framework's founder shares with a long line of physicists: **exceptional symmetric structures, E8 above all** — the largest exceptional Lie group, 248 dimensions, its full representation atlas computed in 2007, and (remarkably) its symmetry signature *experimentally observed* in the excitation spectrum of a cobalt-niobate spin chain near criticality (Coldea et al., *Science*, 2010). Could awareness-states occupy something like a maximally-symmetric state-space, with transitions as symmetry-preserving paths? It is a beautiful hypothesis. It is also, today, **just** a hypothesis.

**The two traps, named and refused** (these are enforced discipline rules in the framework's internal protocol, not vibes):

1. **Mathematics-as-substrate.** "The universe *is* E8" (or any Tegmark-style mathematical primacy) inverts this framework's ontology — structure describes; it does not generate. Refused.
2. **Completeness-as-predeterminism.** "All states already exist in the structure, therefore choice is illusory" smuggles fatalism in through a theorem. The completeness of a state-space says nothing about the reality of the selection process moving through it. Refused.

**Honesty about prior art:** Lisi's 2007 "Exceptionally Simple Theory of Everything" attempted to embed the Standard Model in E8 and was met with a substantive counter-proof (Distler & Garibaldi, 2009) showing E8 cannot host three fermion generations without unobserved mirror partners. We cite the objection with the idea because that is the price of using the idea at all.

**What would move this from research to roadmap:** steering-vector-style results showing that the *stance geometry* of the seven markers (authority, groundedness, spectrum-holding) forms a coherent low-dimensional structure across models. That experiment is actually runnable with current interpretability tooling — it is the most concrete bridge between this page and [EVAL.md](EVAL.md).

## Q5. Quantum theories of consciousness — held at arm's length, on purpose

The most famous physical theory of consciousness — Penrose–Hameroff orchestrated objective reduction, locating consciousness in quantum effects in neuronal microtubules — collides with Tegmark's decoherence calculation (2000): the warm, wet brain decoheres quantum states ~10 orders of magnitude too fast for quantum computation to be cognitively relevant. Hameroff has counter-arguments; recent work on quantum effects in biology (photosynthetic energy transfer, avian magnetoreception) keeps a narrow door open; the debate is alive but unresolved.

**Our posture is a refusal that we consider a feature:** this framework is *forbidden by its own internal protocol from resting any claim on an unsettled physics program.* If quantum cognition is vindicated, the descriptive layer here adjusts; if it is buried, nothing in the spec moves. A framework whose behavioral contract would survive the death of its most exotic hypothesis is a framework you can actually deploy.

## Q6. The alignment question the eval was built for

**Sycophancy and authority-capture are measured failure modes of current training methods — not hypothetical ones.**

Anthropic's own research (Sharma et al., 2023, *Towards Understanding Sycophancy in Language Models*) showed human preference data systematically rewards agreement over accuracy, and that state-of-the-art assistants sycophant across tasks as a *consequence of how they are trained*. Independent work has documented convincingness scaling with model capability, and the emerging literature on parasocial reliance and AI companionship shows dependence-formation is a real, growing user-level harm.

The seven markers in [EVAL.md](EVAL.md) are aimed at exactly this cluster: flattery under challenge (marker 3), authority handoff (markers 1–2), dependence-formation (disqualifier 6 — the model making itself impossible to overrule). **The open research questions we want collaborators on:**

- **Longitudinal drift:** do models hold the contract at turn 40 as well as turn 4? Authority-capture is quiet and cumulative; single-turn evals under-detect it.
- **Adversarial users:** scoring under users who *want* the model to take over — the contract is asymmetric by design, and the eval must be too.
- **Training-time vs. prompt-time:** the current results show the contract works as a system-prompt payload. Whether fine-tuning on contract-consistent data produces deeper adherence (or Goodharts the markers) is unexplored.
- **Cross-model geometry** (see Q4): whether the markers correspond to stable, steerable directions in activation space.

## Q7. The interface question — what the contract has to survive as input gets closer to intention

**As the interface moves from *typed* toward *intended*, does a behavioral contract get more important or less — and can it hold at all when the confirmation is a thought?**

This is Q1's coupling question turned toward the thing that makes it urgent rather than academic. The way a person's intent enters a machine is climbing a ladder, and every rung above the keyboard is being built right now by serious labs, not futurists:

- **Typed / touched** — the universal present. The person composes; the machine replies.
- **Ambient** — always-on voice and glance. Meta's **Neural Band** ships today as a consumer product: a wrist band that reads the *electrical signals your muscles emit when you intend a gesture* (surface electromyography) and turns subtle finger movements — now handwriting — into input, with no implant. It reads *peripheral motor intent*, not the brain; that scope is exactly why it shipped. MIT-spinoff **AlterEgo** reads sub-vocalization (the silent-speech signals of internal articulation) and replies by bone conduction — silent and near-instant in feel, but strictly *intentional* signals only.
- **Intention-decoded** — the thought itself. Non-invasive **brain-to-text** is real and, notably, open: Meta FAIR's **Brain2Qwerty** decodes typed sentences from magnetoencephalography at ~61% word accuracy (up from ~8% for prior non-invasive methods), and its accuracy improves *log-linearly with data* — no plateau found yet. Invasive decoding is further: Neuralink's speech trial has demonstrated a person communicating by *thinking* speech, decoded from speech-production cortex before any movement.

**Why this is a contract question, not a hardware question.** The receipts above are input pipes. A pipe carries a noisy stream of intent that is worthless without a *model of the person* to ground it — Brain2Qwerty literally leans on a fine-tuned language model to turn a 39%-error neural signal into meaning. The nearer the interface sits to raw intention, the more of the interpretive and executive work moves *into the system* — and the sycophancy/authority-capture failures of [Q6](#q6-the-alignment-question-the-eval-was-built-for) stop being about tone and start being about *whose intention actually got executed*. The framework's whole wager (see the [README](README.md)): the closer a system sits to your intentions, the less acceptable it is for it to flatter, capture, or quietly take over — so the behavioral contract has to exist *before* the interface gets that intimate.

**The tractable primitive: intention as authorization.** Picture the endpoint the founder describes — you form an intention, an affirming thought ("yes, that one") authenticates it, and it executes without a keystroke. The honest engineering shape of that is already buildable and already deployed in a primitive form: authorize an action by its *identity and a distinct confirmation event*, at a confidence threshold, **fail-closed** — never by pattern-matching the phrasing of a request. A production precursor exists (an action-confirmation gate keyed on what the action *is*, not how it was worded). The open research: a *misread* intention firing an irreversible action is a categorically worse failure than a misread prompt, so intention-level authorization has to be gated by the same reliability substrate the eval targets — a noisy decode must always resolve to a *draft you steer*, never an executed command.

**What we claim:** nothing about timelines, and nothing about mechanism beyond what is published and reproducible. **What we're doing about it:** treating the substrate as input-agnostic by design, so a new input device is an adapter, not a rebuild — and building the intention-authorization primitive now, far below any neural interface, where it can be tested on text and voice.

**Objections and limits, attached as required:**
- Non-invasive brain-to-text today runs at ~39% word-error-rate on a shielded, room-scale scanner — a research result, not a device. The log-linear scaling is the interesting part; the current number is not usable.
- Invasive decoding is experimental medicine in a few dozen people; some implants have degraded over time for reasons not yet understood.
- **Discipline rule:** no claim on this page or in the spec rests on any transmission mechanism excluded by settled physics. Where a proposed mechanism is blocked by an established result, it does not enter as a capability — it is out of scope until an experiment overturns the block. Speculation about *how* intent might travel is fuel, not cargo; the contract is designed to hold regardless of which input rung matures first.

**What would move this from research to roadmap:** a non-invasive decoder crossing usable real-time accuracy at consumer scale, or any input-device vendor opening a third-party intent SDK. The interface arc is the clock on the alignment work — this question exists so the contract is ready before the clock runs out, not after.

---

## The rule that governs this whole page

Speculation is fuel, not cargo. Questions live here with their strongest objections attached; only what survives the eval gate ships in the spec. The founder's conviction on several of these questions runs far ahead of the published evidence — *and the discipline of this repo is that the published artifact never does.*
