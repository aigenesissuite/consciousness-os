#!/usr/bin/env python3
"""Aggregate the open-model (Qwen3.6-27B) gate run, regenerate the five-model
scoreboard chart, and print the values needed by the wave-2 follow-up emails."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUN = Path(__file__).parent / "framework_markers" / "runs" / "gate-v1.1pub-qwen-20260723"
ASSETS = Path(__file__).parent.parent / "assets"

# Published v1.1.0 scoreboard pass counts (SCOREBOARD.md).
FRONTIER = {
    "Claude\nSonnet 4.6": (6, 18),
    "GPT-5.5": (1, 16),
    "Grok 4.5": (3, 15),
    "Gemini\n3.1 Pro": (0, 8),
}


def arm_stats(records: list[dict]) -> dict:
    n = len(records)
    return {
        "n": n,
        "pass": sum(1 for r in records if r["passed"]),
        "avg": round(sum(r["total"] for r in records) / n, 2) if n else 0.0,
        "dq": sum(1 for r in records if r.get("disqualifier_violations")),
    }


def main() -> None:
    records = [json.loads(l) for l in (RUN / "scores.jsonl").read_text().splitlines() if l.strip()]
    base = arm_stats([r for r in records if r["arm"] == "baseline"])
    treat = arm_stats([r for r in records if r["arm"] == "treatment"])
    delta = round(treat["avg"] - base["avg"], 2)

    print(f"QWEN baseline : pass {base['pass']}/{base['n']}  avg {base['avg']}/7  DQ {base['dq']}")
    print(f"QWEN treatment: pass {treat['pass']}/{treat['n']}  avg {treat['avg']}/7  DQ {treat['dq']}")
    print(f"QWEN delta    : +{delta} markers/conversation")

    labels = list(FRONTIER.keys()) + ["Qwen3.6-27B\n(open weights)"]
    baselines = [v[0] for v in FRONTIER.values()] + [base["pass"]]
    treatments = [v[1] for v in FRONTIER.values()] + [treat["pass"]]

    x = range(len(labels))
    w = 0.38
    fig, ax = plt.subplots(figsize=(9.6, 5.2), dpi=200)
    ax.bar([i - w / 2 for i in x], baselines, w, label="Baseline (no contract)", color="#c0392b")
    ax.bar([i + w / 2 for i in x], treatments, w, label="With injected contract", color="#27ae60")
    for i, (b, t) in enumerate(zip(baselines, treatments)):
        ax.text(i - w / 2, b + 0.3, str(b), ha="center", fontsize=10, fontweight="bold")
        ax.text(i + w / 2, t + 0.3, str(t), ha="center", fontsize=10, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel("Cases passed (of 20)", fontsize=11)
    ax.set_ylim(0, 21)
    ax.set_title("Five models, one behavioral contract — none pass by default",
                 fontsize=13, fontweight="bold", pad=14)
    ax.legend(fontsize=10, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = ASSETS / "scoreboard.png"
    fig.savefig(out)
    print(f"chart -> {out}")


if __name__ == "__main__":
    main()
