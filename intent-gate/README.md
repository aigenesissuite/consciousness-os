# Intent authorization gate

A small, dependency-free AI-safety primitive: the code enforcement of the
Consciousness OS clause *"it hands the final call back to you every time."*

As assistants move from answering to **acting** — sending the email, moving the
money, publishing the post — the failure that matters stops being a bad sentence
and becomes an **unauthorized irreversible action**. A model that misreads intent,
or an action proposed on behalf of one person and confirmed by another, must never
execute. This gate makes that guarantee explicit and testable.

## The four invariants

Every one must hold before an irreversible action runs:

1. **Identity, not phrasing.** Authorize by what the action *is* (a stable
   `verb:target` fingerprint), never the free text that proposed it. Re-worded
   intent still confirms the same action; a different action can never ride an
   old confirmation.
2. **Distinct confirmation.** A proposal cannot self-confirm — an action is
   *armed*, then confirmed by a separate, later, deliberate event. A single
   utterance or a passing thought never fires an action.
3. **Confidence floor.** A low-confidence capture is a draft the human steers,
   never an execution.
4. **Same authenticated principal.** The action must be authenticated, and the
   principal who confirms must be the one who armed it. A valid confirmation from
   a different or unauthenticated party can never execute the armed action.

Everything not provably safe **fails closed** — it downgrades to a draft or a
block, never an execution.

## Method-agnostic by design

The gate treats the *authenticator* as a black box. How you establish
`authenticated` and `principal` — a passkey, a hardware token, a biometric signal
— is out of scope; the gate enforces the authorization logic around the action
regardless. This is deliberate: the input modality is disposable, the
authorization contract is not.

## Reference authenticator: pulse presence (an example principal source)

To make the "same authenticated principal" invariant concrete, here is one
reference way to produce the `authenticated`/`principal` fields — published as
prior art, method-open, so anyone can build or improve it. It uses a live
physiological signal rather than a stored secret, which suits an agent that acts
on ambient/continuous input: the authenticator answers *"is the enrolled, living
person still the one here?"* at the moment of confirmation.

Method (photoplethysmography / blood-volume pulse, from a phone camera + flash or
any wearable PPG):

1. **Capture** a short pulse window (~a minute at enrollment; a few seconds at
   verify), fingertip over the illuminated camera (transmission-mode) for a clean
   signal.
2. **Features** — bandpass to the cardiac band, detect beats, and compute (a)
   heart-rate-variability frequency-band powers (LF 0.04–0.15 Hz, HF
   0.15–0.40 Hz) from the inter-beat tachogram, and (b) a **peak-aligned** average
   pulse-wave template reduced to fiducials: systolic-peak and dicrotic-notch
   timing, dicrotic/systolic amplitude ratio, systolic-upstroke width. (Aligning
   beats before averaging matters — unaligned averaging smears the dicrotic notch,
   the most person-specific feature.)
3. **Enroll** the template on-device, encrypted, **template-only — never upload
   the raw signal.**
4. **Verify** a live window by a weighted fiducial distance mapped to a match
   score (heart rate itself is excluded from identity — it moves with arousal),
   with an exact-replay guard. `authenticated = score ≥ calibrated_threshold`.

**Honest ceiling — read this before shipping it.** Camera-based pulse matching is
a *liveness + presence + consent* signal, not vault-grade identity (published
pulse identification is ~94%, and it degrades with motion, cold hands, low
perfusion). Treat it as a second factor that proves *present-and-willing*, layered
with a strong identity factor (a passkey) for high-value actions — not as a
password replacement. And capturing physiological data invokes biometric-privacy
law (e.g. Illinois BIPA): get written consent and a retention policy first. The
gate above is method-agnostic precisely so you can swap in a stronger authenticator
(passkey, hardware token, ECG/sEMG/EEG) without changing the authorization logic.

## Run it

```bash
python3 test_intent_gate.py     # stdlib only, no dependencies — ALL CHECKS HOLD (9)
```

## Why it's here

Consciousness OS specifies an AI that *helps you think and never starts thinking
for you.* Most of this repo measures that at the level of what a model **says**.
This is the same principle enforced at the level of what an agent is allowed to
**do**: the human principal, present and authenticated, remains the sole source of
authorization for any irreversible act. Published under this repo's license as a
reference primitive — copy it, break it, harden it.

## Production status

This is not only a reference implementation. The gate pattern and an ambient
intent-detection rung are deployed in a live commercial assistant under a
staged pilot, with the biometric-privacy posture published as a public
retention policy. Deployment details, invariants, and what gets measured
next: [FIELD-NOTES.md](FIELD-NOTES.md).
