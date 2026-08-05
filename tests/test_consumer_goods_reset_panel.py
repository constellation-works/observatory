"""Event-aligned panels and their placebo calibration.

The calibration exists to stop a searched-for pattern reading as a discovered one, so the tests
that matter are the ones where the right answer is known: a planted post-event response must be
detected, and pure noise must not be.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import numpy as np
import pytest

from parallax.consumer_goods.reset_panel import (
    build_panel,
    calibrate_against_placebo_calendars,
    load_staple_history,
    panel_extrema,
    placebo_shifts,
    reset_anchor,
    thanksgiving,
    week_over_week_log_change,
)

TERMS = ["alpha", "beta"]


def synthetic_weeks(years: int = 6) -> tuple[list[dt.date], np.ndarray]:
    """Weekly dates and a change matrix of zeros, ready to have a response planted into it."""
    start = dt.date(2020, 1, 5)  # a Sunday
    dates = [start + dt.timedelta(weeks=index) for index in range(52 * years)]
    return dates, np.zeros((len(dates), len(TERMS)))


def anchors_for(dates: list[dt.date]) -> list[dt.date]:
    years = sorted({date.year for date in dates})[1:-1]
    return [reset_anchor(year) for year in years]


class TestCalendar:
    def test_thanksgiving_is_the_fourth_thursday_of_november(self) -> None:
        assert thanksgiving(2021) == dt.date(2021, 11, 25)
        assert thanksgiving(2024) == dt.date(2024, 11, 28)
        assert thanksgiving(2025) == dt.date(2025, 11, 27)

    def test_the_reset_boundary_is_the_sunday_after_thanksgiving(self) -> None:
        """Not the recipe-search spike before it: looking up how to cook is part of the run-up."""
        assert reset_anchor(2021) == dt.date(2021, 11, 28)
        assert reset_anchor(2025) == dt.date(2025, 11, 30)
        for year in range(2021, 2026):
            assert reset_anchor(year).weekday() == 6
            assert 1 <= (reset_anchor(year) - thanksgiving(year)).days <= 7


class TestPlaceboShifts:
    def test_a_window_wider_than_half_a_year_cannot_be_calibrated(self) -> None:
        """E04's -8..+20 window is 29 weeks; two of those do not fit in 52.

        Every placebo would then contain the real event inside its own search range, re-find it,
        and tie — which reads as 'no effect' when it is really 'no valid comparison'.
        """
        with pytest.raises(ValueError, match="cannot be calibrated"):
            placebo_shifts(-8, 20)

    def test_every_placebo_window_is_disjoint_from_the_real_one(self) -> None:
        low, high = -4, 8
        width = high - low + 1
        real = set(range(low, high + 1))
        for shift in placebo_shifts(low, high):
            placebo = {(week + shift) % 52 for week in range(low, high + 1)}
            assert not placebo & {week % 52 for week in real}, f"shift {shift} overlaps"
        assert len(placebo_shifts(low, high)) == 52 - 2 * width + 1


class TestPanel:
    def test_a_planted_post_event_response_is_recovered_at_its_week(self) -> None:
        dates, change = synthetic_weeks()
        anchors = anchors_for(dates)
        index = {date: position for position, date in enumerate(dates)}
        for anchor in anchors:
            change[index[anchor] + 3, 0] = 0.5  # alpha jumps three weeks after every reset

        panel = build_panel(dates, change, anchors, -4, 8)
        alpha_peak = max(
            (e for e in panel_extrema(panel, TERMS, -4) if e.term == "alpha"),
            key=lambda e: e.mean_change,
        )
        assert alpha_peak.relative_week == 3
        assert alpha_peak.mean_change == pytest.approx(0.5)
        assert alpha_peak.unanimous

    def test_positions_with_no_observation_are_nan_not_dropped(self) -> None:
        dates, change = synthetic_weeks(years=2)
        anchors = [reset_anchor(dates[0].year)]
        panel = build_panel(dates, change, anchors, -60, 8)
        assert np.isnan(panel[0, 0, 0]), "a week before the export began has no value"


class TestCalibration:
    def test_a_planted_response_beats_every_placebo_calendar(self) -> None:
        dates, change = synthetic_weeks()
        anchors = anchors_for(dates)
        index = {date: position for position, date in enumerate(dates)}
        for anchor in anchors:
            change[index[anchor] + 2, 0] = -0.4

        results = {
            result.term: result
            for result in calibrate_against_placebo_calendars(dates, change, TERMS, anchors, -4, 8)
        }
        assert results["alpha"].observed == pytest.approx(0.4)
        assert results["alpha"].placebo_at_least_as_extreme == 0
        assert results["alpha"].p_value < 0.05

    def test_noise_does_not_beat_the_placebos_just_because_years_agree(self) -> None:
        """The point of the whole module: unanimity alone is cheap.

        Five years agree by chance one time in sixteen, and the extremum is chosen after searching
        every week in the window — so a searched-for unanimous week must be scored against
        calendars that were allowed to search just as hard.
        """
        rng = np.random.default_rng(0)
        dates, _ = synthetic_weeks(years=8)
        change = rng.normal(0.0, 1.0, size=(len(dates), len(TERMS)))
        anchors = anchors_for(dates)

        results = calibrate_against_placebo_calendars(dates, change, TERMS, anchors, -4, 8)
        for result in results:
            assert result.p_value > 0.05, (
                f"{result.term}: pure noise was called significant at p={result.p_value:.3f}"
            )

    def test_the_p_value_can_never_be_reported_as_zero(self) -> None:
        dates, change = synthetic_weeks()
        anchors = anchors_for(dates)
        change[:, 0] = 1.0  # every week identical, so no week is special
        results = calibrate_against_placebo_calendars(dates, change, TERMS, anchors, -4, 8)
        for result in results:
            assert result.p_value > 0.0


class TestLoading:
    def test_a_trends_export_is_read_past_its_preamble(self, tmp_path: Path) -> None:
        path = tmp_path / "multiTimeline.csv"
        path.write_text(
            "Category: All categories\n\n"
            "Week,rice: (United States),corn: (United States)\n"
            "2021-08-01,57,44\n"
            "2021-08-08,57,43\n",
            encoding="utf-8",
        )
        history = load_staple_history(path)
        assert history.terms == ["rice", "corn"]
        assert history.dates == [dt.date(2021, 8, 1), dt.date(2021, 8, 8)]

        dates, change = week_over_week_log_change(history)
        assert dates == [dt.date(2021, 8, 8)], "a change is stamped at the later week of its pair"
        assert change.shape == (1, 2)

    def test_a_file_without_the_header_row_fails_loudly(self, tmp_path: Path) -> None:
        path = tmp_path / "wrong.csv"
        path.write_text("Region,rice\nWyoming,29%\n", encoding="utf-8")
        with pytest.raises(ValueError, match="Interest-over-time"):
            load_staple_history(path)
