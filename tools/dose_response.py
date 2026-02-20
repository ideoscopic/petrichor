#!/usr/bin/env python3
"""
Fit dose-response models for nature exposure and health outcomes.

Usage:
    python tools/dose_response.py --input dose_response_data.csv --models linear,log,spline,threshold

Input CSV format:
    study_id, dose_value, effect_size, se, n, population_type

Fits candidate models and selects best fit by AIC.
"""

import argparse
import csv
import math
import sys

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("ERROR: matplotlib and numpy required. pip install matplotlib numpy", file=sys.stderr)
    sys.exit(1)

import yaml


def load_data(path: str) -> dict:
    """Load dose-response data from CSV."""
    doses, effects, ses, ns, study_ids = [], [], [], [], []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            doses.append(float(row["dose_value"]))
            effects.append(float(row["effect_size"]))
            ses.append(float(row["se"]))
            ns.append(int(row.get("n", 30)))
            study_ids.append(row["study_id"].strip())
    return {
        "doses": np.array(doses),
        "effects": np.array(effects),
        "ses": np.array(ses),
        "ns": np.array(ns),
        "study_ids": study_ids,
    }


def weighted_least_squares(X: np.ndarray, y: np.ndarray, weights: np.ndarray) -> dict:
    """Weighted least squares regression."""
    W = np.diag(weights)
    try:
        beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
    except np.linalg.LinAlgError:
        return {"beta": np.zeros(X.shape[1]), "residuals": y, "aic": float("inf")}

    y_hat = X @ beta
    residuals = y - y_hat
    n = len(y)
    k = len(beta)
    ss_res = float(residuals.T @ W @ residuals)
    aic = n * math.log(ss_res / n + 1e-10) + 2 * k
    bic = n * math.log(ss_res / n + 1e-10) + k * math.log(n)
    rmse = math.sqrt(ss_res / n)

    return {
        "beta": beta,
        "y_hat": y_hat,
        "residuals": residuals,
        "aic": round(aic, 2),
        "bic": round(bic, 2),
        "rmse": round(rmse, 4),
    }


def fit_linear(doses: np.ndarray, effects: np.ndarray, weights: np.ndarray) -> dict:
    """g = beta0 + beta1 * dose"""
    X = np.column_stack([np.ones(len(doses)), doses])
    result = weighted_least_squares(X, effects, weights)
    return {
        "model": "linear",
        "formula": f"g = {result['beta'][0]:.4f} + {result['beta'][1]:.6f} * dose",
        "intercept": round(float(result["beta"][0]), 4),
        "slope": round(float(result["beta"][1]), 6),
        **{k: v for k, v in result.items() if k not in ("beta", "y_hat", "residuals")},
    }


def fit_log(doses: np.ndarray, effects: np.ndarray, weights: np.ndarray) -> dict:
    """g = beta0 + beta1 * ln(dose)"""
    log_doses = np.log(np.maximum(doses, 0.1))
    X = np.column_stack([np.ones(len(doses)), log_doses])
    result = weighted_least_squares(X, effects, weights)
    return {
        "model": "logarithmic",
        "formula": f"g = {result['beta'][0]:.4f} + {result['beta'][1]:.4f} * ln(dose)",
        "intercept": round(float(result["beta"][0]), 4),
        "slope": round(float(result["beta"][1]), 4),
        **{k: v for k, v in result.items() if k not in ("beta", "y_hat", "residuals")},
    }


