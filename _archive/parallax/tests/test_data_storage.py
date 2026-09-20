from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pyarrow.parquet as pq

from parallax.crypto.data.candles import Candle, write_candle_stream


class CandleStorageTests(unittest.TestCase):
    def test_daily_partition_is_idempotent_but_not_rewritable(self) -> None:
        first = _candle(0, close=101.0)
        second = _candle(60_000, close=102.0)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            summary = write_candle_stream(
                root,
                [(first, second)],
                expected_start_ms=0,
                expected_end_ms=120_000,
            )
            repeated = write_candle_stream(
                root,
                [(first, second)],
                expected_start_ms=0,
                expected_end_ms=120_000,
            )

            self.assertEqual(summary.rows, 2)
            self.assertEqual(summary.missing_minutes, 0)
            self.assertEqual(repeated.files, summary.files)
            self.assertEqual(pq.read_table(summary.files[0]).num_rows, 2)

            with self.assertRaisesRegex(FileExistsError, "immutable"):
                write_candle_stream(root, [(_candle(0, close=100.5), second)])


def _candle(open_time_ms: int, *, close: float) -> Candle:
    return Candle(
        venue="test",
        symbol="BTC-USD",
        interval="1m",
        open_time_ms=open_time_ms,
        close_time_ms=open_time_ms + 59_999,
        open=100.0,
        high=103.0,
        low=99.0,
        close=close,
        volume=1.0,
    )


if __name__ == "__main__":
    unittest.main()
