from __future__ import annotations

import unittest

from parallax.crypto.costs import FillCostObservation, MeasuredCostModel


class MeasuredCostModelTests(unittest.TestCase):
    def test_separates_fee_spread_and_slippage_from_a_fill(self) -> None:
        fill = FillCostObservation(
            side="buy",
            fill_price=100.06,
            best_bid=99.95,
            best_ask=100.05,
            fee_quote=0.10,
            notional_quote=1_000.0,
        )

        self.assertAlmostEqual(fill.fee_bps, 1.0)
        self.assertAlmostEqual(fill.half_spread_bps, 5.0)
        self.assertAlmostEqual(fill.slippage_bps, 1.0)
        self.assertAlmostEqual(fill.total_cost_bps, 7.0)

    def test_round_trip_model_and_fifteen_bps_floor(self) -> None:
        fill = FillCostObservation(
            side="sell",
            fill_price=99.94,
            best_bid=99.95,
            best_ask=100.05,
            fee_quote=0.10,
            notional_quote=1_000.0,
        )
        model = MeasuredCostModel.from_fills([fill])

        self.assertAlmostEqual(model.round_trip_bps, 14.0)
        self.assertFalse(model.is_viable(14.9))
        self.assertTrue(model.is_viable(16.0))


if __name__ == "__main__":
    unittest.main()
