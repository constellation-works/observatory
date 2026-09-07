from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from parallax.cli import _research_database_path, build_parser, main


class DoctorCommandTests(unittest.TestCase):
    def test_doctor_makes_safety_posture_explicit(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["doctor"])

        self.assertEqual(exit_code, 0)
        self.assertIn("research_domains: extensible", output.getvalue())
        self.assertIn("crypto_benchmark: bitcoin buy-and-hold", output.getvalue())
        self.assertIn("live_actions: disabled", output.getvalue())
        self.assertIn("live_trading: disabled", output.getvalue())

    def test_domain_neutral_research_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            database = Path(temporary_directory) / "research.sqlite3"
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "research",
                        "--db",
                        str(database),
                        "preregister",
                        "--domain",
                        "R02-language-models",
                        "--question",
                        "Does BPE beat bytes?",
                        "--hypothesis",
                        "BPE improves compression.",
                        "--baseline",
                        "byte tokenizer",
                        "--method",
                        "fixed corpus split",
                        "--metric",
                        "bytes per token",
                        "--invalidation",
                        "no held-out improvement",
                        "--data-cutoff",
                        "corpus-v1",
                    ]
                )
            self.assertEqual(exit_code, 0)
            experiment_id = output.getvalue().strip()

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "research",
                        "--db",
                        str(database),
                        "close",
                        experiment_id,
                        "--summary",
                        "BPE improved compression.",
                        "--decision",
                        "advance",
                        "--artifacts",
                        "artifacts/bpe.json",
                        "--limitations",
                        "one corpus",
                    ]
                )
            self.assertEqual(exit_code, 0)

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "research",
                        "--db",
                        str(database),
                        "show",
                        experiment_id,
                    ]
                )
            self.assertEqual(exit_code, 0)
            record = json.loads(output.getvalue())
            self.assertEqual(record["venture"], "R02-language-models")
            self.assertEqual(record["decision"], "advance")

    def test_domain_defaults_partition_local_data_by_research_slug(self) -> None:
        parser = build_parser()

        fetch = parser.parse_args(
            [
                "data",
                "fetch",
                "--venue",
                "binance",
                "--symbol",
                "BTCUSDT",
                "--start",
                "2026-08-01",
                "--end",
                "2026-08-02",
            ]
        )
        self.assertEqual(fetch.output, Path("data/R01-crypto/raw/candles"))

        record = parser.parse_args(["book", "record"])
        self.assertEqual(record.output, Path("data/R01-crypto/raw/book"))

        consumer_goods = parser.parse_args(
            [
                "consumer-goods",
                "import-history",
                "--google-trends-file",
                "/tmp/trends.csv",
            ]
        )
        self.assertEqual(
            consumer_goods.output,
            Path("data/R03-consumer-goods/raw/history"),
        )
        self.assertEqual(consumer_goods.google_trends_file, Path("/tmp/trends.csv"))

        pilot = parser.parse_args(["consumer-goods", "pilot"])
        # The pilot reads the manifested snapshot by default. A loose CSV is opt-in via --input,
        # because a result that names an unpinned file cannot say which bytes produced it.
        self.assertIsNone(pilot.input)
        self.assertEqual(
            pilot.history_root,
            Path("data/R03-consumer-goods/raw/history"),
        )

        research = parser.parse_args(
            [
                "research",
                "preregister",
                "--domain",
                "R02-language-models",
                "--question",
                "question",
                "--hypothesis",
                "hypothesis",
                "--baseline",
                "baseline",
                "--method",
                "method",
                "--metric",
                "metric",
                "--invalidation",
                "invalidation",
                "--data-cutoff",
                "cutoff",
            ]
        )
        self.assertEqual(
            _research_database_path(research),
            Path("data/R02-language-models/research.sqlite3"),
        )


if __name__ == "__main__":
    unittest.main()
