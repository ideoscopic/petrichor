#!/usr/bin/env python3
"""
Random-effects meta-analysis using DerSimonian-Laird method.

Usage:
    python tools/meta_pool.py --input pooled_input.csv --method dsl

Input CSV format:
    study_id, hedges_g, se, n_treatment, n_control, year, quality_score

Outputs pooled effect size, heterogeneity stats, and prediction interval.
"""

import argparse
import csv
import math
import sys
import yaml


def dersimonian_laird(effects: list[float], variances: list[float]) -> dict:
    """
    DerSimonian-Laird random-effects meta-analysis.

    Returns pooled effect, CI, heterogeneity statistics.
    """
    k = len(effects)
    if k < 2:
        return {"error": "Need at least 2 studies"}

    # Fixed-effect weights
    weights_fe = [1 / v for v in variances]
    sum_w = sum(weights_fe)

    # Fixed-effect pooled estimate
    theta_fe = sum(w * e for w, e in zip(weights_fe, effects)) / sum_w

    # Q statistic (heterogeneity test)
    q = sum(w * (e - theta_fe)**2 for w, e in zip(weights_fe, effects))

    # Degrees of freedom
    df = k - 1

    # Between-study variance (tau²)
    c = sum_w - sum(w**2 for w in weights_fe) / sum_w
    tau2 = max(0, (q - df) / c)

    # Random-effects weights
    weights_re = [1 / (v + tau2) for v in variances]
    sum_w_re = sum(weights_re)

    # Random-effects pooled estimate
    theta_re = sum(w * e for w, e in zip(weights_re, effects)) / sum_w_re
    se_re = math.sqrt(1 / sum_w_re)

    # 95% CI
    ci_lower = theta_re - 1.96 * se_re
    ci_upper = theta_re + 1.96 * se_re

    # Z-test
    z = theta_re / se_re
    p_value = 2 * (1 - _norm_cdf(abs(z)))

    # I² statistic
    i2 = max(0, (q - df) / q * 100) if q > 0 else 0

    # H² statistic
    h2 = q / df if df > 0 else 1

    # 95% prediction interval
    if k >= 3:
        # t-distribution critical value approximation for df=k-2
        t_crit = 2.0 if k > 10 else _t_critical(k - 2)
        pi_se = math.sqrt(se_re**2 + tau2)
        pi_lower = theta_re - t_crit * pi_se
        pi_upper = theta_re + t_crit * pi_se
    else:
        pi_lower = None
        pi_upper = None

    return {
        "pooled_effect": round(theta_re, 4),
        "se": round(se_re, 4),
        "ci_lower": round(ci_lower, 4),
        "ci_upper": round(ci_upper, 4),
        "z_value": round(z, 4),
        "p_value": round(p_value, 6),
        "k_studies": k,
        "tau2": round(tau2, 4),
        "q_statistic": round(q, 4),
        "q_df": df,
        "q_p_value": round(1 - _chi2_cdf(q, df), 6) if df > 0 else 1.0,
        "i2": round(i2, 1),
        "h2": round(h2, 4),
        "prediction_interval_lower": round(pi_lower, 4) if pi_lower is not None else None,
        "prediction_interval_upper": round(pi_upper, 4) if pi_upper is not None else None,
    }


def leave_one_out(effects: list[float], variances: list[float], study_ids: list[str]) -> list[dict]:
    """Leave-one-out sensitivity analysis."""
    results = []
    for i in range(len(effects)):
        remaining_e = effects[:i] + effects[i+1:]
        remaining_v = variances[:i] + variances[i+1:]
        pooled = dersimonian_laird(remaining_e, remaining_v)
        results.append({
            "excluded": study_ids[i],
            "pooled_effect": pooled["pooled_effect"],
            "ci_lower": pooled["ci_lower"],
            "ci_upper": pooled["ci_upper"],
            "i2": pooled["i2"],
        })
    return results


def _norm_cdf(x: float) -> float:
    """Approximate standard normal CDF."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _chi2_cdf(x: float, df: int) -> float:
    """Very rough chi-square CDF approximation (Wilson-Hilferty)."""
    if df <= 0 or x <= 0:
        return 0.0
    z = ((x / df)**(1/3) - (1 - 2/(9*df))) / math.sqrt(2/(9*df))
    return _norm_cdf(z)


def _t_critical(df: int) -> float:
    """Approximate t critical value for 95% CI."""
    if df <= 1:
        return 12.71
    elif df <= 2:
        return 4.30
    elif df <= 5:
        return 2.57
    elif df <= 10:
        return 2.23
    else:
        return 2.0


def main():
    parser = argparse.ArgumentParser(description="Random-effects meta-analysis")
    parser.add_argument("--input", required=True, help="CSV file with study data")
    parser.add_argument("--method", default="dsl", choices=["dsl"], help="Meta-analysis method")
    parser.add_argument("--output", default=None, help="Output YAML path")
    args = parser.parse_args()

    studies = []
    with open(args.input) as f:
        reader = csv.DictReader(f)
        for row in reader:
            studies.append({
                "study_id": row["study_id"].strip(),
                "hedges_g": float(row["hedges_g"]),
                "se": float(row["se"]),
                "n_treatment": int(row.get("n_treatment", 30)),
                "n_control": int(row.get("n_control", 30)),
                "year": row.get("year", "").strip(),
                "quality_score": row.get("quality_score", "").strip(),
            })

    if len(studies) < 2:
        print("ERROR: Need at least 2 studies for meta-analysis", file=sys.stderr)
        sys.exit(1)

    effects = [s["hedges_g"] for s in studies]
    variances = [s["se"]**2 for s in studies]
    study_ids = [s["study_id"] for s in studies]

    result = dersimonian_laird(effects, variances)
    result["method"] = "DerSimonian-Laird random-effects"
    result["studies"] = studies

    loo = leave_one_out(effects, variances, study_ids)
    result["leave_one_out"] = loo

    output_path = args.output or args.input.replace(".csv", "_meta_results.yaml")
    with open(output_path, "w") as f:
        yaml.dump(result, f, default_flow_style=False, sort_keys=False)

    print(f"Meta-analysis results ({len(studies)} studies):")
    print(f"  Pooled Hedges' g = {result['pooled_effect']} [{result['ci_lower']}, {result['ci_upper']}]")
    print(f"  Z = {result['z_value']}, p = {result['p_value']}")
    print(f"  I² = {result['i2']}%, tau² = {result['tau2']}")
    if result["prediction_interval_lower"] is not None:
        print(f"  95% PI = [{result['prediction_interval_lower']}, {result['prediction_interval_upper']}]")
    print(f"  Results saved to {output_path}")


if __name__ == "__main__":
    main()
