"""Split-conformal prediction sets for the tox endpoint.

TODO: implement

- Nonconformity score: 1 - p(true class) for classification
- Quantile calibrated on *validation scaffolds* (group-level: one score per
  scaffold or per compound — document the choice; per-scaffold is the more
  conservative unit given scaffold exchangeability assumptions)
- Report marginal coverage on test scaffolds; target 90%
- Also report coverage conditioned on applicability-domain flag — coverage
  degradation out-of-domain is expected and should be quantified, not hidden
"""

from __future__ import annotations

import numpy as np


def conformal_threshold(scores: np.ndarray, alpha: float = 0.1) -> float:
    """Return the (1-alpha) conformal quantile of calibration scores."""
    raise NotImplementedError("TODO: implement conformal threshold")
