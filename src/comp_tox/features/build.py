"""Compute Morgan fingerprints and persist them as a sparse matrix.

Primary representation: Morgan (ECFP-style) fingerprints, radius 2, 2048
bits — a strong, interpretable baseline for toxicity endpoints.

Outputs:
    features.npz              csr_matrix, row-aligned with the meta parquet
    features_meta.parquet     compound_id, canonical_smiles, scaffold_id, label
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
from scipy import sparse

RADIUS = 2
FP_SIZE = 2048


def build_features(in_path: str, npz_out: str, meta_out: str) -> None:
    df = pd.read_parquet(in_path)
    gen = rdFingerprintGenerator.GetMorganGenerator(radius=RADIUS, fpSize=FP_SIZE)

    rows = []
    keep = []
    for i, smi in enumerate(df["canonical_smiles"]):
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue
        rows.append(gen.GetFingerprintAsNumPy(mol))
        keep.append(i)

    X = sparse.csr_matrix(np.asarray(rows, dtype=np.uint8))
    sparse.save_npz(npz_out, X)
    df.iloc[keep].reset_index(drop=True)[
        ["compound_id", "canonical_smiles", "scaffold_id", "label"]
    ].to_parquet(meta_out, index=False)
    print(f"features: {X.shape[0]} x {X.shape[1]} matrix -> {npz_out}")


def main() -> None:
    in_path, npz_out, meta_out = sys.argv[1], sys.argv[2], sys.argv[3]
    build_features(in_path, npz_out, meta_out)


if __name__ == "__main__":
    main()
