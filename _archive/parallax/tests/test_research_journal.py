from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from parallax.research import ResearchIntent, ResearchJournal, ResearchOutcome


class ResearchJournalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        path = Path(self.temporary_directory.name) / "research.sqlite3"
        self.journal = ResearchJournal(path)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_preregistration_is_domain_neutral_and_immutable(self) -> None:
        experiment_id = self.journal.preregister(
            ResearchIntent(
                venture="R02-language-models",
                question="Does a BPE tokenizer reduce validation bytes per token?",
                hypothesis="BPE beats the byte baseline at a fixed vocabulary size.",
                baseline="byte tokenizer",
                method="train both tokenizers on the same corpus split",
                primary_metric="validation bytes per token",
                invalidation="the confidence interval includes zero improvement",
                data_cutoff="corpus-v1 before the held-out split is opened",
            )
        )
        self.journal.record_outcome(
            experiment_id,
            ResearchOutcome(
                summary="BPE reduced validation bytes per token by 18%.",
                decision="advance",
                artifacts="artifacts/tokenizer-bpe-v1.json",
                limitations="One small English-language corpus.",
            ),
        )

        entry = self.journal.get(experiment_id)
        self.assertEqual(entry["venture"], "R02-language-models")
        self.assertEqual(entry["decision"], "advance")

        with sqlite3.connect(self.journal.path) as connection:
            with self.assertRaisesRegex(sqlite3.IntegrityError, "immutable"):
                connection.execute(
                    "UPDATE research_intents SET hypothesis = 'hindsight' WHERE id = ?",
                    (experiment_id,),
                )

    def test_outcome_decision_is_bounded(self) -> None:
        experiment_id = self.journal.preregister(
            ResearchIntent("domain", "q", "h", "b", "m", "metric", "invalid", "cutoff")
        )

        with self.assertRaisesRegex(ValueError, "decision must be one of"):
            self.journal.record_outcome(
                experiment_id,
                ResearchOutcome("summary", "publish", "artifact", "limitations"),
            )


if __name__ == "__main__":
    unittest.main()
