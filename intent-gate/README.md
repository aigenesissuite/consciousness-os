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
