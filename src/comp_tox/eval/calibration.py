"""Probability calibration measurement and plotting.

TODO: implement

- Expected calibration error over M equal-width bins (M=15 typical)
- Reliability curve -> results/calibration.png
- Report calibration pre/post any recalibration fit; recalibration must be
  fit on validation scaffolds only, never on test
"""

from __future__ import annotations

import numpy as np


def expected_calibration_error(
    y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 15
) -> float:
    """ECE: mean absolute gap between bin accuracy and bin confidence."""
    raise NotImplementedError("TODO: implement ECE")