def fit_threshold(doses: np.ndarray, effects: np.ndarray, weights: np.ndarray) -> dict:
    """g = beta0 if dose < tau, beta0 + beta1*(dose-tau) if dose >= tau"""
    best_aic = float("inf")
    best_result = None
    best_tau = 0

    candidate_taus = np.percentile(doses, [20, 30, 40, 50, 60, 70, 80])
    for tau in candidate_taus:
        above = doses >= tau
        if sum(above) < 2 or sum(~above) < 2:
            continue
        dose_shifted = np.maximum(doses - tau, 0)
        X = np.column_stack([np.ones(len(doses)), dose_shifted])
        result = weighted_least_squares(X, effects, weights)
        if result["aic"] < best_aic:
            best_aic = result["aic"]
            best_result = result
            best_tau = tau

    if best_result is None:
        return {"model": "threshold", "error": "Could not fit threshold model"}

    return {
        "model": "threshold",
        "formula": f"g = {best_result['beta'][0]:.4f} if dose < {best_tau:.0f}, else + {best_result['beta'][1]:.6f} * (dose - {best_tau:.0f})",
        "threshold": round(float(best_tau), 1),
        "intercept": round(float(best_result["beta"][0]), 4),
        "slope_above": round(float(best_result["beta"][1]), 6),
        **{k: v for k, v in best_result.items() if k not in ("beta", "y_hat", "residuals")},
    }


def main():
    parser = argparse.ArgumentParser(description="Fit dose-response models")
    parser.add_argument("--input", required=True, help="CSV with dose-response data")
    parser.add_argument("--models", default="linear,log,threshold", help="Comma-separated model list")
    parser.add_argument("--output", default=None, help="Output YAML path")
    parser.add_argument("--plot", default=None, help="Output plot path")
    args = parser.parse_args()

    data = load_data(args.input)
    weights = 1 / (data["ses"]**2 + 1e-10)

    model_map = {
        "linear": fit_linear,
        "log": fit_log,
        "threshold": fit_threshold,
    }

    results = []
    for model_name in args.models.split(","):
        model_name = model_name.strip()
        if model_name in model_map:
            result = model_map[model_name](data["doses"], data["effects"], weights)
            results.append(result)
            print(f"{result['model']:15s}  AIC={result.get('aic','N/A'):>8s}  RMSE={result.get('rmse','N/A')}")

    results.sort(key=lambda r: r.get("aic", float("inf")))
    best = results[0] if results else None

    output = {
        "models": results,
        "best_model": best["model"] if best else None,
        "n_data_points": len(data["doses"]),
        "dose_range": [float(data["doses"].min()), float(data["doses"].max())],
    }

    output_path = args.output or args.input.replace(".csv", "_models.yaml")
    with open(output_path, "w") as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False)

    print(f"\nBest model: {best['model'] if best else 'none'}")
    print(f"Results saved to {output_path}")

    # Generate plot if requested
    if args.plot and best:
        fig, ax = plt.subplots(figsize=(8, 6))
        marker_sizes = weights / weights.max() * 200 + 20
        ax.scatter(data["doses"], data["effects"], s=marker_sizes,
                   alpha=0.7, color="steelblue", edgecolors="black", linewidth=0.5)

        dose_range = np.linspace(max(0.1, data["doses"].min()), data["doses"].max(), 200)
        if best["model"] == "linear":
            y_pred = best["intercept"] + best["slope"] * dose_range
        elif best["model"] == "logarithmic":
            y_pred = best["intercept"] + best["slope"] * np.log(dose_range)
        elif best["model"] == "threshold":
            tau = best["threshold"]
            y_pred = np.where(dose_range < tau,
                              best["intercept"],
                              best["intercept"] + best["slope_above"] * (dose_range - tau))
        else:
            y_pred = np.zeros_like(dose_range)

        ax.plot(dose_range, y_pred, color="red", linewidth=2, label=f"Best fit: {best['model']}")
        ax.axhline(y=0.5, color="green", linestyle=":", linewidth=1, label="Clinically meaningful (g=0.5)")
        ax.axhline(y=0, color="black", linestyle="--", linewidth=0.5)
        ax.set_xlabel("Nature Dose (minutes/week)")
        ax.set_ylabel("Effect Size (Hedges' g)")
        ax.set_title("Dose-Response Relationship")
        ax.legend()
        plt.tight_layout()
        plt.savefig(args.plot, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Plot saved to {args.plot}")


if __name__ == "__main__":
    main()
