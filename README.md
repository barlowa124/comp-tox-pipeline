# comp-tox-pipeline

Reproducible computational toxicology pipeline predicting **Tox21 NR-ER**
(estrogen receptor agonism, an endocrine-disruption endpoint) from chemical
structure, built on public data.

**Status: working baseline.** End-to-end Snakemake DAG runs download →
standardize → features → scaffold split → train → evaluate on real Tox21 data.
Four models compared on identical splits (logistic regression and random
forest on Morgan fingerprints, a GIN graph network, and a TensorFlow/Keras
MLP, all Platt-calibrated on validation scaffolds). The evaluation rigor
is the point.

## Problem

New Approach Methodologies (NAMs) aim to reduce reliance on animal testing by
predicting toxicity from in-vitro assays and chemical structure. This project
builds an end-to-end, reproducible ML pipeline for a single high-value
toxicity endpoint, with the evaluation rigor that regulatory-adjacent use
demands: scaffold-split evaluation, applicability-domain analysis, and
calibrated uncertainty instead of point predictions.

## Endpoint

**Tox21 NR-ER** (nuclear-receptor estrogen agonism). Chosen because endocrine
disruption is a flagship NAMs use case (in-vitro/in-silico estrogenicity is
actively argued to displace animal uterotrophic assays), labels are fully
public, and the ~13% active rate (9.0% in the held-out test partition,
per-split counts committed in `results/metrics.json`) exercises the
imbalance-aware evaluation.
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

Scaffold-split evaluation, where no scaffold is shared between partitions,
is the estimate of prospective performance on new chemotypes. 610 test compounds,
55 actives (9.0%). Bootstrap CIs over scaffold groups:

| Model | AUROC (95% CI) | AUPRC (95% CI) | ECE | Conformal @90% | In-domain AUROC | Out-domain AUROC |
|---|---|---|---|---|---|---|
| Logistic regression (fingerprints) | 0.644 (0.574–0.719) | 0.244 (0.159–0.336) | 0.033 | 0.930 | **0.751** | 0.619 |
| Random forest (fingerprints) | 0.726 (0.667–0.787) | 0.274 (0.199–0.378) | 0.044 | 0.931 | 0.701 | 0.733 |
| GIN graph network | 0.666 (see metrics.json) | 0.249 | 0.040 | 0.934 | 0.507 | 0.704 |
| Keras MLP (fingerprints) | 0.679 (0.620–0.748) | **0.314** (0.213–0.415) | 0.053 | 0.928 | 0.823 | 0.648 |

Two findings worth reporting plainly:

- **For logistic regression the applicability domain works as intended:**
  performance is materially better in-domain (0.751 vs 0.619), which is
  why AD flagging is reported instead of one pooled number.
- **For random forest and the GNN it inverts** (RF: 0.701 in / 0.733 out;
  GNN: 0.507 in / 0.704 out). The Tanimoto nearest-neighbor domain does
  not discriminate their performance. Applicability domains are
  model-dependent, not a property of the dataset alone. Any AD claim here
  is conditioned on the model it was measured with.

### Second endpoint: Tox21 NR-AR (androgen receptor agonism)

Same pipeline, same protocol, with `endpoint.assay_id` switched to `NR-AR`
(7,118 compounds after standardization; 2.4% actives in test). `results/metrics_NR-AR.json`:

| Model | AUROC | In-domain AUROC | Out-domain AUROC |
|---|---:|---:|---:|
| Logistic regression | 0.728 | 0.920 | 0.702 |
| Random forest | 0.830 | 0.908 | 0.816 |
| GIN graph network | 0.831 | 0.816 | 0.834 |
| Keras MLP | **0.344** | 0.225 | 0.368 |

On NR-AR the AD direction holds for logreg and RF but **inverts for the
GNN** (0.816 in-domain vs 0.834 out). The MLP's in/out numbers are part
of its collapse, not evidence either way. NR-AR
has 4.8% train prevalence (272 actives vs 659 on NR-ER) and the MLP
memorizes. Train AUROC reaches 1.000 within 10 epochs while validation
degrades *below chance* (training curves from the run log; per-epoch
history is not committed). Early stopping on val AUROC selects 0.641-valid,
but that checkpoint still anti-ranks the held-out scaffolds (0.344, CI
0.19–0.50). The sklearn heads and GIN degrade gracefully. The lightly-
regularized MLP does not. That is a model×endpoint
interaction, and a reminder that "ran fine on the other
endpoint" is not evidence of robustness.

Overall AUROC is modest, and it is the scaffold-split result. Random-split
numbers for this endpoint are typically ~0.8+ and misleading.

Artifacts: `results/metrics.json`, `results/calibration.png`
(reliability curve over test scaffolds).

### Framework ports and distributed training

- `src/comp_tox/models/gnn_jax.py` reimplements the GIN in JAX/Flax and
  verifies it: `parity_check` maps the trained PyTorch weights into the
  Flax parameter tree and asserts identical logits (<1e-4) on the same
  graphs. Cross-framework agreement is the evidence the port is correct,
  not a reimplementation that merely runs.
- `src/comp_tox/models/gnn_ddp.py` + `ddp_main.py` train the same GIN
  under `torch.distributed` DDP on the gloo backend, with real spawned
  worker processes, partitioned data, gradient all-reduce, rank-0
  evaluation. The code path is identical to multi-GPU (nccl). Only the
  backend and scale differ. Verified on CPU. Multi-GPU scaling is
  untested and labeled as such.
- `src/comp_tox/models/mlp_tf.py` is a TensorFlow/Keras MLP head on the
  same fingerprints and splits, wrapped in a picklable sklearn adapter so
  it flows through the identical Platt-calibration, conformal, and
  applicability-domain path. PyTorch, JAX, and TF are all exercised on
  this one task: same data, same eval, three frameworks.

## Limitations

- Predictions are research-grade, not regulatory-grade. No GxP, validation, or
  safety claims are made or implied.
- Baseline model only. The contribution is the evaluation scaffold, not
  state-of-the-art accuracy. Next step: RF/GP/GNN comparison on the same splits.
- Applicability domain covers only ~18% of the test set at the current
  threshold. Most of chemical space is flagged, by design.
- Assay labels are noisy and class-imbalanced. See `docs/evaluation.md`.

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
