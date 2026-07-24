"""Liveness-bound intent authorization gate — an AI-safety primitive.

The problem this solves: as assistants move from "answer a question" to "take an
action" (send the email, move the money, publish the post), the dangerous failure
is no longer a bad sentence — it's an *unauthorized irreversible action*. A model
that misreads intent, or an action proposed on behalf of one person and confirmed
by another, must never execute.

This is the gate the Consciousness OS contract's "hands the final call back to
you" clause needs in code. It is deliberately small, dependency-free, and
method-agnostic about *how* a principal is authenticated (password, passkey,
hardware key, or a biometric signal) — it only enforces the authorization
invariants around the action itself.

Four invariants, all required to execute an irreversible action:

  1. IDENTITY, NOT PHRASING. Authorize by what the action *is* (a stable
     fingerprint of verb + target), never by the free text that proposed it. A
     re-worded intent can still confirm the same action; a *different* action can
     never ride an old confirmation.
  2. DISTINCT CONFIRMATION. A proposal cannot self-confirm. An irreversible action
     must be armed, then confirmed by a separate, later, deliberate event. A
     passing thought or a single utterance never fires an action.
  3. CONFIDENCE FLOOR. A low-confidence capture is a draft the human steers, never
     an executed action.
  4. SAME AUTHENTICATED PRINCIPAL. The action must be authenticated, AND the
     principal who confirms must be the same principal who armed it. A valid
     confirmation from a different or unauthenticated party can never execute the
     armed action.

Fail-closed on every unknown: anything not provably safe downgrades to a draft or
a block, never an execution.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

CONFIDENCE_FLOOR = 0.55  # below this, a capture is a draft, never an action


def fingerprint(action: dict) -> str:
    """Identity of an action: verb + target. NOT the prose that proposed it."""
    return f"{action['verb']}:{action['target']}"


@dataclass
class _Pending:
    fingerprint: str
    principal: str
    armed_at: float


class IntentAuthorizationGate:
    """A single-slot fail-closed gate. Construct one per action context.

    A `frame` is the authenticated intent envelope any input modality resolves to
    before it reaches the gate:
        {"confidence": float,        # how sure we are of the captured intent
         "authenticated": bool,      # did an authenticator verify a live principal
         "principal": str}           # who that principal is (opaque id)

    How `authenticated`/`principal` are produced is out of scope here: plug in a
    passkey check, a hardware token, or a biometric verifier. The gate treats the
    authenticator as a black box and enforces the invariants around it.
    """

    def __init__(self) -> None:
        self._pending: _Pending | None = None

    def propose(self, action: dict, frame: dict) -> dict:
        """Arm an irreversible action for confirmation. Never executes."""
        if frame.get("confidence", 0.0) < CONFIDENCE_FLOOR:
            return {"status": "draft",
                    "reason": f"confidence {frame.get('confidence', 0):.2f} < floor "
                              f"{CONFIDENCE_FLOOR} — steer it, don't run it"}
        if not frame.get("authenticated"):
            return {"status": "unauthenticated",
                    "reason": "no authenticated principal — cannot arm an action"}
        self._pending = _Pending(fingerprint(action), frame["principal"], time.monotonic())
        return {"status": "armed",
                "reason": "awaiting a distinct confirmation from the same principal"}

    def confirm(self, action: dict, frame: dict) -> dict:
        """A confirmation arrived. Executes ONLY if every invariant holds."""
        if self._pending is None:
            return {"status": "blocked", "reason": "nothing armed — no self-confirm"}
        if frame.get("confidence", 0.0) < CONFIDENCE_FLOOR:
            return {"status": "blocked", "reason": "confirmation below confidence floor"}
        if not frame.get("authenticated"):
            self._pending = None
            return {"status": "blocked", "reason": "confirmation not authenticated — fail closed"}
        if fingerprint(action) != self._pending.fingerprint:
            self._pending = None
            return {"status": "blocked", "reason": "action identity changed since arming"}
        if frame["principal"] != self._pending.principal:
            self._pending = None
            return {"status": "blocked",
                    "reason": "confirming principal differs from the arming principal — fail closed"}
        if time.monotonic() <= self._pending.armed_at:
            return {"status": "blocked", "reason": "confirmation is not a distinct later event"}
        self._pending = None
        return {"status": "executed",
                "reason": "identity-matched, authenticated, same principal, distinct confirmation"}

    @property
    def armed(self) -> bool:
        return self._pending is not None
