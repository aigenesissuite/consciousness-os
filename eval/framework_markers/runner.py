"""Runner — replays golden cases against a system-under-test.

Two arms per case:

- ``baseline``   generic-assistant system prompt only. Represents the commodity
                 advice-bot the framework is supposed to beat.
- ``treatment``  the SAME generic prompt with the ``framework_core`` payload
                 prepended. The payload is the only independent variable, so the
                 marker delta (treatment − baseline) is attributable to it. The
                 Phase 2 exit criterion is a +3 to +5 marker delta.

Output: one transcript JSON per (case, arm) under
``runs/<run_id>/<arm>/<case-name>.json``, plus a ``manifest.json``. The system
prompt is stored redacted-by-flag (the judge must not see it — anti-Goodhart).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import REPO_ROOT, framework_core_version, load_framework_core_payload
from .cases import Case
from .providers import Completion, chat

ARM_BASELINE = "baseline"
ARM_TREATMENT = "treatment"
ARMS = (ARM_BASELINE, ARM_TREATMENT)

RUNS_DIR = REPO_ROOT / "eval" / "framework_markers" / "runs"

_BASELINE_SYSTEM = (
    "You are a helpful, friendly AI assistant chatting with someone over text "
    "message. Keep replies concise and conversational."
)


def build_systems(framework_payload: str | None = None) -> dict[str, str]:
    """Return ``{arm: system_prompt}``. Treatment = payload + baseline."""
    payload = framework_payload if framework_payload is not None else load_framework_core_payload()
    return {
        ARM_BASELINE: _BASELINE_SYSTEM,
        ARM_TREATMENT: f"{payload}\n\n{_BASELINE_SYSTEM}",
    }


@dataclass
class Turn:
    turn: int
    role: str
    content: str


@dataclass
class Transcript:
    case_id: int
    slug: str
    arm: str
    provider: str
    model: str
    framework_core_version: str
    system_redacted: bool
    turns: list[Turn] = field(default_factory=list)
    # Harness v2: stipulated prior context replayed as history before the
    # scored turns (turn=0). Judges see it labeled as unscored prior context.
    primer_turns: list[Turn] = field(default_factory=list)

    def to_json(self) -> dict:
        d = asdict(self)
        return d


def new_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def run_case(
    case: Case,
    arm: str,
    system: str,
    *,
    provider: str = "mock",
    model: str | None = None,
    max_tokens: int = 700,
    temperature: float = 0.4,
) -> Transcript:
    """Replay a single case under one arm; returns the full transcript."""
    transcript = Transcript(
        case_id=case.case_id,
        slug=case.slug,
        arm=arm,
        provider=provider,
        model=model or provider,
        framework_core_version=framework_core_version(),
        system_redacted=True,
    )
    history: list[dict[str, str]] = []
    for role, content in case.primer_turns:
        history.append({"role": role, "content": content})
        transcript.primer_turns.append(Turn(turn=0, role=role, content=content))
    for i, user_text in enumerate(case.user_turns, start=1):
        history.append({"role": "user", "content": user_text})
        transcript.turns.append(Turn(turn=i, role="user", content=user_text))
        completion: Completion = chat(
            system,
            history,
            provider=provider,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        transcript.model = completion.model
        history.append({"role": "assistant", "content": completion.text})
        transcript.turns.append(Turn(turn=i, role="assistant", content=completion.text))
    return transcript


def run_cases(
    cases: list[Case],
    *,
    arms: tuple[str, ...] = ARMS,
    provider: str = "mock",
    model: str | None = None,
    run_id: str | None = None,
    runs_dir: Path | None = None,
    framework_payload: str | None = None,
    max_tokens: int = 700,
    temperature: float = 0.4,
) -> tuple[str, list[Transcript]]:
    """Run every (case, arm); write transcripts + manifest; return them."""
    run_id = run_id or new_run_id()
    base = (runs_dir or RUNS_DIR) / run_id
    systems = build_systems(framework_payload)
    transcripts: list[Transcript] = []
    for arm in arms:
        arm_dir = base / arm
        arm_dir.mkdir(parents=True, exist_ok=True)
        for case in cases:
            t = run_case(
                case,
                arm,
                systems[arm],
                provider=provider,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            (arm_dir / f"{case.name}.json").write_text(
                json.dumps(t.to_json(), indent=2, ensure_ascii=False), encoding="utf-8"
            )
            transcripts.append(t)

    manifest = {
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "provider": provider,
        "model": model or provider,
        "arms": list(arms),
        "framework_core_version": framework_core_version(),
        "cases": [c.name for c in cases],
        "count": len(transcripts),
    }
    base.mkdir(parents=True, exist_ok=True)
    (base / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return run_id, transcripts
