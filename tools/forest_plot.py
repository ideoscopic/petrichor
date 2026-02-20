#!/usr/bin/env python3
"""
Generate forest plots from meta-analysis data.

Usage:
    python tools/forest_plot.py --input pooled_input.csv --output results/forest_plot.png
    python tools/forest_plot.py --input pooled_input.csv --grouped --output results/grouped_forest.png
"""

import argparse
import csv
import sys

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("ERROR: matplotlib required. Install with: pip install matplotlib", file=sys.stderr)
    sys.exit(1)


def load_studies(path: str) -> list[dict]:
    """Load study data from CSV."""
    studies = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            g = float(row["hedges_g"])
            se = float(row["se"])
            studies.append({
                "study_id": row["study_id"].strip(),
                "hedges_g": g,
                "se": se,
                "ci_lower": g - 1.96 * se,
                "ci_upper": g + 1.96 * se,
                "weight": 1 / se**2 if se > 0 else 0,
                "year": row.get("year", "").strip(),
                "subgroup": row.get("subgroup", "").strip(),
            })
    return studies


def forest_plot(studies: list[dict], output_path: str, title: str = "Forest Plot",
                pooled: dict | None = None, grouped: bool = False) -> None:
    """Generate a forest plot."""
    fig_height = max(4, len(studies) * 0.4 + 2)
    fig, ax = plt.subplots(figsize=(10, fig_height))

    max_weight = max(s["weight"] for s in studies) if studies else 1
    y_positions = list(range(len(studies), 0, -1))

    for i, (study, y) in enumerate(zip(studies, y_positions)):
        norm_weight = study["weight"] / max_weight
        marker_size = 4 + norm_weight * 8

        ax.plot(
            [study["ci_lower"], study["ci_upper"]], [y, y],
            color="black", linewidth=1
        )
        ax.plot(
            study["hedges_g"], y,
            "s", color="steelblue", markersize=marker_size, zorder=3
        )
        label = f"{study['study_id']}"
        if study["year"]:
            label += f" ({study['year']})"
        ax.text(
            -0.05, y, label,
            ha="right", va="center", fontsize=8,
            transform=ax.get_yaxis_transform()
        )
        ci_text = f"{study['hedges_g']:.2f} [{study['ci_lower']:.2f}, {study['ci_upper']:.2f}]"
        ax.text(
            1.02, y, ci_text,
            ha="left", va="center", fontsize=8,
            transform=ax.get_yaxis_transform()
        )

    # Line of no effect
    ax.axvline(x=0, color="black", linewidth=0.5, linestyle="--")

    # Pooled estimate diamond
    if pooled:
        y_diamond = 0.3
        diamond_x = [pooled["ci_lower"], pooled["hedges_g"], pooled["ci_upper"], pooled["hedges_g"]]
        diamond_y = [y_diamond, y_diamond + 0.3, y_diamond, y_diamond - 0.3]
        ax.fill(diamond_x, diamond_y, color="red", alpha=0.7)
        ax.text(
            -0.05, y_diamond, "Pooled",
            ha="right", va="center", fontsize=8, fontweight="bold",
            transform=ax.get_yaxis_transform()
        )

    ax.set_xlabel("Hedges' g (95% CI)")
    ax.set_title(title)
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Forest plot saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate forest plots")
    parser.add_argument("--input", required=True, help="CSV file with study data")
    parser.add_argument("--output", required=True, help="Output image path")
    parser.add_argument("--title", default="Forest Plot", help="Plot title")
    parser.add_argument("--grouped", action="store_true", help="Group by subgroup column")
    args = parser.parse_args()

    studies = load_studies(args.input)
    if not studies:
        print("ERROR: No studies found in input file", file=sys.stderr)
        sys.exit(1)

    forest_plot(studies, args.output, title=args.title)


if __name__ == "__main__":
    main()
