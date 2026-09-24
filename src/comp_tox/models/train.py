"""Train the endpoint model on the train split; calibrate on validation.

Baseline: logistic regression on Morgan fingerprints with balanced class
weights, then Platt (sigmoid) calibration fit on the validation split via
FrozenEstimator — the calibrator never sees training or test data.

Persisted bundle: calibrated model, base model, config echo, row counts.
"""

from __future__ import annotations

import sys

import joblib
import pandas as pd
from scipy import sparse
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
from sklearn.linear_model import LogisticRegression


def train(splits_path: str, features_path: str, out_path: str) -> None:
    df = pd.read_parquet(splits_path)
    X = sparse.load_npz(features_path)
    y = df["label"].to_numpy()

    tr = (df["split"] == "train").to_numpy()
    va = (df["split"] == "valid").to_numpy()

    base = LogisticRegression(
        max_iter=2000, class_weight="balanced", solver="lbfgs"
    )
    base.fit(X[tr], y[tr])

    calibrated = CalibratedClassifierCV(FrozenEstimator(base), method="sigmoid")
    calibrated.fit(X[va], y[va])

    bundle = {
        "model": calibrated,
        "base": base,
        "train_rows": int(tr.sum()),
        "valid_rows": int(va.sum()),
        "train_actives": int(y[tr].sum()),
        "valid_actives": int(y[va].sum()),
    }
    joblib.dump(bundle, out_path)
    print(
        f"train: {tr.sum()} train / {va.sum()} valid rows "
        f"({y[tr].sum()} train actives) -> {out_path}"
    )


def main() -> None:
    splits_path, features_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    train(splits_path, features_path, out_path)


if __name__ == "__main__":
    main()
