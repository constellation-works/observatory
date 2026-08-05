from __future__ import annotations

import csv
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import numpy as np

from parallax.consumer_goods.pilot import load_attention_history, run_pilot


def _write_history(path: Path, *, rows: int = 220) -> None:
    rng = np.random.default_rng(42)
    smart_ring = np.empty(rows)
    fitness_tracker = np.empty(rows)
    smartwatch = np.empty(rows)
    smart_ring[0] = 8
    fitness_tracker[0] = 45
    smartwatch[0] = 55
    for index in range(1, rows):
        shock = rng.normal(0, 1.2)
        smart_ring[index] = max(1, smart_ring[index - 1] + 0.08 + shock)
        fitness_tracker[index] = max(
            1,
            0.94 * fitness_tracker[index - 1] + 2.8 - 0.35 * shock + rng.normal(0, 0.5),
        )
        smartwatch[index] = max(
            1,
            0.96 * smartwatch[index - 1] + 2.2 - 0.08 * shock + rng.normal(0, 0.5),
        )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Category: All categories"])
        writer.writerow([])
        writer.writerow(
            [
                "Week",
                "smart ring: (United States)",
                "smartwatch: (United States)",
                "fitness tracker: (United States)",
            ]
        )
        start = date(2021, 1, 3)
        for index in range(rows):
            writer.writerow(
                [
                    (start + timedelta(days=7 * index)).isoformat(),
                    f"{smart_ring[index]:.4f}",
                    f"{smartwatch[index]:.4f}",
                    f"{fitness_tracker[index]:.4f}",
                ]
            )


class ConsumerGoodsPilotTests(unittest.TestCase):
    def test_excludes_current_partial_week_and_runs_chronological_split(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "pilot.csv"
            _write_history(path)
            cutoff = date(2025, 3, 23)

            history = load_attention_history(path, as_of=cutoff)
            result = run_pilot(path, as_of=cutoff, bootstrap_samples=100)

            self.assertEqual(history.granularity, "week")
            self.assertTrue(
                all(observed + timedelta(days=7) <= cutoff for observed in history.dates)
            )
            self.assertEqual(
                result.train_rows + result.validation_rows + result.test_rows,
                result.rows - 1 - 12,
            )
            self.assertGreater(result.test_rows, 16)
            self.assertTrue(np.isfinite(result.fitness_tracker_ratio.model_mae))
            self.assertIn(result.decision, {"advance", "stop"})

    def test_rejects_wrong_query_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "pilot.csv"
            _write_history(path)
            content = path.read_text().replace(
                "smartwatch: (United States),fitness tracker: (United States)",
                "fitness tracker: (United States),smartwatch: (United States)",
            )
            path.write_text(content)

            with self.assertRaisesRegex(ValueError, "expected pilot terms in order"):
                load_attention_history(path, as_of=date(2026, 1, 1))

    def test_a_weekly_source_cannot_advance_on_an_unrunnable_weekly_check(self) -> None:
        """E01's gate needs a weekly-aggregation result; weekly data cannot produce one.

        Regression: the flag defaulted to True and was only reassigned for daily data, so the
        artifact claimed 'weekly aggregation check passed' on a source where nothing was checked,
        and that phantom pass counted toward advancing the claim.
        """
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "pilot.csv"
            _write_history(path)

            result = run_pilot(path, as_of=date(2025, 3, 23), bootstrap_samples=100)

            self.assertEqual(result.granularity, "week")
            rationale = " ".join(result.rationale)
            self.assertIn("not runnable", rationale)
            self.assertNotIn("passed", rationale)
            self.assertEqual(result.decision, "stop")

    def test_the_seasonal_term_completes_one_cycle_per_year_on_weekly_data(self) -> None:
        """Regression: dividing day ordinals by 52.1775 gave a 52-*day* cycle, not an annual one.

        The baseline the whole experiment is measured against is 'seasonal persistence'. With a
        seven-week cycle standing in for the year, that baseline carries no annual term and is
        easier to beat than E01 specifies.
        """
        import numpy as np

        from parallax.consumer_goods import pilot as pilot_module

        one_year_later = date(2022, 1, 3).toordinal() - date(2021, 1, 3).toordinal()
        period = pilot_module.DAYS_PER_YEAR
        self.assertAlmostEqual(one_year_later / period, 1.0, places=2)
        self.assertAlmostEqual(
            np.sin(2 * np.pi * date(2021, 1, 3).toordinal() / period),
            np.sin(2 * np.pi * date(2022, 1, 3).toordinal() / period),
            places=2,
        )


if __name__ == "__main__":
    unittest.main()
