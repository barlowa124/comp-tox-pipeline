"""Applicability domain estimation.

TODO: implement

- Distance metric: Tanimoto distance on Morgan fingerprints to the nearest
  training-set neighbor
- Threshold: calibrate on validation scaffolds (see config.evaluation.ad_threshold);
  a compound is in-domain iff NN distance <= threshold
- Diagnostics: report metric degradation as a function of distance, and the
  fraction of test compounds flagged out-of-domain
"""

from __future__ import annotations

import numpy as np


def in_domain(nn_distances: np.ndarray, threshold: float) -> np.ndarray:
    """Boolean mask: True where a compound is inside the applicability domain."""
    raise NotImplementedError("TODO: implement applicability-domain check")
