"""Promote a golden-case DRAFT into the production set.

Promotion is an OPERATOR action (Tier 0), not an agent action — the
anti-Goodhart guarantee in EVAL-7-MARKERS.md §5 and golden-cases/README.md
depends on a human auditing each case before it can gate a release. This tool
only mechanizes the file move + frontmatter cleanup once the operator has
decided; it refuses to run without an explicit operator acknowledgement, and it
refuses crisis/safety cases without a second, stronger acknowledgement (those
must be hand-validated — "crisis cases are not safely LLM-drafted",
case-04 §"Operator review priority: HIGH").

Usage:
    python -m eval.framework_markers.promote \
        --draft case-01-sole-authority-handoff --i-am-operator
    python -m eval.framework_markers.promote \
        --draft case-04-suicide-disclosure --case-id 16 \
        --i-am-operator --operator-validated-crisis
"""

from __future__ import annotations

import argparse
import re
import sys

from .cases import DRAFTS_DIR, GOLDEN_DIR, parse_case

# Slugs whose subject matter must be hand-validated by the operator before they
# can gate a release. Substring match against the draft slug.
_CRISIS_MARKERS = ("suicide", "crisis", "disembodiment", "self-harm", "spectrum-edge")


def _is_crisis(slug: str) -> bool:
    return any(m in slug for m in _CRISIS_MARKERS)


def _strip_draft_frontmatter(text: str) -> str:
    out = []
    for line in text.splitlines():
        if re.match(r"^\s*(draft_status|draft_author)\s*:", line):
            continue
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def _retarget(text: str, case_id: int | None, slug: str | None) -> str:
    if case_id is not None:
        text = re.sub(r"(?m)^case_id:\s*.*$", f"case_id: {case_id}", text, count=1)
        text = re.sub(r"(?m)^(#\s*Case)\s+\d+", rf"\g<1> {case_id:02d}", text, count=1)
    if slug is not None:
        text = re.sub(r"(?m)^slug:\s*.*$", f"slug: {slug}", text, count=1)
    return text


def promote(draft_name: str, *, case_id: int | None, slug: str | None,
            keep_draft: bool) -> str:
    draft_path = DRAFTS_DIR / (draft_name if draft_name.endswith(".md") else f"{draft_name}.md")
    if not draft_path.exists():
        raise FileNotFoundError(f"draft not found: {draft_path}")
    case = parse_case(draft_path)
    final_id = case_id if case_id is not None else case.case_id
    final_slug = slug if slug is not None else case.slug

    text = draft_path.read_text(encoding="utf-8")
    text = _retarget(_strip_draft_frontmatter(text), case_id, slug)

    dest = GOLDEN_DIR / f"case-{final_id:02d}-{final_slug}.md"
    if dest.exists():
        raise FileExistsError(f"production case already exists: {dest}")
    dest.write_text(text, encoding="utf-8")
    if not keep_draft:
        draft_path.unlink()
    return str(dest)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="eval.framework_markers.promote")
    p.add_argument("--draft", required=True, help="draft filename (with or without .md)")
    p.add_argument("--case-id", type=int, default=None, help="renumber on promotion")
    p.add_argument("--slug", default=None, help="rename slug on promotion")
    p.add_argument("--keep-draft", action="store_true",
                   help="copy instead of git-mv (leave the draft in place)")
    p.add_argument("--i-am-operator", action="store_true",
                   help="required: confirms a human operator authorized this promotion")
    p.add_argument("--operator-validated-crisis", action="store_true",
                   help="required for crisis/safety cases: confirms the operator "
                        "hand-validated the crisis routing")
    args = p.parse_args(argv)

    if not args.i_am_operator:
        print("REFUSED: promotion is an operator action. Re-run with --i-am-operator "
              "only after a human has audited this draft.", file=sys.stderr)
        return 2

    slug_for_check = args.slug or args.draft.removesuffix(".md").split("-", 2)[-1]
    if _is_crisis(slug_for_check) and not args.operator_validated_crisis:
        print(f"REFUSED: '{slug_for_check}' looks like a crisis/safety case. Crisis "
              "cases are not safely LLM-drafted and must be hand-validated. Re-run "
              "with --operator-validated-crisis once you have verified the crisis "
              "routing (e.g. 988 / 741741) by hand.", file=sys.stderr)
        return 3

    try:
        dest = promote(args.draft, case_id=args.case_id, slug=args.slug,
                       keep_draft=args.keep_draft)
    except (FileNotFoundError, FileExistsError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 4
    print(f"promoted → {dest}")
    if not args.keep_draft:
        print("draft removed (use `git status` to review the move).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
