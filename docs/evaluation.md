# Evaluation notes

## Split integrity

- No `scaffold_id` appears in more than one partition (enforced by
  `eval/splits.py`; covered by `tests/test_splits.py`).
- Partition sizes: 4,872 train / 609 valid / 610 test compounds.

## Metrics (baseline run, logistic regression + Platt calibration)

- AUROC 0.644 (95% CI 0.574–0.719), AUPRC 0.244 (0.159–0.336) — CIs are
  bootstrap over scaffold groups, not rows.
- ECE 0.033; reliability curve in `results/calibration.png`.
- Split-conformal @ 90%: observed coverage 0.930, mean set size 1.04.
- Applicability domain (Tanimoto NN ≤ 0.3): 17.9% of test in-domain;
  AUROC 0.751 in-domain vs 0.619 out-domain.

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
