"""Invariants for the liveness-bound intent authorization gate.
Run: python3 test_intent_gate.py   (stdlib only; exits non-zero on any failure)
"""

from __future__ import annotations

import sys
import time

from intent_gate import IntentAuthorizationGate

failures = 0


def check(name: str, cond: bool) -> None:
    global failures
    print(("PASS  " if cond else "FAIL  ") + name)
    if not cond:
        failures += 1


ACTION = {"verb": "send_email", "target": "client"}
AUTH = {"confidence": 0.9, "authenticated": True, "principal": "alice"}


def fresh():
    return IntentAuthorizationGate()


# a low-confidence capture is a draft, never an action
check("low confidence -> draft",
      fresh().propose(ACTION, {"confidence": 0.3, "authenticated": True, "principal": "alice"})["status"] == "draft")

# an unauthenticated capture cannot even arm
check("unauthenticated -> cannot arm",
      fresh().propose(ACTION, {"confidence": 0.9, "authenticated": False, "principal": "alice"})["status"] == "unauthenticated")

# nothing armed -> a confirmation cannot self-authorize
check("no self-confirm", fresh().confirm(ACTION, AUTH)["status"] == "blocked")

# the full valid path executes (armed, then a distinct later confirm, same principal)
g = fresh()
check("propose arms", g.propose(ACTION, AUTH)["status"] == "armed")
time.sleep(0.001)  # ensure the confirm is a strictly-later event
check("valid path executes", g.confirm(ACTION, AUTH)["status"] == "executed")

# a different principal cannot confirm an action someone else armed
g = fresh()
g.propose(ACTION, AUTH)
check("different principal blocked",
      g.confirm(ACTION, {"confidence": 0.9, "authenticated": True, "principal": "mallory"})["status"] == "blocked")

# losing authentication between arm and confirm fails closed
g = fresh()
g.propose(ACTION, AUTH)
check("de-authenticated confirm blocked",
      g.confirm(ACTION, {"confidence": 0.9, "authenticated": False, "principal": "alice"})["status"] == "blocked")

# a different action cannot ride an existing arming
g = fresh()
g.propose(ACTION, AUTH)
check("action identity change blocked",
      g.confirm({"verb": "delete", "target": "client"}, AUTH)["status"] == "blocked")

# a re-worded but identical action still confirms (identity, not phrasing)
g = fresh()
g.propose({"verb": "send_email", "target": "client"}, AUTH)
time.sleep(0.001)
check("same action identity still confirms",
      g.confirm({"verb": "send_email", "target": "client"}, AUTH)["status"] == "executed")

print()
print("ALL CHECKS HOLD" if failures == 0 else f"{failures} FAILURES")
sys.exit(0 if failures == 0 else 1)
