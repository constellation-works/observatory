"""End-to-end replay of a synthetic capture, including capture holes."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

from parallax.crypto.microstructure.book import iter_records
from parallax.crypto.microstructure.pipeline import BuildSummary, build_features, iter_feature_rows
from parallax.crypto.microstructure.record import CaptureConfig, CaptureWriter, capture_paths

MS = 1_000_000


def snapshot_record(local_ms: int, last_update_id: int) -> dict:
    return {
        "kind": "snapshot",
        "local_ns": local_ms * MS,
        "data": {
            "lastUpdateId": last_update_id,
            "bids": [["100.00", "5"], ["99.95", "4"]],
            "asks": [["100.10", "5"], ["100.15", "4"]],
        },
    }


def depth_record(event_ms: int, first_id: int, final_id: int, bid_qty: float) -> dict:
    return {
        "kind": "ws",
        "local_ns": event_ms * MS,
        "stream": "btcusdt@depth@100ms",
        "data": {
            "e": "depthUpdate",
            "E": event_ms,
            "U": first_id,
            "u": final_id,
            "b": [["100.00", f"{bid_qty}"]],
            "a": [],
        },
    }


def trade_record(event_ms: int, qty: float, buyer_is_maker: bool) -> dict:
    return {
        "kind": "ws",
        "local_ns": event_ms * MS,
        "stream": "btcusdt@aggTrade",
        "data": {
            "e": "aggTrade",
            "E": event_ms,
            "T": event_ms,
            "p": "100.05",
            "q": f"{qty}",
            "m": buyer_is_maker,
        },
    }


def synthetic_capture(seconds: int = 30) -> list[dict]:
    base_ms = 1_700_000_000_000
    records: list[dict] = [snapshot_record(base_ms, last_update_id=1_000)]
    update_id = 1_001
    for step in range(seconds * 5):  # one book update every 200 ms
        event_ms = base_ms + step * 200
        records.append(depth_record(event_ms, update_id, update_id + 4, 5.0 + step % 3))
        update_id += 5
        if step % 5 == 0:
            records.append(trade_record(event_ms + 50, qty=0.5, buyer_is_maker=step % 10 == 0))
    return records


def test_replay_produces_one_row_per_sample_instant() -> None:
    summary = BuildSummary()
    rows = list(iter_feature_rows(synthetic_capture(30), sample_seconds=1.0, summary=summary))
    assert 25 <= len(rows) <= 30
    assert summary.rows == len(rows)
    assert summary.gaps == 0
    assert summary.trades > 0

    timestamps = [row["ts_ns"] for row in rows]
    assert timestamps == sorted(timestamps)
    assert all(row["mid"] > 0.0 for row in rows)
    assert all(row["dt_s"] > 0.0 for row in rows)


def test_sampling_interval_controls_row_count() -> None:
    coarse = list(iter_feature_rows(synthetic_capture(30), sample_seconds=5.0))
    fine = list(iter_feature_rows(synthetic_capture(30), sample_seconds=1.0))
    assert len(coarse) < len(fine)


def test_a_desync_suppresses_rows_until_the_next_snapshot() -> None:
    records = synthetic_capture(20)
    base_ms = 1_700_000_000_000
    # Break the update-id chain a third of the way in, then re-anchor much later.
    records.insert(40, depth_record(base_ms + 8_000, 9_000_000, 9_000_004, 7.0))
    records.append(snapshot_record(base_ms + 30_000, last_update_id=9_100_000))

    summary = BuildSummary()
    rows = list(iter_feature_rows(records, sample_seconds=1.0, summary=summary))
    assert summary.gaps >= 1
    assert summary.samples_skipped_desync >= 1
    assert rows, "rows before the gap are still valid"


def test_stale_book_samples_are_skipped() -> None:
    records = synthetic_capture(5)
    base_ms = 1_700_000_000_000
    # A long silence with the update-id chain intact: the book is still synced, just old.
    # Sampling must not carry the last known book forward across the hole.
    records.append(depth_record(base_ms + 600_000, 1_126, 1_130, 5.0))
    summary = BuildSummary()
    list(iter_feature_rows(records, sample_seconds=1.0, max_staleness_seconds=5.0, summary=summary))
    assert summary.gaps == 0, "the chain is contiguous, so this is staleness and not a desync"
    assert summary.samples_skipped_stale > 500


def test_a_sample_never_sees_an_update_stamped_at_its_own_instant() -> None:
    """Regression: draining after applying leaked the event at time T into the sample at T."""
    base_ms = 1_700_000_000_000  # exactly on the one-second sampling grid
    records: list[dict] = [snapshot_record(base_ms, last_update_id=1_000)]
    update_id = 1_001
    for step in range(1, 10):
        records.append(depth_record(base_ms + step * 200, update_id, update_id + 4, 5.0))
        update_id += 5
    # A wall an order of magnitude larger appears exactly at the second sample instant.
    records.append(depth_record(base_ms + 2_000, update_id, update_id + 4, 500.0))
    update_id += 5
    for step in range(11, 21):
        records.append(depth_record(base_ms + step * 200, update_id, update_id + 4, 500.0))
        update_id += 5

    rows = {int(row["ts_ns"]): row for row in iter_feature_rows(records, sample_seconds=1.0)}
    at_the_instant = rows[(base_ms + 2_000) * MS]
    assert at_the_instant["depth_bid_25"] < 1_000.0, "the wall posted at T leaked into sample T"
    assert rows[(base_ms + 3_000) * MS]["depth_bid_25"] > 10_000.0


def test_capture_writer_round_trips_through_the_reader(tmp_path: Path) -> None:
    config = CaptureConfig(symbol="BTCUSDT", root=tmp_path)
    writer = CaptureWriter(config)
    writer.write({"kind": "event", "local_ns": 1, "event": "ws_connected"})
    writer.write(snapshot_record(1_700_000_000_000, last_update_id=5))
    writer.close()

    # The writer may legitimately rotate mid-test if the wall clock crosses an hour boundary,
    # so assert on record content, not file count.
    paths = capture_paths(tmp_path, "BTCUSDT")
    assert len(paths) >= 1
    records = list(iter_records(paths))
    assert records[0]["kind"] == "manifest", "every rotated file must open with the manifest"
    assert records[0]["symbol"] == "BTCUSDT"
    assert records[0]["capture_version"] == 2
    kinds = [record["kind"] for record in records]
    assert kinds.count("snapshot") == 1
    assert [r.get("event") for r in records if r["kind"] == "event"] == ["ws_connected"]


def test_a_live_truncated_capture_reads_to_the_truncation_point(tmp_path: Path) -> None:
    """Regression: analyzing while the recorder is mid-write must not abort the replay."""
    complete = tmp_path / "a.jsonl.gz"
    with gzip.open(complete, "wt", encoding="utf-8") as handle:
        handle.write(json.dumps({"kind": "event", "local_ns": 1}) + "\n")

    live = tmp_path / "b.jsonl.gz"
    with gzip.open(live, "wt", encoding="utf-8") as handle:
        for index in range(200):
            handle.write(json.dumps({"kind": "event", "local_ns": index}) + "\n")
    live.write_bytes(live.read_bytes()[:-30])  # no gzip end-of-stream marker, like a live file

    records = list(iter_records([complete, live]))
    assert records[0]["local_ns"] == 1, "the complete file must be read fully"
    assert len(records) > 1, "the truncated file must still yield its intact prefix"


def test_reader_skips_malformed_lines(tmp_path: Path) -> None:
    path = tmp_path / "broken.jsonl.gz"
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        handle.write(json.dumps({"kind": "event", "local_ns": 1}) + "\n")
        handle.write("{not json\n")
        handle.write("\n")
        handle.write(json.dumps({"kind": "event", "local_ns": 2}) + "\n")
    assert len(list(iter_records([path]))) == 2


def test_build_features_writes_a_parquet_table(tmp_path: Path) -> None:
    import pyarrow.parquet as pq

    capture = tmp_path / "capture.jsonl.gz"
    with gzip.open(capture, "wt", encoding="utf-8") as handle:
        for record in synthetic_capture(60):
            handle.write(json.dumps(record) + "\n")

    output = tmp_path / "features.parquet"
    summary = build_features([capture], output, sample_seconds=1.0)
    assert summary.rows > 0
    assert summary.output == output

    table = pq.read_table(output)
    assert table.num_rows == summary.rows
    for column in ("ts_ns", "mid", "queue_imbalance", "ofi", "maker_flow_imbalance"):
        assert column in table.column_names


def test_capture_config_validation() -> None:
    import pytest

    with pytest.raises(ValueError):
        CaptureConfig(symbol="")
    with pytest.raises(ValueError):
        CaptureConfig(symbol="BTC-USD")
    with pytest.raises(ValueError):
        CaptureConfig(symbol="BTCUSDT", depth_limit=0)
    with pytest.raises(ValueError):
        CaptureConfig(symbol="BTCUSDT", snapshot_seconds=0.0)

    config = CaptureConfig(symbol="btcusdt")
    assert config.streams[0] == "btcusdt@depth@100ms"
    assert "streams=" in config.ws_url
    assert config.manifest()["symbol"] == "BTCUSDT"
