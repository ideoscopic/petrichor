#!/usr/bin/env python3
"""
Score study quality using adapted Cochrane Risk of Bias 2 criteria.

Usage:
    python tools/quality_score.py --input paper_metadata.yaml
    python tools/quality_score.py --interactive

Produces a structured quality assessment for inclusion in meta-analyses.
"""

import argparse
import sys
import yaml


DOMAINS = {
    "randomization": {
        "question": "Was the allocation sequence random?",
        "low": "Computer-generated or table of random numbers",
        "some_concerns": "Method not described but stated as randomized",
        "high": "Non-random (alternation, date of birth, etc.) or not randomized",
    },
    "allocation_concealment": {
        "question": "Was allocation concealed from those enrolling participants?",
        "low": "Central allocation, sequentially numbered sealed envelopes",
        "some_concerns": "Not described",
        "high": "Open allocation schedule or no concealment",
    },
    "blinding_outcome": {
        "question": "Were outcome assessors blinded to group assignment?",
        "low": "Assessors blinded or outcomes are objective measures",
        "some_concerns": "Not described but objective outcomes used",
        "high": "Assessors not blinded and subjective outcomes",
    },
    "incomplete_data": {
        "question": "Were incomplete outcome data adequately addressed?",
        "low": "Attrition <10% and balanced, or ITT analysis used",
        "some_concerns": "Attrition 10-20%, reasons reported",
        "high": "Attrition >20% or differential attrition or no handling described",
    },
    "selective_reporting": {
        "question": "Are reports of the study free of selective outcome reporting?",
        "low": "Pre-registered protocol, all outcomes reported",
        "some_concerns": "No protocol but expected outcomes reported",
        "high": "Some expected outcomes not reported or post-hoc changes",
    },
    "measurement_validity": {
        "question": "Were validated measurement instruments used?",
        "low": "Validated, widely-used instruments (PHQ-9, GAD-7, PSS, etc.)",
        "some_concerns": "Adapted versions or less common validated tools",
        "high": "Unvalidated measures or single-item assessments",
    },
    "confounders": {
        "question": "Were important confounders controlled?",
        "low": "RCT with balanced groups, or adjusted for key confounders",
        "some_concerns": "Some confounders addressed but not all key ones",
        "high": "No adjustment for confounders in observational study",
    },
}


def score_study(assessments: dict[str, str]) -> dict:
    """
    Score a study based on domain assessments.

    Each domain is scored: 'low', 'some_concerns', or 'high' risk.
    Overall score rules:
    - Low risk: all domains low or ≤1 some_concerns
    - Some concerns: 2+ some_concerns but no high
    - High risk: any domain high
    """
    scores = {"low": 0, "some_concerns": 0, "high": 0}
    domain_results = {}

    for domain, judgment in assessments.items():
        if domain not in DOMAINS:
            continue
        judgment = judgment.lower().replace(" ", "_").replace("-", "_")
        if judgment in ("low", "low_risk"):
            judgment = "low"
        elif judgment in ("some_concerns", "some", "moderate", "unclear"):
            judgment = "some_concerns"
        elif judgment in ("high", "high_risk"):
            judgment = "high"
        else:
            judgment = "some_concerns"

        scores[judgment] += 1
        domain_results[domain] = {
            "judgment": judgment,
            "question": DOMAINS[domain]["question"],
        }

    if scores["high"] > 0:
        overall = "high"
    elif scores["some_concerns"] >= 2:
        overall = "some_concerns"
    else:
        overall = "low"

    numeric = {"low": 3, "some_concerns": 2, "high": 1}
    quality_score = round(sum(numeric.get(v["judgment"], 2) for v in domain_results.values()) / max(len(domain_results), 1), 1)

    return {
        "overall_risk_of_bias": overall,
        "quality_score": quality_score,
        "max_score": 3.0,
        "domain_count": len(domain_results),
        "domains": domain_results,
        "summary": {
            "low_risk_domains": scores["low"],
            "some_concerns_domains": scores["some_concerns"],
            "high_risk_domains": scores["high"],
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Score study quality (Cochrane RoB 2 adapted)")
    parser.add_argument("--input", help="YAML file with quality assessments")
    parser.add_argument("--output", help="Output YAML path")
    args = parser.parse_args()

    if args.input:
        with open(args.input) as f:
            data = yaml.safe_load(f)
        assessments = data.get("quality_assessment", data)
        result = score_study(assessments)

        output_path = args.output or args.input.replace(".yaml", "_quality.yaml")
        with open(output_path, "w") as f:
            yaml.dump(result, f, default_flow_style=False, sort_keys=False)

        print(f"Overall risk of bias: {result['overall_risk_of_bias']}")
        print(f"Quality score: {result['quality_score']}/{result['max_score']}")
        for domain, info in result["domains"].items():
            print(f"  {domain}: {info['judgment']}")
        print(f"Results saved to {output_path}")
    else:
        print("Quality Assessment Domains:")
        print("=" * 60)
        for domain, info in DOMAINS.items():
            print(f"\n{domain}:")
            print(f"  Q: {info['question']}")
            print(f"  Low risk: {info['low']}")
            print(f"  Some concerns: {info['some_concerns']}")
            print(f"  High risk: {info['high']}")
        print("\nProvide assessments in YAML format with domain: judgment pairs.")


if __name__ == "__main__":
    main()
