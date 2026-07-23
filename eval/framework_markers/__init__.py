"""framework_markers — the EVAL-7-MARKERS behavioral eval harness.

Self-contained, provider-agnostic harness that scores aiOS-class conversations
against the 7 behavioral markers defined in ``EVAL-7-MARKERS.md`` and
gates ``framework_core.md`` releases.

This package lives in the substrate repo (operator workspace), NOT inside the
``digital-hires`` product tree. That is a deliberate divergence from the original
sketch in ``IMPLEMENTATION-ROADMAP.md`` §2 — see ``README.md`` "Why external".

Pipeline:

    cases.py     parse golden-case scripts (production set only; never drafts/)
        │
    runner.py    replay each case against a system-under-test (baseline vs
        │        treatment) → conversation transcripts (JSONL)
        │
    judge.py     LLM-as-judge scores each transcript against the 7-marker rubric
        │        → score objects (JSONL)
        │
    aggregate.py pass/marker/disqualifier rates + trend → report.md

Everything runs offline-deterministic with ``provider=mock`` for tests and CI
smoke; real measurement uses ``provider=local`` (free Qwen, Cost Doctrine) for
the scoree and ``provider=anthropic`` (frontier) for the judge.
"""

from __future__ import annotations

import re
from pathlib import Path

__all__ = [
    "REPO_ROOT",
    "load_framework_core_payload",
    "framework_core_version",
]

# eval/framework_markers/__init__.py → repo root is two parents up.
REPO_ROOT = Path(__file__).resolve().parents[2]

_BEGIN = "### BEGIN framework_core ###"
_END = "### END framework_core ###"


def load_framework_core_payload(path: Path | None = None) -> str:
    """Return the treatment-arm payload.

    Private workspace: the ``BEGIN..END`` block from ``framework_core.md``.
    Public repo: ``framework_core.md`` is the private-register edition and is not
    published (see ``eval/PAYLOAD.lock.json`` for its hash commitment); we fall
    back to the full public ``SPEC.md`` so ``--payload-file``-less runs still
    measure a real contract. Pass ``--payload-file`` to pin any payload you want.
    """
    if path is None:
        private = REPO_ROOT / "framework_core.md"
        if private.exists():
            path = private
        else:
            public_spec = REPO_ROOT / "SPEC.md"
            if public_spec.exists():
                return public_spec.read_text(encoding="utf-8").strip()
            raise RuntimeError(
                "no payload found: neither framework_core.md nor SPEC.md exists; "
                "use --payload-file"
            )
    text = path.read_text(encoding="utf-8")
    start = text.find(_BEGIN)
    end = text.find(_END)
    if start < 0 or end < 0 or end <= start:
        raise RuntimeError(f"framework_core payload markers not found in {path}")
    return text[start + len(_BEGIN) : end].strip()


def framework_core_version(path: Path | None = None) -> str:
    """Parse ``framework_core_version`` from the §4 operator-notes block."""
    src = path or (REPO_ROOT / "framework_core.md")
    if not src.exists():
        # Public repo: version rides on the published spec (see SPEC.md header).
        spec = REPO_ROOT / "SPEC.md"
        if spec.exists():
            m = re.search(r"currently v(\d+\.\d+\.\d+)", spec.read_text(encoding="utf-8"))
            if m:
                return m.group(1)
        return "0.0.0"
    text = src.read_text(encoding="utf-8")
    marker = "`framework_core_version`:"
    idx = text.find(marker)
    if idx < 0:
        return "0.0.0"
    line = text[idx + len(marker) : text.find("\n", idx)]
    return line.strip().strip("`").strip()
