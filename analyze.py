#!/usr/bin/env python3
"""Analyze benchmark results and produce a Markdown report."""

import json
import sys


def load_results(path: str = "results.json") -> dict:
    with open(path) as f:
        return json.load(f)


def format_cost_cents(cost_usd: float) -> str:
    """Format cost in cents to 4 significant figures."""
    cents = cost_usd * 100
    if cents == 0:
        return "$0.0000"
    # Use 4 significant figures
    return f"${cents:.4g}c"


def format_cost_dollars(cost_usd: float) -> str:
    """Format cost in dollars with appropriate precision."""
    if cost_usd < 0.0001:
        return f"${cost_usd:.6f}"
    return f"${cost_usd:.4f}"


def analyze(results: dict) -> str:
    """Generate full Markdown analysis from results."""
    tasks = results["tasks"]
    model_keys = ["haiku-4.5", "sonnet-4.6", "opus-4.6"]
    is_dry_run = results["metadata"].get("dry_run", False)

    lines = []
    lines.append("# Benchmark Results\n")

    if is_dry_run:
        lines.append("> **Note:** These results are from a dry run (no actual API calls).\n")

    # Results table
    lines.append("## Cost per Task (USD)\n")
    lines.append("| Task | Haiku 4.5 | Sonnet 4.6 | Opus 4.6 | Best Value |")
    lines.append("|------|-----------|------------|----------|------------|")

    totals = {m: 0.0 for m in model_keys}
    best_picks = {}

    for task_name, task_results in tasks.items():
        costs = {}
        for model_key in model_keys:
            cost = task_results[model_key]["cost_usd"]
            costs[model_key] = cost
            totals[model_key] += cost

        best_model = min(costs, key=costs.get) if not is_dry_run else "—"
        best_picks[task_name] = best_model

        row_costs = " | ".join(format_cost_dollars(costs[m]) for m in model_keys)
        best_label = best_model if isinstance(best_model, str) and best_model == "—" else best_model.replace("-", " ").title()
        lines.append(f"| {task_name} | {row_costs} | {best_label} |")

    # Totals row
    total_row = " | ".join(format_cost_dollars(totals[m]) for m in model_keys)
    lines.append(f"| **TOTAL** | {total_row} | — |")
    lines.append("")

    # Token usage table
    lines.append("## Token Usage per Task\n")
    lines.append("| Task | Model | Input Tokens | Output Tokens |")
    lines.append("|------|-------|-------------|---------------|")

    for task_name, task_results in tasks.items():
        for model_key in model_keys:
            r = task_results[model_key]
            lines.append(
                f"| {task_name} | {model_key} | {r['input_tokens']} | {r['output_tokens']} |"
            )
    lines.append("")

    # Summary insights
    lines.append("## Key Insights\n")

    if not is_dry_run:
        # Cost ratios
        if totals["haiku-4.5"] > 0:
            sonnet_ratio = totals["sonnet-4.6"] / totals["haiku-4.5"]
            opus_ratio = totals["opus-4.6"] / totals["haiku-4.5"]
            lines.append(
                f"- **Sonnet 4.6 costs {sonnet_ratio:.1f}x** more than Haiku 4.5 across all tasks"
            )
            lines.append(
                f"- **Opus 4.6 costs {opus_ratio:.1f}x** more than Haiku 4.5 across all tasks"
            )

        # Cheapest task
        cheapest_task = min(tasks, key=lambda t: tasks[t]["haiku-4.5"]["cost_usd"])
        cheapest_cost = tasks[cheapest_task]["haiku-4.5"]["cost_usd"]
        lines.append(
            f"- **Cheapest task on Haiku:** {cheapest_task} at {format_cost_dollars(cheapest_cost)}"
        )

        # Most expensive task
        most_expensive = max(tasks, key=lambda t: tasks[t]["opus-4.6"]["cost_usd"])
        expensive_cost = tasks[most_expensive]["opus-4.6"]["cost_usd"]
        lines.append(
            f"- **Most expensive task on Opus:** {most_expensive} at {format_cost_dollars(expensive_cost)}"
        )

        # Haiku total
        lines.append(
            f"- **Total cost for all 10 tasks on Haiku:** {format_cost_dollars(totals['haiku-4.5'])}"
        )
    else:
        lines.append("- _No insights available for dry run._")

    lines.append("")
    return "\n".join(lines)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "results.json"
    results = load_results(path)
    report = analyze(results)

    print(report)

    output_path = "RESULTS.md"
    with open(output_path, "w") as f:
        f.write(report)
    print(f"\nReport saved to {output_path}")


if __name__ == "__main__":
    main()
