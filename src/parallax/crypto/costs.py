"""Execution-cost measurements derived from actual fills and contemporaneous quotes."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite
from statistics import fmean
from typing import Literal

GROSS_EDGE_FLOOR_BPS = 15.0


@dataclass(frozen=True)
class FillCostObservation:
    side: Literal["buy", "sell"]
    fill_price: float
    best_bid: float
    best_ask: float
    fee_quote: float
    notional_quote: float

    def __post_init__(self) -> None:
        if self.side not in {"buy", "sell"}:
            raise ValueError("side must be buy or sell")
        values = (
            self.fill_price,
            self.best_bid,
            self.best_ask,
            self.fee_quote,
            self.notional_quote,
        )
        if any(not isfinite(value) for value in values):
            raise ValueError("fill-cost values must be finite")
        if min(self.fill_price, self.best_bid, self.best_ask, self.notional_quote) <= 0.0:
            raise ValueError("prices and notional must be positive")
        if self.best_ask < self.best_bid:
            raise ValueError("best ask must not be below best bid")
        if self.fee_quote < 0.0:
            raise ValueError("fee must be non-negative")

    @property
    def mid_price(self) -> float:
        return (self.best_bid + self.best_ask) / 2.0

    @property
    def fee_bps(self) -> float:
        return self.fee_quote / self.notional_quote * 10_000.0

    @property
    def half_spread_bps(self) -> float:
        return (self.best_ask - self.best_bid) / (2.0 * self.mid_price) * 10_000.0

    @property
    def slippage_bps(self) -> float:
        if self.side == "buy":
            return (self.fill_price - self.best_ask) / self.mid_price * 10_000.0
        return (self.best_bid - self.fill_price) / self.mid_price * 10_000.0

    @property
    def total_cost_bps(self) -> float:
        return self.fee_bps + self.half_spread_bps + self.slippage_bps


@dataclass(frozen=True)
class MeasuredCostModel:
    sample_size: int
    fee_bps_per_fill: float
    half_spread_bps_per_fill: float
    slippage_bps_per_fill: float

    @classmethod
    def from_fills(cls, fills: Sequence[FillCostObservation]) -> MeasuredCostModel:
        if not fills:
            raise ValueError("at least one fill is required")
        return cls(
            sample_size=len(fills),
            fee_bps_per_fill=fmean(fill.fee_bps for fill in fills),
            half_spread_bps_per_fill=fmean(fill.half_spread_bps for fill in fills),
            slippage_bps_per_fill=fmean(fill.slippage_bps for fill in fills),
        )

    @property
    def one_way_bps(self) -> float:
        return self.fee_bps_per_fill + self.half_spread_bps_per_fill + self.slippage_bps_per_fill

    @property
    def round_trip_bps(self) -> float:
        return 2.0 * self.one_way_bps

    def net_edge_bps(self, expected_gross_edge_bps: float) -> float:
        return expected_gross_edge_bps - self.round_trip_bps

    def is_viable(self, expected_gross_edge_bps: float) -> bool:
        return (
            expected_gross_edge_bps >= GROSS_EDGE_FLOOR_BPS
            and self.net_edge_bps(expected_gross_edge_bps) > 0.0
        )
