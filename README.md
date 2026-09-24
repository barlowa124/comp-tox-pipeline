# comp-tox-pipeline

Reproducible computational toxicology pipeline for predicting **[TODO: endpoint]**
from chemical structure, built on public NAMs-relevant data (EPA ToxCast/Tox21,
PubChem, ChEMBL).

**Status: scaffold.** Pipeline stages are stubbed; see `TODO` markers throughout
`src/`. The scaffold split (`comp_tox.eval.splits`) is implemented and tested.

## Problem

New Approach Methodologies (NAMs) aim to reduce reliance on animal testing by
predicting toxicity from in-vitro assays and chemical structure. This project
builds an end-to-end, reproducible ML pipeline for a single high-value
toxicity endpoint, with the evaluation rigor that regulatory-adjacent use
demands: scaffold-split evaluation, applicability-domain analysis, and
calibrated uncertainty rather than point predictions.

## Endpoint

TODO: finalize. Candidates:

- Hepatotoxicity / DILI (high decision relevance, harder label noise)
- hERG inhibition (cardiotox; well-studied, good public data)
- Tox21 estrogen/androgen receptor agonism (clean NAMs narrative)
- ToxCast AC50 for a selected assay (largest label budget)

See `docs/endpoint-selection.md`.

## Data

| Source | Use | Access |
|---|---|---|
| EPA ToxCast/Tox21 (invitrodb) | assay endpoints, labels | public bulk download |
| PubChem | compound structures, bioassay | PUG-REST |
| ChEMBL | supplementary bioactivity | public download |

## Quickstart

```bash
pip install -e .[dev]
snakemake --cores 4          # runs the full DAG (stubbed)
pytest tests/
snakemake -n               # dry-run DAG check
```

## Pipeline

`download → standardize → features → scaffold split → train → evaluate → report`

See `workflow/Snakefile`.

## Results

TODO: headline table — scaffold-split AUROC/AUPRC, expected calibration error,
conformal coverage at 90%, applicability-domain coverage vs. Tanimoto threshold.

## Limitations

- Predictions are research-grade, not regulatory-grade. No GxP, validation, or
  safety claims are made or implied.
- Applicability domain is limited to chemistry resembling the training set;
  out-of-domain inputs get flagged, not trusted.
- Assay labels are noisy and class-imbalanced; see `docs/evaluation.md`.

## Repo layout

```
config/        endpoint + model + evaluation config
workflow/      Snakemake DAG
src/comp_tox/
  data/        download + standardization
  features/    fingerprints + descriptors
  models/      training
  eval/        scaffold split, calibration, conformal, applicability domain
tests/
docs/
```
