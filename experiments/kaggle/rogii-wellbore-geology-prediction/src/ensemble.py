"""Per-well model selection via a prefix playoff (rung D+).

The oracle that picks the better of two models per well is far stronger than
either model alone, and the pick is observable at inference time: replay each
candidate over the tail of the *known* prefix — anchor at the window start,
predict forward, score against the observed ``TVT_input`` — and trust the
winner with the real suffix.

Two details matter (learned from the first, failed version):

- Prefixes are short (median ~1,700 ft including the build/curve section), so
  the playoff window must adapt to the well: it is capped at half the
  *lateral* portion of the prefix, and the replay never starts in the curve,
  where constant-TVT loses for reasons that say nothing about the lateral.
- Model risk is asymmetric (the fallback's worst well is ~70 ft RMSE; a wrong
  surface can be hundreds), so the risky candidate must beat the safe one by
  a margin to be picked.

The replay hands each candidate a synthetic :class:`WellPair` whose
``TVT_input`` is masked from the playoff boundary onward, so any model
implementing the standard interface can compete without modification.
"""

from __future__ import annotations

import numpy as np

from .baselines import Model, WellLoader
from .data import WellPair

#: |dZ| per 1-ft step below which the well counts as lateral.
LATERAL_DZ_PER_FT = 0.3
#: Consecutive lateral samples required to call the landing.
LATERAL_RUN = 100


def _masked_at(pair: WellPair, ps: int) -> WellPair:
    """Copy of ``pair`` whose TVT_input is masked from row ``ps`` onward."""
    h = pair.horizontal.copy()
    h.loc[h.index[ps:], "TVT_input"] = np.nan
    return WellPair(name=pair.name, horizontal=h, typewell=pair.typewell)


def lateral_start(pair: WellPair) -> int | None:
    """Index where the well has landed: first sustained low-|dZ| run."""
    z = pair.horizontal["Z"].to_numpy()[: pair.prediction_start]
    flat = np.abs(np.diff(z)) < LATERAL_DZ_PER_FT
    run = np.convolve(flat, np.ones(LATERAL_RUN, dtype=int), mode="valid")
    hits = np.nonzero(run == LATERAL_RUN)[0]
    return int(hits[0]) if len(hits) else None


class PrefixPlayoff:
    """Choose per well between a safe and a risky model by prefix replay.

    ``candidates[0]`` is the safe fallback; later candidates must beat its
    replay RMSE by ``margin_ft`` to win the suffix.
    """

    def __init__(
        self,
        candidates: list[Model],
        eval_window_ft: float = 1000.0,
        margin_ft: float = 1.0,
    ):
        self.candidates = candidates
        self.eval_window_ft = eval_window_ft
        self.margin_ft = margin_ft
        names = "+".join(m.name.split("_")[0] for m in candidates)
        self.name = f"P_playoff_{names}_{int(eval_window_ft)}ft_m{margin_ft:g}"

    def fit(self, train_wells: list[str], loader: WellLoader) -> None:
        for m in self.candidates:
            m.fit(train_wells, loader)

    def _playoff_ps(self, pair: WellPair) -> int | None:
        """Synthetic PS for the replay, or None if the well can't host one."""
        lat = lateral_start(pair)
        if lat is None:
            return None
        ps = pair.prediction_start
        md = pair.horizontal["MD"].to_numpy()
        lateral_ft = md[ps - 1] - md[lat]
        window = min(self.eval_window_ft, 0.5 * lateral_ft)
        if window < 300:
            return None
        cut = int(np.searchsorted(md[:ps], md[ps - 1] - window))
        if cut - lat < 100:  # anchor history must itself be lateral
            return None
        return cut

    def predict(self, pair: WellPair) -> np.ndarray:
        best = self.candidates[0]
        cut = self._playoff_ps(pair)
        if cut is not None:
            ps = pair.prediction_start
            truth = pair.horizontal["TVT_input"].to_numpy()[cut:ps]
            replay = _masked_at(pair, cut)
            ok = np.isfinite(truth)
            scores = []
            for m in self.candidates:
                pred = np.asarray(m.predict(replay), dtype=float)[: ps - cut]
                scores.append(float(np.sqrt(np.mean((pred[ok] - truth[ok]) ** 2))))
            challengers = int(np.argmin(scores[1:])) + 1
            if scores[challengers] < scores[0] - self.margin_ft:
                best = self.candidates[challengers]
        return best.predict(pair)


class SoftBlendPlayoff(PrefixPlayoff):
    """Blend candidate predictions with inverse-square replay-RMSE weights.

    Hard selection pays full price for every wrong pick; with only ~50-55%
    selection accuracy, hedging is cheaper. Falls back to ``candidates[0]``
    when no replay window fits.
    """

    def __init__(self, candidates: list[Model], eval_window_ft: float = 1000.0):
        super().__init__(candidates, eval_window_ft=eval_window_ft, margin_ft=0.0)
        names = "+".join(m.name.split("_")[0] for m in candidates)
        self.name = f"S_softblend_{names}_{int(eval_window_ft)}ft"

    def predict(self, pair: WellPair) -> np.ndarray:
        cut = self._playoff_ps(pair)
        if cut is None:
            return self.candidates[0].predict(pair)
        ps = pair.prediction_start
        truth = pair.horizontal["TVT_input"].to_numpy()[cut:ps]
        replay = _masked_at(pair, cut)
        ok = np.isfinite(truth)
        scores = []
        for m in self.candidates:
            pred = np.asarray(m.predict(replay), dtype=float)[: ps - cut]
            scores.append(float(np.sqrt(np.mean((pred[ok] - truth[ok]) ** 2))))
        w = 1.0 / (np.asarray(scores) ** 2 + 1e-9)
        w /= w.sum()
        preds = np.stack([np.asarray(m.predict(pair), dtype=float)
                          for m in self.candidates])
        return (w[:, None] * preds).sum(axis=0)
