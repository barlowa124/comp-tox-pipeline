"""Evaluate on held-out scaffolds and produce the report artifacts.

Orchestrates the eval submodules (test split only):
    - eval.calibration: ECE + reliability curve -> results/calibration.png
    - eval.conformal: split-conformal coverage at 90%, calibration on
      validation scaffolds
    - eval.applicability: Tanimoto NN distance to train set; report metrics
      conditioned on in/out of domain
    - AUROC, AUPRC (report both; imbalance makes AUPRC the honest one)

All metrics get bootstrap CIs over scaffold groups (not over rows).

Outputs:
    results/metrics.json
    results/calibration.png
"""

from __future__ import annotations

import argparse


def evaluate(model_path: str, data_path: str, metrics_out: str, cal_out: str) -> None:
    raise NotImplementedError("TODO: implement evaluation")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model")
    parser.add_argument("data")
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--calibration", required=True)
    args = parser.parse_args()
    evaluate(args.model, args.data, args.metrics, args.calibration)


if __name__ == "__main__":
    main()
