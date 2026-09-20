from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from parallax.crypto.journal import TradeIntent, TradeJournal, TradeOutcome


class TradeJournalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        path = Path(self.temporary_directory.name) / "journal.sqlite3"
        self.journal = TradeJournal(path)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_preregistration_is_immutable_and_outcome_is_appended(self) -> None:
        trade_id = self.journal.preregister(
            TradeIntent(
                hypothesis="Momentum persists after a volatility contraction.",
                entry_rule="Buy on the first close above the 20-bar high.",
                exit_rule="Exit on a close below the 10-bar low.",
                invalidation="No entry if spread exceeds 8 bps.",
                size="0.001 BTC",
                expected_edge_bps=24.0,
            )
        )
        self.journal.record_outcome(
            trade_id,
            TradeOutcome(
                fill="0.001 BTC at 100000 USD",
                fees="0.10 USD",
                slippage_bps=2.0,
                result="+0.75 USD",
            ),
        )

        entry = self.journal.get(trade_id)
        self.assertEqual(entry["expected_edge_bps"], 24.0)
        self.assertEqual(entry["result"], "+0.75 USD")

        with sqlite3.connect(self.journal.path) as connection:
            with self.assertRaisesRegex(sqlite3.IntegrityError, "immutable"):
                connection.execute(
                    "UPDATE trade_intents SET hypothesis = 'hindsight' WHERE id = ?", (trade_id,)
                )

    def test_outcome_can_only_be_recorded_once(self) -> None:
        trade_id = self.journal.preregister(
            TradeIntent("h", "entry", "exit", "invalid", "1 USD", 20.0)
        )
        outcome = TradeOutcome("fill", "fee", 1.0, "result")
        self.journal.record_outcome(trade_id, outcome)

        with self.assertRaises(sqlite3.IntegrityError):
            self.journal.record_outcome(trade_id, outcome)


if __name__ == "__main__":
    unittest.main()
