from __future__ import annotations

import json
import tempfile
import unittest
from datetime import UTC, date, datetime
from pathlib import Path

from parallax.consumer_goods.data.history import import_historical_snapshot
from parallax.consumer_goods.universe import (
    PILOT_TRENDS_BASKETS,
    TRACKED_PRODUCT_TYPES,
    TRACKED_TRENDS_BASKETS,
)


def _write_pilot_export(directory: Path, *, wearable_value: int = 50) -> Path:
    directory.mkdir(parents=True)
    basket = PILOT_TRENDS_BASKETS[0]
    header = ",".join(f"{term}: (United States)" for term in basket.terms)
    row = ",".join(str(value) for value in (wearable_value, 75, 35))
    path = directory / f"{basket.basket_id}.csv"
    path.write_text(
        f"Category: All categories\n\nWeek,{header}\n2026-08-02,{row}\n",
        encoding="utf-8",
    )
    return path


class ConsumerGoodsHistoricalImportTests(unittest.TestCase):
    def test_frozen_universe_matches_the_documented_scope(self) -> None:
        self.assertEqual(
            {tracked.family for tracked in TRACKED_PRODUCT_TYPES},
            {"wearable-health", "floor-cleaning", "countertop-cooking"},
        )
        self.assertEqual(len(TRACKED_PRODUCT_TYPES), 10)
        identities = {(tracked.family, tracked.product_type) for tracked in TRACKED_PRODUCT_TYPES}
        self.assertEqual(len(identities), len(TRACKED_PRODUCT_TYPES))
        self.assertEqual(len(TRACKED_TRENDS_BASKETS), 3)
        self.assertEqual(
            tuple(basket.basket_id for basket in PILOT_TRENDS_BASKETS),
            ("wearable-health",),
        )

        document = (
            (
                Path(__file__).parents[1]
                / "docs/research/R03-consumer-goods/docs/TRACKING_UNIVERSE.md"
            )
            .read_text()
            .lower()
        )
        for tracked in TRACKED_PRODUCT_TYPES:
            self.assertIn(tracked.product_type.replace("-", " "), document)
            self.assertIn(tracked.search_term, document)
            for brand in tracked.brands:
                self.assertIn(brand.lower(), document)

    def test_preserves_google_trends_pilot_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            exports = temporary / "exports"
            export = _write_pilot_export(exports)

            result = import_historical_snapshot(
                temporary / "raw" / "history",
                google_trends_file=export,
                snapshot_date=date(2026, 8, 2),
                collected_at=datetime(2026, 8, 2, 18, tzinfo=UTC),
            )

            self.assertTrue(result.created)
            self.assertEqual(result.snapshot.name, "2026-08-02")
            self.assertEqual(len(result.files), 1)
            manifest = json.loads((result.snapshot / "manifest.json").read_text())
            self.assertEqual(manifest["schema_version"], 2)
            self.assertEqual(
                manifest["research_grain"],
                "product-family, product-type, geography, and historical week",
            )
            self.assertIn("not purchases", manifest["interpretation"])
            self.assertEqual(
                {source["basket_id"] for source in manifest["sources"]},
                {"wearable-health"},
            )
            self.assertEqual(manifest["sources"][0]["granularity"], "week")

    def test_accepts_daily_official_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            exports = temporary / "exports"
            export = _write_pilot_export(exports)
            path = exports / "wearable-health.csv"
            path.write_text(
                path.read_text().replace("Week,", "Day,"),
                encoding="utf-8",
            )

            result = import_historical_snapshot(
                temporary / "raw" / "history",
                google_trends_file=export,
                snapshot_date=date(2026, 8, 2),
                collected_at=datetime(2026, 8, 2, 18, tzinfo=UTC),
            )

            manifest = json.loads((result.snapshot / "manifest.json").read_text())
            self.assertEqual(manifest["sources"][0]["granularity"], "day")

    def test_identical_rerun_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            exports = temporary / "exports"
            export = _write_pilot_export(exports)
            root = temporary / "history"
            arguments = {
                "google_trends_file": export,
                "snapshot_date": date(2026, 8, 2),
            }
            first = import_historical_snapshot(
                root,
                **arguments,
                collected_at=datetime(2026, 8, 2, 18, tzinfo=UTC),
            )
            second = import_historical_snapshot(
                root,
                **arguments,
                collected_at=datetime(2026, 8, 2, 19, tzinfo=UTC),
            )

            self.assertTrue(first.created)
            self.assertFalse(second.created)
            self.assertEqual(first.snapshot, second.snapshot)

    def test_rejects_changed_source_for_existing_date(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            exports = temporary / "exports"
            export = _write_pilot_export(exports)
            root = temporary / "history"
            import_historical_snapshot(
                root,
                google_trends_file=export,
                snapshot_date=date(2026, 8, 2),
                collected_at=datetime(2026, 8, 2, 18, tzinfo=UTC),
            )
            (exports / "wearable-health.csv").write_text(
                "Week,smart ring,smartwatch,fitness tracker\n2026-08-02,51,75,35\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(FileExistsError, "source changed"):
                import_historical_snapshot(
                    root,
                    google_trends_file=export,
                    snapshot_date=date(2026, 8, 2),
                    collected_at=datetime(2026, 8, 2, 19, tzinfo=UTC),
                )

    def test_requires_the_pilot_export(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            exports = Path(temporary_directory)
            with self.assertRaisesRegex(ValueError, "export does not exist"):
                import_historical_snapshot(
                    exports / "raw",
                    google_trends_file=exports / "missing.csv",
                )

    def test_rejects_terms_that_differ_from_frozen_basket(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            exports = Path(temporary_directory) / "exports"
            export = _write_pilot_export(exports)
            (exports / "wearable-health.csv").write_text(
                "Week,smart ring,smartwatch,activity tracker\n2026-08-02,50,75,35\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "terms differ from frozen basket"):
                import_historical_snapshot(
                    Path(temporary_directory) / "raw",
                    google_trends_file=export,
                )


if __name__ == "__main__":
    unittest.main()
