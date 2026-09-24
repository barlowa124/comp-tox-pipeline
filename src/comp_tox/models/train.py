"""Train the endpoint models on the train split; calibrate on validation.

Baselines: logistic regression and random forest on Morgan fingerprints,
each Platt-calibrated on the validation split via FrozenEstimator — the
calibrator never sees training or test data. All configured models are
trained on identical scaffold splits so comparison is apples-to-apples.

Persisted bundle: {name: calibrated model} dict + metadata.
"""

from __future__ import annotations

import sys

import joblib
import pandas as pd
import yaml
from scipy import sparse
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.frozen import FrozenEstimator
from sklearn.linear_model import LogisticRegression

MODEL_REGISTRY = {
    "logistic_regression": lambda seed: LogisticRegression(
        max_iter=2000, class_weight="balanced", solver="lbfgs"
    ),
    "random_forest": lambda seed: RandomForestClassifier(
        n_estimators=400, class_weight="balanced", n_jobs=-1, random_state=seed
    ),
}


def train(splits_path: str, features_path: str, out_path: str) -> None:
    with open("config/config.yaml") as f:
        cfg = yaml.safe_load(f)
    seed = cfg["split"]["seed"]
    names = [cfg["model"]["type"]] + cfg["model"].get("compare", [])

    df = pd.read_parquet(splits_path)
    X = sparse.load_npz(features_path)
    y = df["label"].to_numpy()

    tr = (df["split"] == "train").to_numpy()
    va = (df["split"] == "valid").to_numpy()

    models = {}
    for name in dict.fromkeys(names):
        base = MODEL_REGISTRY[name](seed)
        base.fit(X[tr], y[tr])
        calibrated = CalibratedClassifierCV(
            FrozenEstimator(base), method="sigmoid"
        )
        calibrated.fit(X[va], y[va])
        models[name] = calibrated
        print(f"trained {name}")

    bundle = {
        "models": models,
        "primary": cfg["model"]["type"],
        "train_rows": int(tr.sum()),
        "valid_rows": int(va.sum()),
        "train_actives": int(y[tr].sum()),
        "valid_actives": int(y[va].sum()),
    }
    joblib.dump(bundle, out_path)
    print(
        f"train: {tr.sum()} train / {va.sum()} valid rows "
        f"({y[tr].sum()} train actives), models={list(models)} -> {out_path}"
    )


def main() -> None:
    splits_path, features_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    train(splits_path, features_path, out_path)


if __name__ == "__main__":
    main()
