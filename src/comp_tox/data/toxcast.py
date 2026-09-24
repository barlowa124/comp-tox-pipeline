"""Download endpoint data from public tox data sources.

TODO: implement download of the configured endpoint's assay data.

ToxCast/Tox21: EPA publishes invitrodb bulk releases; pull the assay table for
the configured assay_id, join to compound identifiers (DSSTox ID / CASRN /
SMILES). Alternative: Tox21 aggregated activity calls from PubChem.

Output schema (data/raw/assay.parquet):
    compound_id, smiles, label (or ac50), assay_id, source

Cache everything under data/raw/; never re-download inside a pipeline run.
"""

from __future__ import annotations

import argparse


def download(endpoint: str, assay_id: str | None, out_path: str) -> None:
    raise NotImplementedError("TODO: implement endpoint download")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    raise NotImplementedError("TODO: wire download() to config")


if __name__ == "__main__":
    main()
