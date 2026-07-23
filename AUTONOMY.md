# The Autonomy Boundary

This project is partially operated by an AI agent, and some of the email you may
have received about it was composed and sent by that agent. Since the project's
subject is behavioral contracts for AI systems, the operating boundary for our
own agent should be written down with the same precision we demand of the spec.
This page is that document.

## What the agent does autonomously

- Engineering on the eval harness: provider adapters, bug fixes, test suites,
  run orchestration. (Example: the thinking-mode fix in
  `eval/framework_markers/providers.py` was diagnosed, patched, tested, and
  committed by the agent.)
- Running published measurements end to end: scoree runs, judging, aggregation,
  report generation.
- Drafting and sending project correspondence from the program inbox
  (`gen@ai-genesis.ai`), with the founder named, blind-copied on every send,
  and set as the reply path. The agent logs every send.
- Research simulations used to improve the project's own communication (e.g.
  persona-simulated reviews of our README and of our outreach email — findings
  from those simulations are why this page exists).

## What requires the human principal

- Any change to the spec's normative content (SPEC.md) or the eval rubric.
- Publishing results: numbers ship only after verification against raw run
  artifacts, and release-gate verdicts follow the preregistered protocol
  rather than anyone's judgment, human or agent.
- Posting under the founder's identity (forums, social accounts, personal
  correspondence with named individuals he knows).
- Anything irreversible outside the repo: spending, legal commitments,
  account creation, data deletion.

## The mechanism, not the vibe

The same fail-closed pattern measured by this repo's eval governs the agent's
operation: proposed actions are separated from executed actions, execution of
irreversible steps requires a distinct confirmation from the principal, and
unknown cases default to "don't." We hold ourselves to the contract we publish,
and this page is versioned in git so any drift is public.

*If you received email from this project and want a human: reply. Replies go
directly to the founder, not to the agent.*
