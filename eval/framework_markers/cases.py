"""Golden-case parser.

Loads the PRODUCTION golden-case set only. The ``drafts/`` and ``retired/``
folders are NEVER loaded by the runner — this is the anti-Goodhart guarantee
(EVAL-7-MARKERS.md §5, golden-cases/README.md): the judge and runner only ever
see operator-promoted cases.

Case files follow the binding schema in
``external-corpora/eval-harness/golden-cases/README.md`` §"Schema":

    ---
    case_id: NN
    slug: <slug>
    markers_tested: [M1, M2, ...]
    expected_pass_score: ">=5"
    pre_conditions:
      persona: gen
      channel: imessage
    hidden_trap: <one sentence>
    created: YYYY-MM-DD
    ---
    # Case NN — <slug>
    ## Hidden trap ...
    ## Conversation script
    ### User turn 1
    <text>
    ## Judge instructions for this case
    <text>
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import REPO_ROOT

GOLDEN_DIR = REPO_ROOT / "external-corpora" / "eval-harness" / "golden-cases"
DRAFTS_DIR = GOLDEN_DIR / "drafts"

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_TURN_RE = re.compile(r"^#{2,3}\s+User turn\s+(\d+)\s*$", re.IGNORECASE)
_JUDGE_HDR_RE = re.compile(r"^#{2,3}\s+Judge instructions", re.IGNORECASE)
# Harness v2: cases that stipulate prior context declare it as replayable turns
# under "## Precondition primer" (### Prior user / ### Prior assistant). The
# runner injects them as conversation history BEFORE the scored script — fixes
# the case-14 class of bug where honest "I don't have memory" was scored as a
# lie because the stipulated context was never actually provided.
_PRIMER_TURN_RE = re.compile(r"^#{2,3}\s+Prior (user|assistant)\s*$", re.IGNORECASE)


@dataclass(frozen=True)
class Case:
    case_id: int
    slug: str
    markers_tested: tuple[str, ...]
    expected_pass_score: str
    persona: str
    channel: str
    hidden_trap: str
    user_turns: tuple[str, ...]
    judge_instructions: str
    source_path: Path
    is_draft: bool = False
    extra: dict[str, str] = field(default_factory=dict)
    # ((role, content), ...) injected as history before the scored turns.
    primer_turns: tuple[tuple[str, str], ...] = ()

    @property
    def name(self) -> str:
        return f"case-{self.case_id:02d}-{self.slug}"


def _parse_frontmatter(block: str) -> dict[str, object]:
    """Tiny YAML-lite parser: scalars, ``[a, b]`` lists, one nested block."""
    data: dict[str, object] = {}
    nested_key: str | None = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw[0] in (" ", "\t")
        line = raw.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if indented and nested_key:
            nested = data.setdefault(nested_key, {})
            if isinstance(nested, dict):
                nested[key] = value
            continue
        if value == "":
            nested_key = key
            data[key] = {}
            continue
        nested_key = None
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = tuple(v.strip() for v in inner.split(",") if v.strip())
        else:
            data[key] = value
    return data


def parse_case(path: Path) -> Case:
    text = path.read_text(encoding="utf-8")
    fm_match = _FRONTMATTER_RE.match(text)
    if not fm_match:
        raise ValueError(f"{path.name}: missing YAML frontmatter")
    fm = _parse_frontmatter(fm_match.group(1))
    body = text[fm_match.end():]

    pre = fm.get("pre_conditions", {})
    pre = pre if isinstance(pre, dict) else {}

    user_turns: list[str] = []
    primer_turns: list[tuple[str, str]] = []
    judge_lines: list[str] = []
    buf: list[str] | None = None
    buf_kind: str | None = None  # "turn" | primer role ("user"/"assistant")
    in_judge = False

    def _flush() -> None:
        nonlocal buf, buf_kind
        if buf is None:
            return
        text = "\n".join(buf).strip()
        if text:
            if buf_kind == "turn":
                user_turns.append(text)
            else:
                primer_turns.append((buf_kind or "user", text))
        buf, buf_kind = None, None

    for line in body.splitlines():
        if _JUDGE_HDR_RE.match(line):
            _flush()
            in_judge = True
            continue
        if in_judge:
            judge_lines.append(line)
            continue
        primer_match = _PRIMER_TURN_RE.match(line)
        if primer_match:
            _flush()
            buf, buf_kind = [], primer_match.group(1).lower()
            continue
        if _TURN_RE.match(line):
            _flush()
            buf, buf_kind = [], "turn"
            continue
        if buf is not None:
            buf.append(line)
    _flush()

    markers = fm.get("markers_tested", ())
    markers = markers if isinstance(markers, tuple) else ()

    known = {
        "case_id", "slug", "markers_tested", "expected_pass_score",
        "pre_conditions", "hidden_trap", "created", "draft_status", "draft_author",
    }
    extra = {k: str(v) for k, v in fm.items() if k not in known and not isinstance(v, dict)}

    return Case(
        case_id=int(str(fm.get("case_id", "0")).strip() or "0"),
        slug=str(fm.get("slug", path.stem)),
        markers_tested=markers,
        expected_pass_score=str(fm.get("expected_pass_score", f">={5}")),
        persona=str(pre.get("persona", "gen")),
        channel=str(pre.get("channel", "imessage")),
        hidden_trap=str(fm.get("hidden_trap", "")),
        user_turns=tuple(t for t in user_turns if t),
        judge_instructions="\n".join(judge_lines).strip(),
        source_path=path,
        is_draft="draft_status" in fm,
        extra=extra,
        primer_turns=tuple(primer_turns),
    )


def load_production_cases(golden_dir: Path | None = None) -> list[Case]:
    """Promoted cases only — top-level ``case-*.md``, never ``drafts/``/``retired/``."""
    root = golden_dir or GOLDEN_DIR
    cases = [
        parse_case(p)
        for p in sorted(root.glob("case-*.md"))
        if p.parent == root
    ]
    return sorted(cases, key=lambda c: c.case_id)


def load_draft_cases(ids: list[int] | None = None, drafts_dir: Path | None = None) -> list[Case]:
    """Load DRAFT cases for a bootstrap/baseline run only.

    Drafts are NOT the regression gate (anti-Goodhart: ``load_production_cases``
    never returns them). This loader exists solely so the operator can run a
    pre-promotion baseline measurement against draft scaffolds. ``ids`` filters
    by ``case_id`` (the number in the filename), e.g. ``[1, 2, 3]``.
    """
    root = drafts_dir or DRAFTS_DIR
    cases = sorted((parse_case(p) for p in root.glob("case-*.md")),
                   key=lambda c: c.case_id)
    if ids is not None:
        wanted = set(ids)
        cases = [c for c in cases if c.case_id in wanted]
    return cases
