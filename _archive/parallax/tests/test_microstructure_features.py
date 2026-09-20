"""Feature semantics: signs, and the separation of cancellation from execution."""

from __future__ import annotations

import math

import pytest

from parallax.crypto.microstructure.book import BookState, Trade
from parallax.crypto.microstructure.features import (
    DecayState,
    FeatureConfig,
    compute_features,
    feature_columns,
    order_flow_imbalance,
)

SECOND = 1_000_000_000


def book(ts_ns: int, bid_qty: float = 5.0, ask_qty: float = 5.0) -> BookState:
    return BookState(
        ts_ns=ts_ns,
        bids=((100.0, bid_qty), (99.9, 3.0)),
        asks=((100.1, ask_qty), (100.2, 3.0)),
    )


def test_order_flow_imbalance_is_positive_when_the_bid_grows() -> None:
    assert order_flow_imbalance(book(0), book(SECOND, bid_qty=8.0)) == 3.0


def test_order_flow_imbalance_is_negative_when_the_bid_is_pulled() -> None:
    assert order_flow_imbalance(book(0), book(SECOND, bid_qty=2.0)) == -3.0


def test_order_flow_imbalance_counts_a_price_improvement_as_buy_pressure() -> None:
    previous = BookState(ts_ns=0, bids=((100.0, 5.0),), asks=((100.1, 5.0),))
    current = BookState(ts_ns=SECOND, bids=((100.05, 2.0),), asks=((100.1, 5.0),))
    assert order_flow_imbalance(previous, current) == 2.0


def test_order_flow_imbalance_is_zero_for_a_one_sided_book() -> None:
    empty = BookState(ts_ns=0, bids=(), asks=())
    assert order_flow_imbalance(empty, book(SECOND)) == 0.0


def _maker_flow(
    previous: BookState, current: BookState, trades: list[Trade] | None = None
) -> dict[str, float]:
    config = FeatureConfig()
    row = compute_features(
        previous, current, trades or [], config, DecayState(config.flow_half_lives_s)
    )
    assert row is not None
    return row


def test_depth_consumed_by_trades_is_not_counted_as_cancellation() -> None:
    """A wall that was eaten and a wall that was pulled look identical in raw depth."""
    previous = book(0, ask_qty=5.0)
    current = book(SECOND, ask_qty=3.0)
    aggressive_buy = [Trade(ts_ns=SECOND, price=100.1, qty=2.0, buyer_is_maker=False)]
    row = _maker_flow(previous, current, aggressive_buy)
    assert row["maker_flow_ask"] == pytest.approx(0.0)


def test_depth_pulled_without_trades_is_counted_as_cancellation() -> None:
    row = _maker_flow(book(0, ask_qty=5.0), book(SECOND, ask_qty=3.0), [])
    assert row["maker_flow_ask"] == pytest.approx(-2.0)
    assert row["maker_flow_imbalance"] > 0.0  # bids intact, asks thinning


def test_posting_new_size_is_positive_maker_flow() -> None:
    row = _maker_flow(book(0, ask_qty=5.0), book(SECOND, ask_qty=9.0), [])
    assert row["maker_flow_ask"] == pytest.approx(4.0)


def test_void_imbalance_is_positive_when_bids_are_deeper() -> None:
    thin_asks = BookState(
        ts_ns=SECOND,
        bids=((100.0, 20.0), (99.9, 20.0)),
        asks=((100.1, 1.0), (100.2, 1.0)),
    )
    row = _maker_flow(book(0), thin_asks)
    assert row["void_imbalance_25"] > 0.0
    assert row["queue_imbalance"] > 0.0


def test_trade_imbalance_and_gross_quantity() -> None:
    trades = [
        Trade(ts_ns=SECOND, price=100.1, qty=3.0, buyer_is_maker=False),
        Trade(ts_ns=SECOND, price=100.0, qty=1.0, buyer_is_maker=True),
    ]
    row = _maker_flow(book(0), book(SECOND), trades)
    assert row["trade_qty"] == pytest.approx(4.0)
    assert row["trade_imbalance"] == pytest.approx(0.5)


def test_features_are_none_when_mid_is_undefined() -> None:
    config = FeatureConfig()
    one_sided = BookState(ts_ns=SECOND, bids=(), asks=((100.1, 1.0),))
    result = compute_features(book(0), one_sided, [], config, DecayState(config.flow_half_lives_s))
    assert result is None


def test_decay_halves_over_one_half_life() -> None:
    decay = DecayState((10.0,))
    decay.update(dt_s=0.0, signed_qty=10.0, gross_qty=10.0, log_return=0.0)
    assert decay.features()["flow_signed_10"] == pytest.approx(10.0)
    decay.update(dt_s=10.0, signed_qty=0.0, gross_qty=0.0, log_return=0.0)
    assert decay.features()["flow_signed_10"] == pytest.approx(5.0)
    decay.update(dt_s=10.0, signed_qty=0.0, gross_qty=0.0, log_return=0.0)
    assert decay.features()["flow_signed_10"] == pytest.approx(2.5)


def test_decayed_drift_records_recent_direction_in_bps() -> None:
    decay = DecayState((60.0,))
    decay.update(dt_s=0.0, signed_qty=0.0, gross_qty=0.0, log_return=math.log(1.001))
    assert decay.features()["drift_bps_60"] == pytest.approx(9.995, rel=1e-3)


def test_flow_ratio_is_bounded_and_zero_without_volume() -> None:
    decay = DecayState((30.0,))
    decay.update(dt_s=0.0, signed_qty=0.0, gross_qty=0.0, log_return=0.0)
    assert decay.features()["flow_ratio_30"] == 0.0
    decay.update(dt_s=0.0, signed_qty=4.0, gross_qty=4.0, log_return=0.0)
    assert decay.features()["flow_ratio_30"] == pytest.approx(1.0)


def test_feature_columns_match_the_emitted_row() -> None:
    config = FeatureConfig()
    row = _maker_flow(book(0), book(SECOND))
    for name in feature_columns(config):
        assert name in row


def test_invalid_configuration_is_rejected() -> None:
    with pytest.raises(ValueError):
        FeatureConfig(depth_grid_bps=())
    with pytest.raises(ValueError):
        FeatureConfig(flow_half_lives_s=(-1.0,))
    with pytest.raises(ValueError):
        FeatureConfig(maker_flow_band_bps=0.0)
