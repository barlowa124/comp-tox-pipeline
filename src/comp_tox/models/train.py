"""Train the endpoint model on the train split only.

TODO: implement

- Baseline: logistic regression on Morgan fingerprints (calibrated via
  CalibratedClassifierCV or Platt on the validation split)
- Then compare: random forest, optionally a GNN — document why/why not
- Hyperparameter selection must use validation scaffolds only, never test
- Persist model + a metadata sidecar (config hash, data hash, sklearn version)
"""

from __future__ import annotations

import sys


def train(in_path: str, out_path: str) -> None:
    raise NotImplementedError("TODO: implement training")


def main() -> None:
    in_path, out_path = sys.argv[1], sys.argv[2]
    train(in_path, out_path)


if __name__ == "__main__":
    main()
