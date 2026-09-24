"""Compute molecular features.

TODO: implement

- Morgan fingerprints (radius 2, 2048 bits) as the primary representation —
  strong baseline for tox endpoints and interpretable via bit attribution
- Optional: RDKit 2D descriptors, MACCS keys
- Persist feature matrix aligned to compound_id; record fingerprint params
  in a sidecar JSON for provenance

Output schema (data/processed/features.parquet):
    compound_id, canonical_smiles, scaffold_id, label, fp_0..fp_2047 (or sparse)
"""

from __future__ import annotations

import sys


def build_features(in_path: str, out_path: str) -> None:
    raise NotImplementedError("TODO: implement feature build")


def main() -> None:
    in_path, out_path = sys.argv[1], sys.argv[2]
    build_features(in_path, out_path)


if __name__ == "__main__":
    main()
