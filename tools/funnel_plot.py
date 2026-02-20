#!/usr/bin/env python3
"""
Generate funnel plots for publication bias assessment.

Usage:
    python tools/funnel_plot.py --input pooled_input.csv --output results/funnel_plot.png

A symmetric funnel suggests no publication bias. Asymmetry suggests
small studies with non-significant results may be missing.
"""

import argparse
import csv
import math
import sys

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    print("ERROR: matplotlib required. Install with: pip install matplotlib", file=sys.stderr)
    sys.exit(1)


def load_studies(path: str) -> list[dict]:
    """Load study data from CSV."""
    studies = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            studies.append({
                "study_id": row["study_id"].strip(),
                "hedges_g": float(row["hedges_g"]),
                "se": float(row["se"]),
            })
    return studies


def eggers_test(effects: list[float], ses: list[float]) -> dict:
    """
    Egger's regression test for funnel plot asymmetry.
    Regresses standardized effect (g/se) on precision (1/se).
    Significant intercept suggests asymmetry.
    """
    n = len(effects)
    if n < 10:
        return {"note": "Egger's test requires ≥10 studies", "performed": False}

    precisions = [1 / se for se in ses]
    standardized = [g / se for g, se in zip(effects, ses)]

    mean_x = sum(precisions) / n
    mean_y = sum(standardized) / n

    ss_xx = sum((x - mean_x)**2 for x in precisions)
    ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(precisions, standardized))

    if ss_xx == 0:
        return {"note": "Cannot compute — zero variance in precision", "performed": False}

    slope = ss_xy / ss_xx
    intercept = mean_y - slope * mean_x

    residuals = [y - (intercept + slope * x) for x, y in zip(precisions, standardized)]
    ss_res = sum(r**2 for r in residuals)
    mse = ss_res / (n - 2)
    se_intercept = math.sqrt(mse * (1/n + mean_x**2 / ss_xx))

    t_stat = intercept / se_intercept if se_intercept > 0 else 0

    return {
        "performed": True,
        "intercept": round(intercept, 4),
        "se_intercept": round(se_intercept, 4),
        "t_statistic": round(t_stat, 4),
        "significant": abs(t_stat) > 2.0,
        "interpretation": "Asymmetry detected (possible publication bias)" if abs(t_stat) > 2.0
                         else "No significant asymmetry detected",
    }


def funnel_plot(studies: list[dict], output_path: str) -> None:
    """Generate a funnel plot."""
    fig, ax = plt.subplots(figsize=(8, 6))

    effects = [s["hedges_g"] for s in studies]
    ses = [s["se"] for s in studies]

    ax.scatter(effects, ses, color="steelblue", s=50, zorder=3, edgecolors="black", linewidth=0.5)

    # Pooled effect line (simple weighted mean)
    weights = [1/se**2 for se in ses]
    pooled = sum(w * e for w, e in zip(weights, effects)) / sum(weights)
    ax.axvline(x=pooled, color="red", linewidth=1, linestyle="--", label=f"Pooled g={pooled:.2f}")

    # Pseudo 95% CI funnel
    max_se = max(ses) * 1.1
    se_range = [i * max_se / 100 for i in range(1, 101)]
    ci_lower = [pooled - 1.96 * se for se in se_range]
    ci_upper = [pooled + 1.96 * se for se in se_range]
    ax.plot(ci_lower, se_range, color="gray", linewidth=0.8, linestyle=":")
    ax.plot(ci_upper, se_range, color="gray", linewidth=0.8, linestyle=":")
    ax.fill_betweenx(se_range, ci_lower, ci_upper, alpha=0.05, color="gray")

    ax.set_xlabel("Hedges' g")
    ax.set_ylabel("Standard Error")
    ax.set_title("Funnel Plot")
    ax.invert_yaxis()
    ax.legend(fontsize=9)
    ax.axvline(x=0, color="black", linewidth=0.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Funnel plot saved to {output_path}")

    # Run Egger's test
    result = eggers_test(effects, ses)
    print(f"Egger's test: {result.get('interpretation', result.get('note', ''))}")


def main():
    parser = argparse.ArgumentParser(description="Generate funnel plots")
    parser.add_argument("--input", required=True, help="CSV with study data")
    parser.add_argument("--output", required=True, help="Output image path")
    args = parser.parse_args()

    studies = load_studies(args.input)
    if len(studies) < 3:
        print("ERROR: Need at least 3 studies for funnel plot", file=sys.stderr)
        sys.exit(1)

    funnel_plot(studies, args.output)


if __name__ == "__main__":
    main()
