from __future__ import annotations

import unittest

from parallax.crypto import run_backtest


class RunBacktestTests(unittest.TestCase):
    def test_target_position_is_lagged_one_interval(self) -> None:
        result = run_backtest([0.10, 0.20, -0.10], [1.0, 0.0, -1.0])

        self.assertEqual(result.executed_positions, (0.0, 1.0, 0.0))
        self.assertEqual(result.strategy_equity, (1.0, 1.0, 1.2, 1.2))
        self.assertAlmostEqual(result.benchmark_equity[-1], 1.188)

    def test_cost_is_charged_on_position_change(self) -> None:
        result = run_backtest(
            [0.0, 0.0, 0.0],
            [1.0, -1.0, 0.0],
            cost_bps_per_turnover=10.0,
        )

        self.assertEqual(result.turnover, (0.0, 1.0, 2.0))
        self.assertAlmostEqual(result.strategy_equity[-1], 0.997002)

    def test_reports_drawdown_and_excess_return(self) -> None:
        result = run_backtest([0.10, -0.20, 0.10], [1.0, 1.0, 1.0])

        self.assertAlmostEqual(result.strategy_max_drawdown, 0.20)
        self.assertAlmostEqual(result.benchmark_max_drawdown, 0.20)
        self.assertAlmostEqual(
            result.excess_return,
            result.strategy_total_return - result.benchmark_total_return,
        )

    def test_rejects_misaligned_inputs(self) -> None:
        with self.assertRaisesRegex(ValueError, "equal length"):
            run_backtest([0.01], [1.0, 1.0])

    def test_rejects_unbounded_positions(self) -> None:
        with self.assertRaisesRegex(ValueError, "within"):
            run_backtest([0.01], [1.1])

    def test_beating_market_requires_return_and_risk_adjusted_outperformance(self) -> None:
        losing_to_buy_and_hold = run_backtest([0.10, 0.10], [1.0, 1.0])
        avoiding_a_crash = run_backtest([0.10, -0.50, 0.10, 0.10], [0.0, 0.0, 1.0, 1.0])

        self.assertFalse(losing_to_buy_and_hold.beats_market)
        self.assertTrue(avoiding_a_crash.beats_market)


if __name__ == "__main__":
    unittest.main()
