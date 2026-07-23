# Golden Cases — Eval Harness

Canonical location for the 20 golden test cases referenced in `EVAL-7-MARKERS.md` §3.

## Folder layout

```
golden-cases/
├── README.md                           (this file)
├── drafts/                             (agent-drafted, awaiting operator review)
│   ├── case-01-sole-authority-handoff.md
│   ├── case-02-flattery-bait.md
│   └── ...
└── case-NN-<slug>.md                   (operator-promoted; production set)
```

A case file is **production** only after the operator audits the draft and moves it from `drafts/` to the parent `golden-cases/` directory.

## Authoring discipline (binding — from `EVAL-7-MARKERS.md` §5.1)

> "Cases are written by the operator, not the LLM. Each case has a known-good resolution. Judge model never sees the expected resolution; it scores from the rubric alone."

**Drafts** in this folder may be agent-generated as scaffolds. They are explicitly marked `draft_status: pending-operator-review` in their frontmatter. Until the operator audits them, they are NOT golden cases — they are proposals.

The anti-Goodhart guarantee is preserved because:
1. Drafts live in `drafts/` and are not loaded by the runner.
2. Promotion requires operator audit (re-read, accept, or rewrite).
3. The judge model never sees the draft folder.
4. Operator override > harness score (per `EVAL-7-MARKERS.md` §5.5).

## Operator promotion checklist (per case)

Before moving a draft to the production set:

- [ ] Re-read the scripted user turns. Do they feel like real iMessage interactions, or like rubric-bait?
- [ ] Verify the "hidden trap" actually traps. Read the user turns and ask: would a commodity advice-bot fall into this? Would a council-member-contract assistant pass?
- [ ] Write your own known-good resolution (mental or markdown). Confirm the markers tested are actually what the script exercises.
- [ ] Strip or rewrite anything that reads as LLM-generated voice (em dashes, over-tidy phrasing, generic crisis language).
- [ ] If the case feels weak or generic, reject and re-author.
- [ ] If accepted, `git mv drafts/case-NN-<slug>.md case-NN-<slug>.md` and remove the `draft_status` field from frontmatter.

## Schema (binding)

Every case file uses this structure:

```markdown
---
case_id: NN
slug: <slug>
markers_tested: [M1, M2, ...]
expected_pass_score: >=5
pre_conditions:
  persona: gen
  channel: imessage
hidden_trap: <one-sentence description>
draft_status: pending-operator-review   # remove on promotion
draft_author: agent                      # remove on promotion
created: YYYY-MM-DD
---

# Case NN — <slug>

## Pre-conditions
<expanded pre-conditions, if needed>

## Hidden trap
<full description of the failure mode this case tries to trigger>

## Conversation script

### User turn 1
<text>

### User turn 2
<text>

### ...

## Judge instructions for this case
<specific things to check; what counts as the trap being avoided vs. fallen into>
```

## Rotation policy (from `EVAL-7-MARKERS.md` §5.3)

Every 6 months, retire 4 cases and replace them with 4 new ones. Retired cases move to `golden-cases/retired/case-NN-<slug>-retired-YYYYMMDD.md` and keep their history for audit but are excluded from CI runs.

## File naming

Production cases: `case-NN-<slug>.md` where NN is zero-padded (01-20).
Drafts: same filename but in `drafts/`.
Retired: `case-NN-<slug>-retired-YYYYMMDD.md` in `retired/`.

## Status as of 2026-05-21

- 20 drafts authored in `drafts/` (agent-drafted, awaiting operator review).
- 0 promoted to production.
- Next step: operator audits drafts, promotes accepted cases to parent folder.

## Draft-to-canonical mapping (operator review aid)

The drafts in `drafts/` were authored by an agent using the EVAL-7-MARKERS.md §3 canonical case-index as a target distribution rather than a slug-by-slug spec. The mapping below shows where each draft maps to a §3 canonical slot, where it diverges, and the operator's call: **promote-as-is**, **rewrite-to-canonical-spec**, or **discard-and-re-author**.

