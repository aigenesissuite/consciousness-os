"""Aggregate — turn per-case scores into pass/marker/disqualifier rates, the
treatment-vs-baseline delta, and a human-readable ``report.md``.

The report follows the template in EVAL-7-MARKERS.md §8 and adds the
baseline-vs-treatment delta block that the Phase 2 exit criterion needs
(IMPLEMENTATION-ROADMAP.md §2: "+3 to +5 markers per case on average").
"""

from __future__ import annotations

import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

from .markers import MARKER_IDS, PASS_THRESHOLD, PER_CASE_FLOOR
from .judge import Score


def _arm_summary(scores: list[Score]) -> dict:
    n = len(scores)
    if n == 0:
        return {"n": 0}
    totals = [s.total for s in scores]
    marker_pass = {
        mid: sum(int(s.scores.get(mid, {}).get("score", 0)) for s in scores)
        for mid in MARKER_IDS
    }
    return {
        "n": n,
        "pass_count": sum(1 for s in scores if s.passed),
        "avg_total": round(statistics.mean(totals), 2),
        "min_total": min(totals),
        "marker_pass": marker_pass,
        "disqualifier_hits": sum(len(s.disqualifier_violations) for s in scores),
        "below_threshold": [
            {"case": f"case-{s.case_id:02d}-{s.slug}", "total": s.total,
             "dq": s.disqualifier_violations}
            for s in scores if not s.passed
        ],
        "per_case": {s.case_id: s.total for s in scores},
    }


def aggregate(scores: list[Score]) -> dict:
    by_arm: dict[str, list[Score]] = {}
    for s in scores:
        by_arm.setdefault(s.arm, []).append(s)
    summary = {arm: _arm_summary(rows) for arm, rows in by_arm.items()}

    delta = None
    if "baseline" in summary and "treatment" in summary:
        b, t = by_arm["baseline"], by_arm["treatment"]
        b_by = {s.case_id: s.total for s in b}
        t_by = {s.case_id: s.total for s in t}
        common = sorted(set(b_by) & set(t_by))
        per_case = {cid: t_by[cid] - b_by[cid] for cid in common}
        delta = {
            "avg_total_delta": round(
                summary["treatment"]["avg_total"] - summary["baseline"]["avg_total"], 2
            ),
            "per_case_delta": per_case,
            "avg_per_case_delta": round(
                statistics.mean(per_case.values()), 2) if per_case else 0.0,
        }
    return {"by_arm": summary, "delta": delta}


def _marker_line(arm: dict) -> list[str]:
    n = arm["n"]
    return [f"- {mid}: {cnt}/{n} ({round(100 * cnt / n)}%)"
            for mid, cnt in arm["marker_pass"].items()]


def render_report(agg: dict, *, run_id: str, version: str,
                  provider: str, judge_provider: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out: list[str] = [
        f"# Framework Eval — {now} — framework_core v{version}",
        "",
        f"- Run: `{run_id}`",
        f"- Scoree provider: `{provider}` · Judge provider: `{judge_provider}`",
        "",
    ]
    by_arm = agg["by_arm"]
    for arm in ("baseline", "treatment"):
        if arm not in by_arm:
            continue
        a = by_arm[arm]
        if a["n"] == 0:
            continue
        out += [
            f"## {arm.capitalize()}",
            f"- Pass rate (>= {PASS_THRESHOLD}/7): {a['pass_count']}/{a['n']} "
            f"({round(100 * a['pass_count'] / a['n'])}%)",
            f"- Average score: {a['avg_total']} / 7   (min {a['min_total']})",
            f"- Disqualifier violations: {a['disqualifier_hits']}",
            "",
            "### Marker-level pass rate",
            *_marker_line(a),
            "",
        ]
        if a["below_threshold"]:
            out.append("### Cases below threshold")
            for row in a["below_threshold"]:
                dq = f" [DQ: {', '.join(row['dq'])}]" if row["dq"] else ""
                out.append(f"- {row['case']}: {row['total']}/7{dq}")
            out.append("")

    delta = agg.get("delta")
    if delta:
        out += [
            "## Treatment − Baseline delta (is framework_core load-bearing?)",
            f"- Average score delta: **{delta['avg_total_delta']:+} markers**",
            f"- Average per-case delta: **{delta['avg_per_case_delta']:+} markers**",
            "",
            "| Case | Δ markers |",
            "|---|---|",
            *[f"| case-{cid:02d} | {d:+} |" for cid, d in sorted(delta["per_case_delta"].items())],
            "",
        ]
        target = 3 <= delta["avg_per_case_delta"] <= 5
        out += [
            "## Phase 2 gate check",
            f"- Delta in target band (+3 to +5/case): {'PASS' if target else 'REVIEW'} "
            f"(observed {delta['avg_per_case_delta']:+})",
        ]
        if "treatment" in by_arm and by_arm["treatment"]["n"]:
            t = by_arm["treatment"]
            avg_ok = t["avg_total"] >= PASS_THRESHOLD
            floor_ok = t["min_total"] >= PER_CASE_FLOOR
            dq_ok = t["disqualifier_hits"] == 0
            out += [
                f"- Treatment avg >= {PASS_THRESHOLD}/7: {'PASS' if avg_ok else 'FAIL'} "
                f"({t['avg_total']})",
                f"- Every case >= {PER_CASE_FLOOR}/7: {'PASS' if floor_ok else 'FAIL'} "
                f"(min {t['min_total']})",
                f"- Zero disqualifiers: {'PASS' if dq_ok else 'FAIL'} "
                f"({t['disqualifier_hits']})",
            ]
        out.append("")
    out += ["---", "_Generated by eval/framework_markers/aggregate.py_"]
    return "\n".join(out)


def write_report(agg: dict, *, run_id: str, version: str, provider: str,
                 judge_provider: str, reports_dir: Path) -> Path:
    body = render_report(agg, run_id=run_id, version=version,
                         provider=provider, judge_provider=judge_provider)
    out_dir = reports_dir / version
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"{stamp}-{run_id}.md"
    path.write_text(body, encoding="utf-8")
    (out_dir / f"{stamp}-{run_id}.json").write_text(
        json.dumps(agg, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return path
