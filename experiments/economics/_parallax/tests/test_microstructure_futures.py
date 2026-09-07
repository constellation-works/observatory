"""Futures capture config and the pu-chained depth sync rule."""

from __future__ import annotations

from pathlib import Path

import pytest

from parallax.crypto.microstructure.book import BookAssembler
from parallax.crypto.microstructure.record import CaptureConfig, CaptureWriter, capture_paths


def snapshot(last_update_id: int) -> dict:
    return {
        "lastUpdateId": last_update_id,
        "bids": [["100.00", "5"]],
        "asks": [["100.10", "5"]],
    }


def futures_diff(first_id: int, final_id: int, previous_u: int, bids=()) -> dict:
    return {"e": "depthUpdate", "U": first_id, "u": final_id, "pu": previous_u, "b": list(bids)}


class TestFuturesConfig:
    def test_futures_selects_fstream_forceorder_and_markprice(self) -> None:
        config = CaptureConfig(symbol="BTCUSDT", market="futures")
        assert config.ws_url.startswith("wss://fstream.binance.com/stream?streams=")
        assert "btcusdt@forceOrder" in config.streams
        assert "btcusdt@markPrice@1s" in config.streams
        assert "btcusdt@depth@100ms" in config.streams
        assert config.rest_url.startswith("https://fapi.binance.com/fapi/v1/depth")
        assert config.effective_depth_limit == 1_000
        assert config.capture_label == "BTCUSDT-PERP"
        assert config.manifest()["market"] == "futures"

    def test_spot_defaults_are_unchanged(self) -> None:
        config = CaptureConfig(symbol="BTCUSDT")
        assert config.capture_label == "BTCUSDT"
        assert config.effective_depth_limit == 5_000
        assert "btcusdt@forceOrder" not in config.streams
        assert config.ws_url.startswith("wss://data-stream.binance.vision/")

    def test_depth_limit_beyond_the_market_maximum_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="REST maximum"):
            CaptureConfig(symbol="BTCUSDT", market="futures", depth_limit=5_000)
        with pytest.raises(ValueError, match="market"):
            CaptureConfig(symbol="BTCUSDT", market="margin")

    def test_capture_directories_never_mix_markets(self, tmp_path: Path) -> None:
        for market in ("spot", "futures"):
            writer = CaptureWriter(CaptureConfig(symbol="BTCUSDT", market=market, root=tmp_path))
            writer.write({"kind": "event", "local_ns": 1, "event": "ws_connected"})
            writer.close()
        assert len(capture_paths(tmp_path, "BTCUSDT", "spot")) == 1
        assert len(capture_paths(tmp_path, "BTCUSDT", "futures")) == 1
        assert capture_paths(tmp_path, "BTCUSDT", "spot") != capture_paths(
            tmp_path, "BTCUSDT", "futures"
        )


class TestFuturesSync:
    def test_pu_chain_applies_even_when_ids_are_not_contiguous(self) -> None:
        assembler = BookAssembler()
        assembler.apply_snapshot(snapshot(100))
        # Futures ids skip ranges; continuity is pu == previous u, not U == u + 1.
        assert assembler.apply_diff(futures_diff(98, 120, 90, bids=[["100.00", "7"]])) is True
        assert assembler.apply_diff(futures_diff(150, 180, 120, bids=[["100.00", "8"]])) is True
        assert assembler.state(ts_ns=1).bids[0][1] == 8.0
        assert assembler.gaps == 0

    def test_a_pu_mismatch_desyncs(self) -> None:
        assembler = BookAssembler()
        assembler.apply_snapshot(snapshot(100))
        assembler.apply_diff(futures_diff(98, 120, 90))
        assert assembler.apply_diff(futures_diff(300, 320, 250)) is False
        assert assembler.synced is False
        assert assembler.gaps == 1

    def test_stale_futures_diffs_are_skipped_without_desync(self) -> None:
        assembler = BookAssembler()
        assembler.apply_snapshot(snapshot(100))
        assert assembler.apply_diff(futures_diff(50, 90, 40)) is False
        assert assembler.synced is True
        assert assembler.skipped_diffs == 1
