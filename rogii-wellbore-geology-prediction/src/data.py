"""Paired well/typewell loading and prediction-start masks.

All loading is by well name (8-char hash). The horizontal-well CSV and the
typewell CSV are always consumed as a pair; the prediction start (PS) is the
first row whose ``TVT_input`` is NaN, and the masked suffix always runs to the
final row (verified across all 773 training wells).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

HORIZONTAL_SUFFIX = "__horizontal_well.csv"
TYPEWELL_SUFFIX = "__typewell.csv"

#: Columns present in both train and test horizontal files. Training-only
#: columns (TVT, the six surfaces) must never be required at inference.
INFERENCE_COLS = ["MD", "X", "Y", "Z", "GR", "TVT_input"]
SURFACE_COLS = ["ANCC", "ASTNU", "ASTNL", "EGFDU", "EGFDL", "BUDA"]


def default_data_dir() -> Path:
    env = os.environ.get("ROGII_DATA_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parent.parent / "data"


def list_wells(split_dir: Path) -> list[str]:
    """Sorted well names that have both a horizontal and a typewell CSV."""
    horizontal = {p.name[: -len(HORIZONTAL_SUFFIX)]
                  for p in split_dir.glob(f"*{HORIZONTAL_SUFFIX}")}
    typewell = {p.name[: -len(TYPEWELL_SUFFIX)]
                for p in split_dir.glob(f"*{TYPEWELL_SUFFIX}")}
    return sorted(horizontal & typewell)


@dataclass(frozen=True)
class WellPair:
    """One modeling example: a horizontal well and its typewell."""

    name: str
    horizontal: pd.DataFrame
    typewell: pd.DataFrame

    @property
    def prediction_start(self) -> int:
        """Index of the first masked ``TVT_input`` row."""
        mask = self.horizontal["TVT_input"].isna().to_numpy()
        if not mask.any():
            raise ValueError(f"{self.name}: no masked TVT_input rows")
        ps = int(np.argmax(mask))
        if not mask[ps:].all():
            raise ValueError(f"{self.name}: masked suffix is not contiguous")
        return ps

    @property
    def has_target(self) -> bool:
        return "TVT" in self.horizontal.columns

    def suffix_target(self) -> np.ndarray:
        """True TVT over the masked suffix (training wells only)."""
        if not self.has_target:
            raise ValueError(f"{self.name}: no TVT column (test well?)")
        return self.horizontal["TVT"].to_numpy()[self.prediction_start:]

    def submission_ids(self) -> list[str]:
        """Kaggle ids for the masked rows: ``{well}_{zero_based_row}``."""
        ps = self.prediction_start
        return [f"{self.name}_{i}" for i in range(ps, len(self.horizontal))]


def load_well(split_dir: Path, name: str, columns: list[str] | None = None) -> WellPair:
    """Load one paired example.

    ``columns`` restricts the horizontal columns (intersected with what the
    file actually has, so training-only columns are tolerated in train).
    """
    hpath = split_dir / f"{name}{HORIZONTAL_SUFFIX}"
    header = pd.read_csv(hpath, nrows=0).columns
    usecols = [c for c in (columns or header) if c in set(header)]
    horizontal = pd.read_csv(hpath, usecols=usecols)[
        [c for c in header if c in usecols]
    ]
    typewell = pd.read_csv(split_dir / f"{name}{TYPEWELL_SUFFIX}")
    return WellPair(name=name, horizontal=horizontal, typewell=typewell)
