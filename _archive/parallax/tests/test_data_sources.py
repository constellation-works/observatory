from __future__ import annotations

import unittest
from urllib.parse import parse_qs, urlparse

from parallax.crypto.data.sources import MINUTE_MS, BinanceKlines, CoinbaseCandles


class BinanceKlinesTests(unittest.TestCase):
    def test_normalizes_public_kline_payload(self) -> None:
        seen_urls: list[str] = []

        def get(url: str) -> list[list[object]]:
            seen_urls.append(url)
            return [
                [
                    0,
                    "100.0",
                    "102.0",
                    "99.0",
                    "101.0",
                    "5.0",
                    MINUTE_MS - 1,
                    "500.0",
                    12,
                    "2.0",
                    "200.0",
                    "0",
                ],
                [
                    MINUTE_MS,
                    "101.0",
                    "103.0",
                    "100.0",
                    "102.0",
                    "6.0",
                    2 * MINUTE_MS - 1,
                    "600.0",
                    14,
                    "3.0",
                    "300.0",
                    "0",
                ],
            ]

        pages = list(BinanceKlines(getter=get, pause_seconds=0).pages("BTCUSDT", 0, 120_000))

        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0][0].venue, "binance")
        self.assertEqual(pages[0][1].close, 102.0)
        query = parse_qs(urlparse(seen_urls[0]).query)
        self.assertEqual(query["interval"], ["1m"])
        self.assertEqual(query["limit"], ["1000"])


class CoinbaseCandlesTests(unittest.TestCase):
    def test_normalizes_reverse_order_public_candles(self) -> None:
        seen_urls: list[str] = []

        def get(url: str) -> list[list[object]]:
            seen_urls.append(url)
            return [
                [60, "100", "103", "101", "102", "6"],
                [0, "99", "102", "100", "101", "5"],
            ]

        pages = list(CoinbaseCandles(getter=get, pause_seconds=0).pages("BTC-USD", 0, 120_000))

        self.assertEqual([candle.open_time_ms for candle in pages[0]], [0, 60_000])
        self.assertEqual(pages[0][0].venue, "coinbase")
        query = parse_qs(urlparse(seen_urls[0]).query)
        self.assertEqual(query["granularity"], ["60"])
        self.assertEqual(query["end"], ["1970-01-01T00:01:59Z"])


if __name__ == "__main__":
    unittest.main()
