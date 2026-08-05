"""Small, dependency-free evaluation primitives for the initial research loop."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class BacktestResult:
    """Summary of a strategy and its passive benchmark over the same return intervals."""

    strategy_equity: tuple[float, ...]
    benchmark_equity: tuple[float, ...]
    executed_positions: tuple[float, ...]
    turnover: tuple[float, ...]
    strategy_total_return: float
    benchmark_total_return: float
    excess_return: float
    strategy_max_drawdown: float
    benchmark_max_drawdown: float
    strategy_return_over_drawdown: float
    benchmark_return_over_drawdown: float
    beats_market: bool


def run_backtest(
    market_returns: Sequence[float],
    target_positions: Sequence[float],
    *,
    cost_bps_per_turnover: float = 0.0,
    initial_equity: float = 1.0,
) -> BacktestResult:
    """Evaluate target positions with a mandatory one-observation execution lag.

    ``market_returns[i]`` is the simple return during interval ``i``. A target position observed
    at the end of interval ``i`` can first earn the return from interval ``i + 1``. This lag is
    deliberate: the scaffold should make the easiest form of look-ahead leakage impossible.

    Positions are bounded to [-1, 1]. Trading cost is ``cost_bps_per_turnover`` times absolute
    position change. The passive benchmark pays the same one-way cost to establish its long
    position. Equity curves include initial equity as their first value.
    """

    returns = tuple(float(value) for value in market_returns)
    targets = tuple(float(value) for value in target_positions)
    _validate_inputs(returns, targets, cost_bps_per_turnover, initial_equity)

    executed = (0.0, *targets[:-1]) if targets else ()
    previous_position = 0.0
    turnover: list[float] = []
    net_returns: list[float] = []
    cost_rate = cost_bps_per_turnover / 10_000.0

    for index, market_return in enumerate(returns):
        position = executed[index]
        interval_turnover = abs(position - previous_position)
        net_return = position * market_return - interval_turnover * cost_rate
        if net_return <= -1.0:
            raise ValueError("strategy equity would become non-positive")
        turnover.append(interval_turnover)
        net_returns.append(net_return)
        previous_position = position

    strategy_equity = _equity_curve(net_returns, initial_equity)
    benchmark_returns = (returns[0] - cost_rate, *returns[1:])
    benchmark_equity = _equity_curve(benchmark_returns, initial_equity)
    strategy_total_return = strategy_equity[-1] / initial_equity - 1.0
    benchmark_total_return = benchmark_equity[-1] / initial_equity - 1.0

    strategy_max_drawdown = _max_drawdown(strategy_equity)
    benchmark_max_drawdown = _max_drawdown(benchmark_equity)
    strategy_return_over_drawdown = _return_over_drawdown(
        strategy_total_return, strategy_max_drawdown
    )
    benchmark_return_over_drawdown = _return_over_drawdown(
        benchmark_total_return, benchmark_max_drawdown
    )

    return BacktestResult(
        strategy_equity=strategy_equity,
        benchmark_equity=benchmark_equity,
        executed_positions=executed,
        turnover=tuple(turnover),
        strategy_total_return=strategy_total_return,
        benchmark_total_return=benchmark_total_return,
        excess_return=strategy_total_return - benchmark_total_return,
        strategy_max_drawdown=strategy_max_drawdown,
        benchmark_max_drawdown=benchmark_max_drawdown,
        strategy_return_over_drawdown=strategy_return_over_drawdown,
        benchmark_return_over_drawdown=benchmark_return_over_drawdown,
        beats_market=(
            strategy_total_return > 0.0
            and strategy_total_return > benchmark_total_return
            and strategy_return_over_drawdown > benchmark_return_over_drawdown
        ),
    )


def _validate_inputs(
    returns: tuple[float, ...],
    targets: tuple[float, ...],
    cost_bps_per_turnover: float,
    initial_equity: float,
) -> None:
    if not returns:
        raise ValueError("market_returns must not be empty")
    if len(returns) != len(targets):
        raise ValueError("market_returns and target_positions must have equal length")
    if not isfinite(initial_equity) or initial_equity <= 0.0:
        raise ValueError("initial_equity must be finite and positive")
    if not isfinite(cost_bps_per_turnover) or cost_bps_per_turnover < 0.0:
        raise ValueError("cost_bps_per_turnover must be finite and non-negative")
    if any(not isfinite(value) or value <= -1.0 for value in returns):
        raise ValueError("market returns must be finite and greater than -1")
    if any(not isfinite(value) or not -1.0 <= value <= 1.0 for value in targets):
        raise ValueError("target positions must be finite and within [-1, 1]")


def _equity_curve(period_returns: Sequence[float], initial_equity: float) -> tuple[float, ...]:
    curve = [initial_equity]
    for period_return in period_returns:
        curve.append(curve[-1] * (1.0 + period_return))
    return tuple(curve)


def _max_drawdown(equity: Sequence[float]) -> float:
    peak = equity[0]
    drawdown = 0.0
    for value in equity:
        peak = max(peak, value)
        drawdown = max(drawdown, 1.0 - value / peak)
    return drawdown


def _return_over_drawdown(total_return: float, max_drawdown: float) -> float:
    if max_drawdown == 0.0:
        return float("inf") if total_return > 0.0 else 0.0
    return total_return / max_drawdown
