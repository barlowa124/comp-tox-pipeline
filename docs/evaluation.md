# Evaluation notes

TODO: fill in after first end-to-end run.

## Split integrity

- Confirm no `scaffold_id` appears in more than one partition.
- Report per-partition scaffold counts, not just row counts.

## Metrics

- AUROC and AUPRC on the test scaffolds, bootstrap CIs over scaffold groups.
- ECE + reliability curve.
- Split-conformal coverage at 90% (validation scaffolds as calibration set).
- Metrics conditioned on applicability-domain flag.

## Known caveats

- TODO: label noise / conflicting-call reconciliation counts
- TODO: class imbalance per split
- TODO: applicability-domain coverage vs. threshold tradeoff
