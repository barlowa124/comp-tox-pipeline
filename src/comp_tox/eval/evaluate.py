"""Evaluate on held-out scaffolds and produce the report artifacts.

TODO: implement

Metrics (test split only):
    - AUROC, AUPRC (report both; imbalance makes AUPRC the honest one)
    - Expected calibration error + reliability curve (results/calibration.png)
    - Conformal coverage at 90%: split-conformal using validation scaffolds
      as the calibration set
    - Applicability domain: Tanimoto nearest-neighbor distance of each test
      compound to the train set; report metrics conditioned on in/out of domain

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
