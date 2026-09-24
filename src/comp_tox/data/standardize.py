"""Standardize chemical structures and aggregate labels.

TODO: implement with rdkit:

- Parse SMILES, drop unparseable rows (log count, never silently)
- Strip salts/solvents, neutralize, canonicalize tautomer
- Emit canonical isomeric SMILES + Bemis-Murcko scaffold ID
- Dedup by canonical SMILES; reconcile conflicting labels explicitly
  (document the reconciliation rule — e.g., any-active wins, majority, or
  drop-conflicting — and record counts)

Output schema (data/processed/compounds.parquet):
    compound_id, canonical_smiles, scaffold_id, label, label_confidence
"""

from __future__ import annotations

import sys


def standardize(in_path: str, out_path: str) -> None:
    raise NotImplementedError("TODO: implement structure standardization")


def main() -> None:
    in_path, out_path = sys.argv[1], sys.argv[2]
    standardize(in_path, out_path)


if __name__ == "__main__":
    main()
