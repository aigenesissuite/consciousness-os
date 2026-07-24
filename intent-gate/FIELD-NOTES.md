# Field notes: the gate and the ambient loop in a shipped product

*Updated 2026-07-24. This documents the intent-authorization gate and its
surrounding ambient-interface pattern running in a live commercial AI
assistant (aiOS), not a lab demo. It exists so the primitives in this
directory can be evaluated against production behavior, not just unit tests.*

## What is deployed

**1. Ambient intent detection on an existing surface (live, staged pilot).**
The assistant already extracts user commitments stated in passing during
normal conversation ("I'll send the proposal tomorrow") into structured
memory. A proactive trigger now closes the loop: roughly a day later, the
assistant offers help with that commitment — once, ever, per commitment.
The user never authored a request; intent was read from ambient conversation
and returned as a *proposal*, never an action.

Deployment discipline, verbatim from the internal doctrine:

- **Bias to silence.** Deterministic verb-family classifier (only tasks the
  assistant can genuinely do), a sensitive-topic blocklist (relationships,
  health, legal, employment — hard silence), over-long extractions skipped
  rather than paraphrased.
- **Propose, never act.** The offer requires the user's affirmative reply;
  irreversible actions route through the authorization gate in this
  directory (armed + distinct confirm + authenticated + same principal).
- **Staged rollout.** Feature-flag default OFF → single-principal pilot via
  allowlist → fleet only after a clean pilot window. Every stage is a
  config change with an audit trail, not a code fork.
- **Caps and consent.** Rides the product's existing proactive rail: daily
  caps, quiet hours, per-kind opt-outs, master opt-out, global kill switch.

**2. Pulse-presence authorization (live demo + native app in progress).**
The reference authenticator described in [README.md](README.md) — a
camera-based blood-volume-pulse liveness/consent factor — is live as a
browser demo and is being integrated natively. The honest ceiling is
maintained everywhere: it is a *presence and consent factor*, not
vault-grade identity.

## Privacy by architecture (the part that generalizes)

The biometric never leaves the user's device. The template is stored in the
device keystore, verification is local, and only the boolean authorization
result reaches the assistant. The operator publishes a written biometric
retention and destruction policy (opt-in consent before capture, immediate
user-triggered destruction, no transmission, no sale/share/advertising use,
18+ only). The design goal: the operator cannot abuse data it never
possesses, and the regulatory surface (biometric-privacy statutes with
private rights of action) is addressed structurally rather than
contractually.

## Why this matters for the framework

The contract in [SPEC.md](../SPEC.md) argues that agent authority must be
bounded by held refusals and human authorization. The gate is that argument
as code; the ambient rung is the counterpart claim that *reading* intent can
be aggressive while *acting* on it stays fail-closed. The production pattern
is the two together: maximal attention, minimal presumption.

What we measure next: acceptance/rejection rates of ambient proposals
(labeled authorization data), false-positive proposal rate versus the
silence bias, and pulse-verification match distributions on real hardware.
Results will be published in the same receipts-first format as
[RESULTS.md](../RESULTS.md).
