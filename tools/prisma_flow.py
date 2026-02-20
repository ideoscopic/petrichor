#!/usr/bin/env python3
"""
Generate PRISMA flow diagrams for systematic review reporting.

Usage:
    python tools/prisma_flow.py --input prisma_data.yaml --output results/prisma_flow.png

Input YAML format:
    identified: 523
    duplicates_removed: 87
    screened: 436
    excluded_screening: 389
    full_text_assessed: 47
    excluded_full_text:
      not_nature_intervention: 12
      no_control_group: 8
      not_mental_health_outcome: 5
      insufficient_data: 3
    included_qualitative: 19
    included_meta: 14
"""

import argparse
import sys

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("ERROR: matplotlib required. Install with: pip install matplotlib", file=sys.stderr)
    sys.exit(1)

import yaml


def draw_box(ax, x, y, text, width=2.5, height=0.6, color="lightsteelblue"):
    """Draw a labeled box on the plot."""
    rect = mpatches.FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.1", facecolor=color, edgecolor="black", linewidth=1
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha="center", va="center", fontsize=8, wrap=True)


def draw_arrow(ax, x1, y1, x2, y2):
    """Draw an arrow between boxes."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="black", lw=1))


def prisma_flow(data: dict, output_path: str) -> None:
    """Generate PRISMA 2020 flow diagram."""
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_xlim(-1, 8)
    ax.set_ylim(-1, 11)
    ax.axis("off")

    # Identification
    draw_box(ax, 3.5, 10, f"Records identified\n(n = {data['identified']})", color="lightyellow")
    draw_arrow(ax, 3.5, 9.7, 3.5, 9.1)

    draw_box(ax, 3.5, 8.8, f"Duplicates removed\n(n = {data['duplicates_removed']})", color="mistyrose")
    draw_arrow(ax, 3.5, 8.5, 3.5, 7.9)

    # Screening
    screened = data.get("screened", data["identified"] - data["duplicates_removed"])
    draw_box(ax, 3.5, 7.6, f"Records screened\n(n = {screened})", color="lightsteelblue")
    draw_arrow(ax, 4.75, 7.6, 6, 7.6)
    draw_box(ax, 6.8, 7.6, f"Excluded\n(n = {data['excluded_screening']})", color="mistyrose")
    draw_arrow(ax, 3.5, 7.3, 3.5, 6.7)

    # Eligibility
    draw_box(ax, 3.5, 6.4, f"Full-text assessed\n(n = {data['full_text_assessed']})", color="lightsteelblue")

    excluded_ft = data.get("excluded_full_text", {})
    if isinstance(excluded_ft, dict):
        total_excluded = sum(excluded_ft.values())
        reasons = "\n".join(f"  {k}: {v}" for k, v in excluded_ft.items())
        excl_text = f"Excluded (n = {total_excluded})\n{reasons}"
    else:
        excl_text = f"Excluded\n(n = {excluded_ft})"

    draw_arrow(ax, 4.75, 6.4, 6, 6.4)
    draw_box(ax, 6.8, 6.4, excl_text, width=2.8, height=1.2, color="mistyrose")
    draw_arrow(ax, 3.5, 6.1, 3.5, 5.3)

    # Included
    included_qual = data.get("included_qualitative", data.get("included", 0))
    draw_box(ax, 3.5, 5.0, f"Included in synthesis\n(n = {included_qual})", color="lightgreen")

    if "included_meta" in data:
        draw_arrow(ax, 3.5, 4.7, 3.5, 4.1)
        draw_box(ax, 3.5, 3.8, f"Included in meta-analysis\n(n = {data['included_meta']})", color="lightgreen")

    # Phase labels
    ax.text(-0.5, 10, "Identification", fontsize=10, fontweight="bold", rotation=90, va="center")
    ax.text(-0.5, 7.6, "Screening", fontsize=10, fontweight="bold", rotation=90, va="center")
    ax.text(-0.5, 6.4, "Eligibility", fontsize=10, fontweight="bold", rotation=90, va="center")
    ax.text(-0.5, 4.4, "Included", fontsize=10, fontweight="bold", rotation=90, va="center")

    ax.set_title("PRISMA 2020 Flow Diagram", fontsize=14, fontweight="bold", pad=20)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"PRISMA flow diagram saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate PRISMA flow diagrams")
    parser.add_argument("--input", required=True, help="YAML with PRISMA data")
    parser.add_argument("--output", required=True, help="Output image path")
    args = parser.parse_args()

    with open(args.input) as f:
        data = yaml.safe_load(f)

    prisma_flow(data, args.output)


if __name__ == "__main__":
    main()
