# Evaluation notes

## Split integrity

- No `scaffold_id` appears in more than one partition (enforced by
  `eval/splits.py`; covered by `tests/test_splits.py`).
- Partition sizes: 4,872 train / 609 valid / 610 test compounds.

## Metrics (baseline run, Morgan fingerprints + Platt calibration)

- Logistic regression: AUROC 0.644 (0.574–0.719), AUPRC 0.244 (0.159–0.336),
  ECE 0.033, conformal @90% coverage 0.930.
- Random forest: AUROC 0.726 (0.667–0.787), AUPRC 0.274 (0.199–0.378),
  ECE 0.044, conformal coverage 0.931.
- CIs are bootstrap over scaffold groups, not rows. Reliability curve in
  `results/calibration.png` (primary model).
- Applicability domain (Tanimoto NN ≤ 0.3): 17.9% of test in-domain.
  Logreg: AUROC 0.751 in / 0.619 out. **RF inverts: 0.701 in / 0.733 out** —
  the AD flag is model-dependent and cannot be reported model-agnostically.

## Known caveats

- The model is a deliberately simple baseline; the evaluation scaffold is
  the contribution. AUROC 0.64 is honest, not impressive.
- Test prevalence (9.0%) is higher than train due to scaffold-group sorting;
  prevalence differences across partitions complicate AUPRC interpretation.
- Conformal coverage is marginal, not conditional — per-scaffold coverage
  varies; see AD-conditioned coverage in `results/metrics.json`.
- The AD threshold (0.3) is configured, not yet calibrated on validation
  scaffolds — see TODO below.

## Next

- Calibrate `ad_threshold` on validation NN-distance vs error curve.
- Compare RF / gradient boosting / GNN on identical splits.
- Second endpoint (hERG or a ToxCast AC50) to check generality.
