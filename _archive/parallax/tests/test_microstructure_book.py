"""Book reconstruction, with emphasis on the failure branch."""

from __future__ import annotations

import pytest

from parallax.crypto.microstructure.book import BookAssembler, BookState, DesyncError, parse_trade


def snapshot(last_update_id: int = 100) -> dict:
    return {
        "lastUpdateId": last_update_id,
        "bids": [["100.00", "5"], ["99.90", "3"], ["99.50", "10"]],
        "asks": [["100.10", "4"], ["100.20", "6"], ["100.50", "12"]],
    }


def diff(first_id: int, final_id: int, bids=(), asks=()) -> dict:
    return {"e": "depthUpdate", "U": first_id, "u": final_id, "b": list(bids), "a": list(asks)}


def test_snapshot_anchors_the_book() -> None:
    assembler = BookAssembler()
    assert assembler.apply_snapshot(snapshot()) is True
    state = assembler.state(ts_ns=1)
    assert state.best_bid == 100.0
    assert state.best_ask == 100.1
    assert state.mid == pytest.approx(100.05)


def test_stale_diffs_before_the_snapshot_are_discarded() -> None:
    assembler = BookAssembler()
    assembler.apply_snapshot(snapshot(last_update_id=100))
    assert assembler.apply_diff(diff(90, 95, bids=[["100.00", "99"]])) is False
    assert assembler.state(ts_ns=1).bids[0][1] == 5.0
    assert assembler.skipped_diffs == 1


def test_first_diff_may_straddle_the_snapshot_id() -> None:
    assembler = BookAssembler()
    assembler.apply_snapshot(snapshot(last_update_id=100))
    assert assembler.apply_diff(diff(98, 103, bids=[["100.00", "7"]])) is True
    assert assembler.state(ts_ns=1).bids[0][1] == 7.0


def test_contiguous_chain_applies_and_zero_quantity_removes_a_level() -> None:
    assembler = BookAssembler()
    assembler.apply_snapshot(snapshot(last_update_id=100))
    assert assembler.apply_diff(diff(101, 105, asks=[["100.10", "0"]])) is True
    assert assembler.apply_diff(diff(106, 110, asks=[["100.15", "2"]])) is True
    state = assembler.state(ts_ns=1)
    assert state.best_ask == 100.15
    assert assembler.applied_diffs == 2
    assert assembler.gaps == 0


def test_a_broken_chain_desyncs_rather_than_inventing_liquidity() -> None:
    assembler = BookAssembler()
    assembler.apply_snapshot(snapshot(last_update_id=100))
    assembler.apply_diff(diff(101, 105, bids=[["100.00", "6"]]))
    assert assembler.apply_diff(diff(200, 205, bids=[["100.00", "99"]])) is False
    assert assembler.gaps == 1
    assert assembler.synced is False
    with pytest.raises(DesyncError):
        assembler.state(ts_ns=1)
    # Diffs stay rejected until a fresh snapshot re-anchors the book.
    assert assembler.apply_diff(diff(206, 210, bids=[["100.00", "99"]])) is False
    assert assembler.apply_snapshot(snapshot(last_update_id=300)) is True
    assert assembler.state(ts_ns=1).bids[0][1] == 5.0


def test_diffs_received_while_the_snapshot_was_in_flight_are_replayed_across_it() -> None:
    """Regression for the real-capture zero-rows failure.

    The REST snapshot takes long enough that the diffs covering ``lastUpdateId + 1`` onward arrive
    over the websocket first, so in file order they *precede* the snapshot record. Binance's sync
    procedure requires buffering and replaying them; looking only forward desyncs on every anchor.
    """
    assembler = BookAssembler()
    # Receive order from the live capture: diffs first, snapshot record after.
    assert assembler.apply_diff(diff(560, 572, bids=[["100.00", "1"]])) is False  # pre-snapshot
    assert assembler.apply_diff(diff(573, 600, bids=[["100.00", "7"]])) is False  # buffered
    assert assembler.apply_diff(diff(601, 684, asks=[["100.10", "9"]])) is False  # buffered
    assembler.apply_snapshot(snapshot(last_update_id=572))

    state = assembler.state(ts_ns=1)
    assert state.bids[0][1] == 7.0, "the buffered straddling diff must be replayed"
    assert state.asks[0][1] == 9.0
    assert assembler.applied_diffs == 2
    assert assembler.gaps == 0
    # And the live chain continues seamlessly from the replayed buffer.
    assert assembler.apply_diff(diff(685, 702, bids=[["100.00", "3"]])) is True
    assert assembler.state(ts_ns=2).bids[0][1] == 3.0


def test_a_hole_inside_the_buffer_itself_still_desyncs() -> None:
    assembler = BookAssembler()
    assembler.apply_diff(diff(573, 600, bids=[["100.00", "7"]]))
    # 601..684 genuinely missing from the buffer.
    assembler.apply_diff(diff(685, 700, bids=[["100.00", "9"]]))
    assembler.apply_snapshot(snapshot(last_update_id=572))
    assert assembler.gaps == 1
    assert assembler.synced is False
    with pytest.raises(DesyncError):
        assembler.state(ts_ns=1)


def test_a_stale_snapshot_never_overwrites_a_newer_book() -> None:
    assembler = BookAssembler()
    assembler.apply_snapshot(snapshot(last_update_id=500))
    assembler.apply_diff(diff(501, 505, bids=[["100.00", "42"]]))
    assert assembler.apply_snapshot(snapshot(last_update_id=200)) is False
    assert assembler.state(ts_ns=1).bids[0][1] == 42.0


def test_depth_within_bps_uses_a_band_around_mid() -> None:
    state = BookState(
        ts_ns=1,
        bids=((100.0, 5.0), (99.9, 3.0), (99.5, 10.0)),
        asks=((100.1, 4.0), (100.2, 6.0), (100.5, 12.0)),
    )
    # mid is 100.05; a 10 bps band spans 99.95 to 100.15.
    assert state.depth_within_bps(10.0) == (5.0, 4.0)
    assert state.depth_within_bps(25.0) == (8.0, 10.0)
    bid_notional, ask_notional = state.notional_within_bps(10.0)
    assert bid_notional == pytest.approx(500.0)
    assert ask_notional == pytest.approx(400.4)


def test_spread_and_one_sided_books() -> None:
    state = BookState(ts_ns=1, bids=((100.0, 1.0),), asks=((100.1, 1.0),))
    assert state.spread_bps == pytest.approx(9.995, rel=1e-3)
    empty = BookState(ts_ns=1, bids=(), asks=((100.1, 1.0),))
    assert empty.mid is None
    assert empty.spread_bps is None
    assert empty.depth_within_bps(10.0) == (0.0, 0.0)


def test_trade_sign_follows_the_aggressor_not_the_maker() -> None:
    lifted_the_ask = parse_trade({"p": "100.1", "q": "2", "m": False, "T": 1_700}, local_ns=0)
    hit_the_bid = parse_trade({"p": "100.0", "q": "2", "m": True, "T": 1_700}, local_ns=0)
    assert lifted_the_ask.signed_qty == 2.0
    assert hit_the_bid.signed_qty == -2.0
    assert lifted_the_ask.ts_ns == 1_700 * 1_000_000
    assert lifted_the_ask.notional == pytest.approx(200.2)


def test_trade_falls_back_to_local_time_when_the_exchange_omits_it() -> None:
    trade = parse_trade({"p": "1", "q": "1", "m": False}, local_ns=1234)
    assert trade.ts_ns == 1234
