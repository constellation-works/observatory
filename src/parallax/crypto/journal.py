"""Append-only trade preregistration and outcome journal."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from math import isfinite
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True)
class TradeIntent:
    hypothesis: str
    entry_rule: str
    exit_rule: str
    invalidation: str
    size: str
    expected_edge_bps: float


@dataclass(frozen=True)
class TradeOutcome:
    fill: str
    fees: str
    slippage_bps: float
    result: str


class TradeJournal:
    """SQLite journal whose records cannot be updated or deleted through normal SQL writes."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def preregister(self, intent: TradeIntent) -> str:
        _require_text(intent.hypothesis, "hypothesis")
        _require_text(intent.entry_rule, "entry_rule")
        _require_text(intent.exit_rule, "exit_rule")
        _require_text(intent.invalidation, "invalidation")
        _require_text(intent.size, "size")
        if not isfinite(intent.expected_edge_bps):
            raise ValueError("expected_edge_bps must be finite")
        trade_id = uuid4().hex
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO trade_intents (
                    id, created_at, hypothesis, entry_rule, exit_rule, invalidation, size,
                    expected_edge_bps
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    trade_id,
                    _now(),
                    intent.hypothesis,
                    intent.entry_rule,
                    intent.exit_rule,
                    intent.invalidation,
                    intent.size,
                    intent.expected_edge_bps,
                ),
            )
        return trade_id

    def record_outcome(self, trade_id: str, outcome: TradeOutcome) -> None:
        _require_text(outcome.fill, "fill")
        _require_text(outcome.fees, "fees")
        _require_text(outcome.result, "result")
        if not isfinite(outcome.slippage_bps):
            raise ValueError("slippage_bps must be finite")
        with self._connect() as connection:
            exists = connection.execute(
                "SELECT 1 FROM trade_intents WHERE id = ?", (trade_id,)
            ).fetchone()
            if exists is None:
                raise KeyError(f"unknown trade id: {trade_id}")
            connection.execute(
                """
                INSERT INTO trade_outcomes (
                    trade_id, recorded_at, fill, fees, slippage_bps, result
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    trade_id,
                    _now(),
                    outcome.fill,
                    outcome.fees,
                    outcome.slippage_bps,
                    outcome.result,
                ),
            )

    def get(self, trade_id: str) -> dict[str, object]:
        with self._connect() as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute(
                """
                SELECT i.*, o.recorded_at, o.fill, o.fees, o.slippage_bps, o.result
                FROM trade_intents AS i
                LEFT JOIN trade_outcomes AS o ON o.trade_id = i.id
                WHERE i.id = ?
                """,
                (trade_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"unknown trade id: {trade_id}")
        return dict(row)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS trade_intents (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    hypothesis TEXT NOT NULL,
                    entry_rule TEXT NOT NULL,
                    exit_rule TEXT NOT NULL,
                    invalidation TEXT NOT NULL,
                    size TEXT NOT NULL,
                    expected_edge_bps REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS trade_outcomes (
                    trade_id TEXT PRIMARY KEY REFERENCES trade_intents(id),
                    recorded_at TEXT NOT NULL,
                    fill TEXT NOT NULL,
                    fees TEXT NOT NULL,
                    slippage_bps REAL NOT NULL,
                    result TEXT NOT NULL
                );

                CREATE TRIGGER IF NOT EXISTS trade_intents_no_update
                BEFORE UPDATE ON trade_intents
                BEGIN
                    SELECT RAISE(ABORT, 'trade preregistrations are immutable');
                END;

                CREATE TRIGGER IF NOT EXISTS trade_intents_no_delete
                BEFORE DELETE ON trade_intents
                BEGIN
                    SELECT RAISE(ABORT, 'trade preregistrations are immutable');
                END;

                CREATE TRIGGER IF NOT EXISTS trade_outcomes_no_update
                BEFORE UPDATE ON trade_outcomes
                BEGIN
                    SELECT RAISE(ABORT, 'trade outcomes are append-only');
                END;

                CREATE TRIGGER IF NOT EXISTS trade_outcomes_no_delete
                BEFORE DELETE ON trade_outcomes
                BEGIN
                    SELECT RAISE(ABORT, 'trade outcomes are append-only');
                END;
                """
            )


def _now() -> str:
    return datetime.now(tz=UTC).isoformat()


def _require_text(value: str, name: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must not be empty")
