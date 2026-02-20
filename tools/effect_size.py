#!/usr/bin/env python3
"""
Calculate standardized effect sizes from raw study statistics.

Usage:
    python tools/effect_size.py --input extracted_data.yaml
    python tools/effect_size.py --means 5.2 3.1 --sds 2.0 1.8 --ns 30 28

Outputs Hedges' g with 95% CI for each outcome.
"""

import argparse
import math
import sys
import yaml


def cohens_d(mean1: float, mean2: float, sd1: float, sd2: float, n1: int, n2: int) -> float:
    """Calculate Cohen's d (standardized mean difference)."""
    pooled_sd = math.sqrt(((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2))
    if pooled_sd == 0:
        return 0.0
    return (mean1 - mean2) / pooled_sd


def hedges_g(d: float, n1: int, n2: int) -> float:
    """Apply Hedges' correction for small-sample bias."""
    df = n1 + n2 - 2
    correction = 1 - (3 / (4 * df - 1))
    return d * correction


def hedges_g_se(g: float, n1: int, n2: int) -> float:
    """Standard error of Hedges' g."""
    return math.sqrt((n1 + n2) / (n1 * n2) + g**2 / (2 * (n1 + n2)))


def ci_95(estimate: float, se: float) -> tuple[float, float]:
    """95% confidence interval."""
    z = 1.96
    return (estimate - z * se, estimate + z * se)


def effect_from_means(pre_t: float, post_t: float, sd_t: float,
                      pre_c: float, post_c: float, sd_c: float,
                      n_t: int, n_c: int) -> dict:
    """Calculate effect size from pre-post means and SDs."""
    change_t = post_t - pre_t
    change_c = post_c - pre_c
    diff = change_t - change_c

    pooled_sd = math.sqrt((sd_t**2 + sd_c**2) / 2)
    if pooled_sd == 0:
        return {"hedges_g": 0, "ci_lower": 0, "ci_upper": 0, "se": 0}

    d = diff / pooled_sd
    g = hedges_g(d, n_t, n_c)
    se = hedges_g_se(g, n_t, n_c)
    lower, upper = ci_95(g, se)

    return {
        "cohens_d": round(d, 4),
        "hedges_g": round(g, 4),
        "se": round(se, 4),
        "ci_lower": round(lower, 4),
        "ci_upper": round(upper, 4),
        "n_treatment": n_t,
        "n_control": n_c,
    }


def effect_from_postonly(mean_t: float, mean_c: float,
                         sd_t: float, sd_c: float,
                         n_t: int, n_c: int) -> dict:
    """Calculate effect size from post-only means and SDs."""
    d = cohens_d(mean_t, mean_c, sd_t, sd_c, n_t, n_c)
    g = hedges_g(d, n_t, n_c)
    se = hedges_g_se(g, n_t, n_c)
    lower, upper = ci_95(g, se)

    return {
        "cohens_d": round(d, 4),
        "hedges_g": round(g, 4),
        "se": round(se, 4),
        "ci_lower": round(lower, 4),
        "ci_upper": round(upper, 4),
        "n_treatment": n_t,
        "n_control": n_c,
    }


def process_yaml(input_path: str) -> None:
    """Process extracted_data.yaml and calculate effect sizes for all outcomes."""
    with open(input_path) as f:
        data = yaml.safe_load(f)

    results = {
        "study_id": data.get("study_info", {}).get("doi", "unknown"),
        "outcomes": []
    }

    for outcome in data.get("outcomes", []):
        has_pre = all(
            outcome.get(k) is not None
            for k in ["pre_mean_treatment", "post_mean_treatment", "pre_mean_control", "post_mean_control"]
        )

        pop = data.get("population", {})
        n_t = pop.get("n_per_group", 30)
        n_c = pop.get("n_per_group", 30)

        if has_pre:
            es = effect_from_means(
                outcome["pre_mean_treatment"], outcome["post_mean_treatment"],
                outcome.get("pre_sd_treatment", 1),
                outcome["pre_mean_control"], outcome["post_mean_control"],
                outcome.get("pre_sd_control", 1),
                n_t, n_c
            )
        else:
            es = effect_from_postonly(
                outcome.get("post_mean_treatment", 0), outcome.get("post_mean_control", 0),
                outcome.get("post_sd_treatment", 1), outcome.get("post_sd_control", 1),
                n_t, n_c
            )

        es["measure"] = outcome.get("measure_name", "unknown")
        es["domain"] = outcome.get("outcome_domain", "unknown")
        results["outcomes"].append(es)

    output_path = input_path.replace("extracted_data", "effect_sizes")
    with open(output_path, "w") as f:
        yaml.dump(results, f, default_flow_style=False)

    print(f"Effect sizes written to {output_path}")
    for o in results["outcomes"]:
        print(f"  {o['measure']}: g = {o['hedges_g']} [{o['ci_lower']}, {o['ci_upper']}]")


def main():
    parser = argparse.ArgumentParser(description="Calculate standardized effect sizes")
    parser.add_argument("--input", help="Path to extracted_data.yaml")
    parser.add_argument("--means", nargs=2, type=float, help="Post means: treatment control")
    parser.add_argument("--sds", nargs=2, type=float, help="Post SDs: treatment control")
    parser.add_argument("--ns", nargs=2, type=int, help="Sample sizes: treatment control")
    args = parser.parse_args()

    if args.input:
        process_yaml(args.input)
    elif args.means and args.sds and args.ns:
        result = effect_from_postonly(
            args.means[0], args.means[1],
            args.sds[0], args.sds[1],
            args.ns[0], args.ns[1]
        )
        print(f"Hedges' g = {result['hedges_g']} [{result['ci_lower']}, {result['ci_upper']}]")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
