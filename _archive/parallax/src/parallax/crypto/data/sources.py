"""Unauthenticated Binance and Coinbase one-minute candle sources."""

from __future__ import annotations

import json
import time
from collections.abc import Callable, Iterator
from datetime import UTC, datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from parallax.crypto.data.candles import Candle

MINUTE_MS = 60_000
JsonGetter = Callable[[str], Any]


class BinanceKlines:
    """Paginate Binance Spot klines from the public market-data-only endpoint."""

    base_url = "https://data-api.binance.vision/api/v3/klines"
    page_size = 1_000

    def __init__(self, getter: JsonGetter | None = None, pause_seconds: float = 0.1) -> None:
        self._getter = getter or _get_json
        self._pause_seconds = pause_seconds

    def pages(self, symbol: str, start_ms: int, end_ms: int) -> Iterator[tuple[Candle, ...]]:
        _validate_range(start_ms, end_ms)
        cursor = start_ms
        while cursor < end_ms:
            query = urlencode(
                {
                    "symbol": symbol,
                    "interval": "1m",
                    "startTime": cursor,
                    "endTime": end_ms - 1,
                    "limit": self.page_size,
                }
            )
            payload = self._getter(f"{self.base_url}?{query}")
            if not isinstance(payload, list):
                raise ValueError("unexpected Binance response")
            page = tuple(
                candle
                for candle in (_parse_binance(symbol, row) for row in payload)
                if cursor <= candle.open_time_ms < end_ms
            )
            if page:
                page = tuple(sorted(page, key=lambda candle: candle.open_time_ms))
                yield page
                cursor = page[-1].open_time_ms + MINUTE_MS
            else:
                cursor += self.page_size * MINUTE_MS
            _pause(self._pause_seconds)


class CoinbaseCandles:
    """Paginate Coinbase Exchange public candles in 300-minute windows."""

    base_url = "https://api.exchange.coinbase.com/products"
    page_size = 300

    def __init__(self, getter: JsonGetter | None = None, pause_seconds: float = 0.1) -> None:
        self._getter = getter or _get_json
        self._pause_seconds = pause_seconds

    def pages(self, symbol: str, start_ms: int, end_ms: int) -> Iterator[tuple[Candle, ...]]:
        _validate_range(start_ms, end_ms)
        cursor = start_ms
        while cursor < end_ms:
            chunk_end = min(cursor + self.page_size * MINUTE_MS, end_ms)
            query = urlencode(
                {
                    "start": _iso_utc(cursor),
                    # Coinbase treats both boundaries as inclusive. Stop inside the final minute
                    # so a nominal 300-minute window cannot request 301 buckets.
                    "end": _iso_utc(chunk_end - 1),
                    "granularity": 60,
                }
            )
            url = f"{self.base_url}/{quote(symbol, safe='')}/candles?{query}"
            payload = self._getter(url)
            if not isinstance(payload, list):
                raise ValueError("unexpected Coinbase response")
            page = tuple(
                sorted(
                    (
                        candle
                        for candle in (_parse_coinbase(symbol, row) for row in payload)
                        if cursor <= candle.open_time_ms < chunk_end
                    ),
                    key=lambda candle: candle.open_time_ms,
                )
            )
            if page:
                yield page
            cursor = chunk_end
            _pause(self._pause_seconds)


def _parse_binance(symbol: str, row: list[Any]) -> Candle:
    if len(row) < 11:
        raise ValueError("unexpected Binance kline payload")
    return Candle(
        venue="binance",
        symbol=symbol,
        interval="1m",
        open_time_ms=int(row[0]),
        close_time_ms=int(row[6]),
        open=float(row[1]),
        high=float(row[2]),
        low=float(row[3]),
        close=float(row[4]),
        volume=float(row[5]),
        quote_volume=float(row[7]),
        trade_count=int(row[8]),
    )


def _parse_coinbase(symbol: str, row: list[Any]) -> Candle:
    if len(row) < 6:
        raise ValueError("unexpected Coinbase candle payload")
    open_time_ms = int(row[0]) * 1_000
    return Candle(
        venue="coinbase",
        symbol=symbol,
        interval="1m",
        open_time_ms=open_time_ms,
        close_time_ms=open_time_ms + MINUTE_MS - 1,
        low=float(row[1]),
        high=float(row[2]),
        open=float(row[3]),
        close=float(row[4]),
        volume=float(row[5]),
    )


def _get_json(url: str) -> Any:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "parallax/0.1"})
    retryable_statuses = {418, 429, 500, 502, 503, 504}
    for attempt in range(5):
        try:
            with urlopen(request, timeout=30) as response:  # noqa: S310 - fixed HTTPS URLs
                return json.load(response)
        except HTTPError as error:
            if error.code not in retryable_statuses or attempt == 4:
                raise
            retry_after = error.headers.get("Retry-After")
            delay = float(retry_after) if retry_after else float(2**attempt)
            time.sleep(delay)
        except URLError:
            if attempt == 4:
                raise
            time.sleep(float(2**attempt))
    raise AssertionError("unreachable retry loop")


def _validate_range(start_ms: int, end_ms: int) -> None:
    if start_ms < 0 or end_ms <= start_ms:
        raise ValueError("start must be before end")
    if start_ms % MINUTE_MS or end_ms % MINUTE_MS:
        raise ValueError("start and end must align to UTC minute boundaries")


def _iso_utc(timestamp_ms: int) -> str:
    value = datetime.fromtimestamp(timestamp_ms / 1_000, tz=UTC)
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def _pause(seconds: float) -> None:
    if seconds < 0.0:
        raise ValueError("pause_seconds must be non-negative")
    if seconds:
        time.sleep(seconds)
