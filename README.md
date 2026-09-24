# comp-tox-pipeline

Reproducible computational toxicology pipeline predicting **Tox21 NR-ER**
(estrogen receptor agonism — an endocrine-disruption endpoint) from chemical
structure, built on public data.

**Status: working baseline.** End-to-end Snakemake DAG runs download →
standardize → features → scaffold split → train → evaluate on real Tox21 data.
Model is a deliberately simple baseline (Morgan fingerprints + logistic
regression + Platt calibration); the evaluation rigor is the point.

## Problem

New Approach Methodologies (NAMs) aim to reduce reliance on animal testing by
predicting toxicity from in-vitro assays and chemical structure. This project
builds an end-to-end, reproducible ML pipeline for a single high-value
toxicity endpoint, with the evaluation rigor that regulatory-adjacent use
demands: scaffold-split evaluation, applicability-domain analysis, and
calibrated uncertainty rather than point predictions.

## Endpoint

**Tox21 NR-ER** — nuclear-receptor estrogen agonism. Chosen because endocrine
disruption is a flagship NAMs use case (in-vitro/in-silico estrogenicity is
actively argued to displace animal uterotrophic assays), labels are fully
public, and the ~9% active rate exercises the imbalance-aware evaluation.
Alternatives considered in `docs/endpoint-selection.md`.

## Data

| Source | Use | Access |
|---|---|---|
| Tox21 (MoleculeNet mirror) | NR-ER endpoint, 6,091 labeled compounds | public CSV download |

Additional sources (ToxCast/invitrodb, PubChem, ChEMBL) documented in
`docs/datasources.md` for endpoint expansion.

## Quickstart

```bash
pip install -e .[dev]        # needs Python >= 3.10; uv recommended
snakemake --cores 4          # runs the full DAG (stubbed)
pytest tests/
snakemake -n                 # dry-run DAG check
# or: make install / test / dag / run
```

## Pipeline

`download → standardize → features → scaffold split → train → evaluate → report`

See `workflow/Snakefile`.

## Results

Scaffold-split evaluation (no scaffold shared between partitions — the honest
estimate of prospective performance on new chemotypes):

| Metric | Value |
|---|---|
| Test scaffolds / compounds | 610 compounds, 55 actives (9.0%) |
| AUROC | 0.644 (95% CI 0.574–0.719) |
| AUPRC | 0.244 (95% CI 0.159–0.336) |
| ECE | 0.033 |
| Conformal coverage @ 90% | 0.930 (mean set size 1.04) |
| In-domain fraction (Tanimoto NN ≤ 0.3) | 17.9% of test |
| AUROC in-domain / out-domain | **0.751** / 0.619 |

The in-domain/out-domain gap is the substantive finding: the model is
meaningfully better where its applicability domain holds, which is exactly
why AD flagging is reported rather than a single pooled number. Overall
AUROC 0.64 is a modest, honest scaffold-split result — random-split numbers
for this endpoint are typically ~0.8+ and misleading.

Artifacts: `results/metrics.json`, `results/calibration.png`
(reliability curve over test scaffolds).

## Limitations

- Predictions are research-grade, not regulatory-grade. No GxP, validation, or
  safety claims are made or implied.
- Baseline model only — the contribution is the evaluation scaffold, not
  state-of-the-art accuracy. Next step: RF/GP/GNN comparison on the same splits.
- Applicability domain covers only ~18% of the test set at the current
  threshold — most of chemical space is flagged, by design.
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
docs/          endpoint selection, data sources, evaluation notes
```
