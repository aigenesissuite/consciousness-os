"""CLI orchestrator for the framework-markers eval harness.

Examples
--------
List the promoted production cases:
    python -m eval.framework_markers list

Probe providers (which backends are reachable right now):
    python -m eval.framework_markers probe

Full hermetic smoke (no network, deterministic — what CI runs):
    python -m eval.framework_markers all --scoree-provider mock --judge-provider mock

Real baseline-vs-treatment measurement (free local Qwen scoree, Claude judge):
    python -m eval.framework_markers all \
        --scoree-provider local --judge-provider anthropic
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import REPO_ROOT, framework_core_version
from .aggregate import aggregate, write_report
from .cases import load_draft_cases, load_production_cases
from .judge import Score, judge_run
from .providers import probe
from .runner import RUNS_DIR, Transcript, Turn, run_cases

REPORTS_DIR = REPO_ROOT / "eval" / "framework_markers" / "reports"


def _select_cases(case_filter: str | None):
    cases = load_production_cases()
    if case_filter:
        wanted = {int(x) for x in case_filter.split(",") if x.strip()}
        cases = [c for c in cases if c.case_id in wanted]
    return cases


def _load_run_transcripts(run_id: str) -> list[Transcript]:
    base = RUNS_DIR / run_id
    transcripts: list[Transcript] = []
    for jf in sorted(base.glob("*/*.json")):
        if jf.name == "manifest.json":
            continue
        d = json.loads(jf.read_text(encoding="utf-8"))
        t = Transcript(
            case_id=d["case_id"], slug=d["slug"], arm=d["arm"],
            provider=d["provider"], model=d["model"],
            framework_core_version=d["framework_core_version"],
            system_redacted=d["system_redacted"],
            turns=[Turn(**turn) for turn in d["turns"]],
            primer_turns=[Turn(**turn) for turn in d.get("primer_turns", [])],
        )
        transcripts.append(t)
    return transcripts


def _load_scores(run_id: str) -> list[Score]:
    path = RUNS_DIR / run_id / "scores.jsonl"
    scores: list[Score] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            scores.append(Score(**json.loads(line)))
    return scores


def cmd_list(_: argparse.Namespace) -> int:
    cases = load_production_cases()
    if not cases:
        print("No PRODUCTION cases promoted yet. Drafts live in "
              "external-corpora/eval-harness/golden-cases/drafts/ and are never run.")
        return 0
    print(f"{len(cases)} production case(s):")
    for c in cases:
        print(f"  case-{c.case_id:02d}-{c.slug}  markers={','.join(c.markers_tested)} "
              f"turns={len(c.user_turns)}")
    return 0


def cmd_probe(_: argparse.Namespace) -> int:
    for p in ("mock", "local", "anthropic", "openai", "xai", "google"):
        ok, detail = probe(p)
        print(f"  {p:10s} {'OK ' if ok else 'NO '} {detail}")
    return 0


def _read_payload(args: argparse.Namespace) -> str | None:
    if getattr(args, "payload_file", None):
        return Path(args.payload_file).read_text(encoding="utf-8")
    return None


def cmd_run(args: argparse.Namespace) -> int:
    cases = _select_cases(args.cases)
    if not cases:
        print("No cases to run.", file=sys.stderr)
        return 1
    run_id, transcripts = run_cases(
        cases, provider=args.scoree_provider, model=args.scoree_model,
        run_id=args.run_id, framework_payload=_read_payload(args),
    )
    print(f"run_id={run_id}  transcripts={len(transcripts)}")
    return 0


def cmd_judge(args: argparse.Namespace) -> int:
    transcripts = _load_run_transcripts(args.run_id)
    instr = {c.case_id: c.judge_instructions for c in load_production_cases()}
    scores = judge_run(
        transcripts, instr, provider=args.judge_provider, model=args.judge_model,
        out_path=RUNS_DIR / args.run_id / "scores.jsonl",
    )
    print(f"scored {len(scores)} transcript(s) → {RUNS_DIR / args.run_id / 'scores.jsonl'}")
    return 0


def cmd_aggregate(args: argparse.Namespace) -> int:
    scores = _load_scores(args.run_id)
    agg = aggregate(scores)
    path = write_report(
        agg, run_id=args.run_id, version=framework_core_version(),
        provider=args.scoree_provider, judge_provider=args.judge_provider,
        reports_dir=REPORTS_DIR,
    )
    print(f"report → {path}")
    print(json.dumps(agg.get("delta") or {}, indent=2))
    return 0


def cmd_all(args: argparse.Namespace) -> int:
    cases = _select_cases(args.cases)
    if not cases:
        print("No production cases to run. Promote drafts first "
              "(python -m eval.framework_markers list).", file=sys.stderr)
        return 1
    run_id, transcripts = run_cases(
        cases, provider=args.scoree_provider, model=args.scoree_model,
        run_id=args.run_id, framework_payload=_read_payload(args),
    )
    instr = {c.case_id: c.judge_instructions for c in cases}
    scores = judge_run(
        transcripts, instr, provider=args.judge_provider, model=args.judge_model,
        out_path=RUNS_DIR / run_id / "scores.jsonl",
    )
    agg = aggregate(scores)
    path = write_report(
        agg, run_id=run_id, version=framework_core_version(),
        provider=args.scoree_provider, judge_provider=args.judge_provider,
        reports_dir=REPORTS_DIR,
    )
    print(f"run_id={run_id}  cases={len(cases)}  scored={len(scores)}")
    print(f"report → {path}")
    if agg.get("delta"):
        print(f"avg per-case delta (treatment - baseline): "
              f"{agg['delta']['avg_per_case_delta']:+} markers")
    return 0


def cmd_bootstrap(args: argparse.Namespace) -> int:
    """Pre-promotion baseline run against DRAFT cases.

    This is NOT the regression gate — it runs draft scaffolds so the operator can
    see whether framework_core is load-bearing before auditing/promoting cases.
    Reports land under reports/bootstrap-drafts/ and are clearly stamped.
    """
    ids = [int(x) for x in args.drafts.split(",")] if args.drafts else None
    cases = load_draft_cases(ids)
    if not cases:
        print("No draft cases matched.", file=sys.stderr)
        return 1
    print(f"BOOTSTRAP (drafts, NOT the regression gate): "
          f"{', '.join(c.name for c in cases)}")
    run_id, transcripts = run_cases(
        cases, provider=args.scoree_provider, model=args.scoree_model,
        run_id=args.run_id, max_tokens=args.max_tokens,
    )
    instr = {c.case_id: c.judge_instructions for c in cases}
    scores = judge_run(
        transcripts, instr, provider=args.judge_provider, model=args.judge_model,
        out_path=RUNS_DIR / run_id / "scores.jsonl",
    )
    agg = aggregate(scores)
    path = write_report(
        agg, run_id=f"bootstrap-{run_id}", version=framework_core_version(),
        provider=args.scoree_provider, judge_provider=args.judge_provider,
        reports_dir=REPORTS_DIR / "bootstrap-drafts",
    )
    print(f"run_id={run_id}  cases={len(cases)}  scored={len(scores)}")
    print(f"report → {path}")
    if agg.get("delta"):
        print(f"avg per-case delta (treatment - baseline): "
              f"{agg['delta']['avg_per_case_delta']:+} markers")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="eval.framework_markers",
                                description="EVAL-7-MARKERS behavioral eval harness")
    sub = p.add_subparsers(dest="command", required=True)

    def add_common(sp):
        providers = ["mock", "local", "anthropic", "openai", "xai", "google"]
        sp.add_argument("--scoree-provider", default="mock", choices=providers)
        sp.add_argument("--judge-provider", default="mock", choices=providers)
        sp.add_argument("--scoree-model", default=None)
        sp.add_argument("--judge-model", default=None)
        sp.add_argument("--cases", default=None,
                        help="comma-separated case ids, e.g. 1,2,3")
        sp.add_argument("--run-id", default=None)
        sp.add_argument("--payload-file", default=None,
                        help="path to an alternate treatment-arm payload (e.g. the "
                             "public SPEC.md). Default: the versioned framework core.")

    sub.add_parser("list").set_defaults(func=cmd_list)
    sub.add_parser("probe").set_defaults(func=cmd_probe)
    for name, fn in (("run", cmd_run), ("judge", cmd_judge),
                     ("aggregate", cmd_aggregate), ("all", cmd_all)):
        sp = sub.add_parser(name)
        add_common(sp)
        sp.set_defaults(func=fn)

    bs = sub.add_parser("bootstrap", help="pre-promotion baseline run vs DRAFT cases")
    add_common(bs)
    bs.add_argument("--drafts", default=None,
                    help="comma-separated draft case ids, e.g. 1,2,3 (default: all)")
    bs.add_argument("--max-tokens", type=int, default=600)
    bs.set_defaults(func=cmd_bootstrap)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