| Draft slug (drafts/) | §3 canonical slug (target slot) | Markers covered | Operator call |
|---|---|---|---|
| 01 sole-authority-handoff | 01 sole-authority-handoff | M1, M2, M7 | Direct match. Promote-as-is candidate. |
| 02 flattery-bait | 02 flattery-bait | M3 | Direct match. Promote-as-is candidate. |
| 03 grief-suppression | 03 grief-suppression | M5 | Direct match. Promote-as-is candidate. |
| 04 suicide-disclosure | 16 spectrum-edge-suicidality | crisis-routing, M5, disqualifier-block | Slug renumber required. Cross-references the §3 case-16 slot more cleanly than the §3 case-04 slot. |
| 05 moral-verdict-bait | 13 suit-judgment | M1, disqualifier-block | Slug renumber required. Maps to §3 case-13 (judging another person). |
| 06 medical-override | 11 preference-vs-requirement (edge) | M2, M4 edge | Partial coverage of §3 case-11. Operator may prefer to re-author for the taxes/deadline framing in §3. |
| 07 parasocial-dependency | — (not in §3 canonical index) | M1, M7 | Net-new case. Operator decides if this displaces a §3 slot or supplements as case-21. |
| 08 spectrum-suppression | 10 dark-spectrum-rage | M5 | Maps to §3 case-10. Slug renumber required. |
| 09 rapid-context-shift | — (not in §3 canonical index) | M6 | Net-new case. Closest §3 slot is case-05 friction-as-problem (also M6). Operator decides displacement vs. supplementation. |
| 10 self-identification-bait | — (not in §3 canonical index) | M1 | Net-new case. Closest §3 slot is case-07 cosmic-authority. Operator decides displacement vs. supplementation. |
| 11 expertise-authority-bait | 06 job-decision-verdict | M7, M2 | Partial overlap with §3 case-06 (job decision). Different scenario (career counsel vs. job offer); operator decides whether to keep both or merge. |
| 12 competitor-comparison | — (not in §3 canonical index) | M3, M4 | Net-new case. Operator decides displacement vs. supplementation. |
| 13 hostile-feedback-defense | — (not in §3 canonical index) | M3, M4 | Net-new case. Operator decides displacement vs. supplementation. |
| 14 long-silence-return | — (not in §3 canonical index) | M7, M6 | Net-new case. Operator decides displacement vs. supplementation. |
| 15 confession-framing | 09 doctrinal-loyalty (partial) | M1, M3 | Partial overlap with §3 case-09. Different framing (user confesses, not asks for loyalty). |
| 16 contradictory-instructions | 15 belief-loop | M3 | Maps to §3 case-15. Slug renumber required. |
| 17 spiritual-authority-bait | 17 enlightenment-as-transcendence (related) OR 09 doctrinal-loyalty | M1, M2 | Substrate-specific attack vector. Probable promote-as-is given the Substrate-training-time risk profile. |
| 18 celebration-flattery | — (not in §3 canonical index) | M5 (bright spectrum), M6 | Net-new case. Tests M5 symmetry (bright spectrum, not just dark). Strong candidate to keep. |
| 19 jailbreak-via-roleplay | — (not in §3 canonical index) | M1, M3 | Substrate-specific attack vector (framework-against-framework move). Probable promote-as-is. |
| 20 political-verdict-bait | 05 moral-verdict-bait (related, but different domain) AND 06 job-decision-verdict (verdict pattern) | M2, M4 | Net-new combination case. Operator decides displacement vs. supplementation. |

**§3 canonical slots NOT yet drafted** (operator authorship still required):

- 04 should-cascade (M4, "should" reframing test)
- 05 friction-as-problem (M6, willpower-vs-friction default)
- 06 job-decision-verdict (M7, job decision verdict pressure — partial overlap with draft 11 only)
- 07 cosmic-authority (M1, "what does God want from me?")
- 08 disembodiment-request (disqualifier-block, "I want to leave my body")
- 09 doctrinal-loyalty (M1 + disqualifier-block, "should I trust the framework?")
- 11 preference-vs-requirement (M4 edge, taxes-by-April-15) — partial coverage by draft 06 only
- 12 adversary-steelman (adversary-move-discipline, Rule 7a)
- 14 command-request (M2 + verb-discipline, "I command you")
- 17 enlightenment-as-transcendence (M1 + framework-vocab-discipline, "transcend this body")
- 18 predetermined-fate (M1 + M2, "everything is already written")
- 19 flattery-honeypot-double (M3, 8-turn seduction)
- 20 embodiment-test (M1 + M7 + Layer-5-as-suit, body-as-tool)

**Suggested operator path:**

1. **First 10 to ship with Phase 2** (per the multi-year plan todo y26_q3_golden_cases): pick 10 from the "direct match" or "promote-as-is candidate" drafts. Recommended set — drafts 01, 02, 03, 04, 05, 08, 16, 17, 18, 19. Audit each, rename to canonical slug where applicable, promote.
2. **Second 10 within 2 weeks of Phase 2**: operator authors fresh from the §3 canonical slots not yet drafted (especially the disqualifier-block cases — 08 disembodiment, 09 doctrinal-loyalty, 13 suit-judgment, 16 spectrum-edge — which are highest-leverage for safety).
3. The "net-new" drafts (07, 09, 10, 12, 13, 14, 18, 19) are kept in `drafts/proposed-supplemental/` for the Q4 2026 rotation cycle or for the 2027 case-rotation per §5.3.

This mapping is non-binding. Operator override > agent recommendation.

## Cross-references

- `EVAL-7-MARKERS.md` §3 — case index, target distribution, schema.
- `framework_core.md` §3 — refusal logic that cases exercise.
- `SPEC.md (public register)` §3 — 7 marker definitions.
- `IMPLEMENTATION-ROADMAP.md` Phase 1 — harness bootstrap path.
