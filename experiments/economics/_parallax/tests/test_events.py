"""The calendar's value is its discipline; these tests are the discipline."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from parallax.crypto.events import Event, EventStore


def unlock(**overrides) -> Event:
    fields = {
        "event_type": "token_unlock",
        "asset": "ARB",
        "venue": "binance",
        "event_time_utc": "2026-09-16T13:00:00Z",
        "announced_time_utc": "2023-03-16T00:00:00Z",
        "source_url": "https://example.com/vesting-schedule",
        "confidence": "confirmed",
        "recorded_by": "test",
        "pct_supply": 2.1,
        # Pinned, not defaulted to now(): visibility depends on filing time, so a wall-clock
        # default would make these assertions drift with the calendar.
        "recorded_time_utc": "2023-03-16T00:00:00Z",
    }
    fields.update(overrides)
    return Event(**fields)


class TestEventValidation:
    def test_a_valid_event_gets_a_deterministic_id(self) -> None:
        assert unlock().event_id == unlock().event_id
        assert unlock().event_id != unlock(asset="OP").event_id

    def test_announcement_after_the_event_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="announced_time_utc"):
            unlock(announced_time_utc="2026-09-17T00:00:00Z")

    def test_naive_timestamps_are_rejected(self) -> None:
        with pytest.raises(ValueError, match="timezone"):
            unlock(event_time_utc="2026-09-16T13:00:00")

    def test_unknown_type_bad_confidence_and_bad_source_are_rejected(self) -> None:
        with pytest.raises(ValueError, match="event_type"):
            unlock(event_type="vibes")
        with pytest.raises(ValueError, match="confidence"):
            unlock(confidence="certain")
        with pytest.raises(ValueError, match="source_url"):
            unlock(source_url="trust me")
        with pytest.raises(ValueError, match="uppercase"):
            unlock(asset="arb")
        with pytest.raises(ValueError, match="pct_supply"):
            unlock(pct_supply=180.0)

    def test_market_wide_events_use_a_star_asset(self) -> None:
        event = unlock(event_type="macro_release", asset="*", pct_supply=None)
        assert event.asset == "*"


class TestEventStore:
    def store(self, tmp_path: Path) -> EventStore:
        return EventStore(tmp_path / "calendar.jsonl")

    def test_append_and_read_back(self, tmp_path: Path) -> None:
        store = self.store(tmp_path)
        event_id = store.append(unlock())
        assert [e.event_id for e in store.current()] == [event_id]

    def test_identical_refiling_is_idempotent(self, tmp_path: Path) -> None:
        store = self.store(tmp_path)
        first = unlock()
        store.append(first)
        store.append(first)  # an agent filing the same fact twice is not an error
        assert len(store.current()) == 1
        assert len(store.all_records()) == 1

    def test_conflicting_refiling_demands_a_supersession(self, tmp_path: Path) -> None:
        store = self.store(tmp_path)
        store.append(unlock(notional_usd=1_000_000.0))
        with pytest.raises(ValueError, match="supersedes"):
            store.append(unlock(notional_usd=2_000_000.0))

    def test_corrections_supersede_rather_than_edit(self, tmp_path: Path) -> None:
        store = self.store(tmp_path)
        original_id = store.append(unlock(notional_usd=1_000_000.0))
        correction = unlock(notional_usd=2_000_000.0, supersedes=original_id)
        assert correction.event_id != original_id, "a correction must not collide with its target"
        store.append(correction)

        current = store.current()
        assert len(current) == 1
        assert current[0].notional_usd == 2_000_000.0
        assert len(store.all_records()) == 2, "the wrong record is preserved, not erased"

    def test_a_two_step_correction_chain_resolves_to_the_latest(self, tmp_path: Path) -> None:
        store = self.store(tmp_path)
        first = store.append(unlock(notional_usd=1.0))
        second = store.append(unlock(notional_usd=2.0, supersedes=first))
        store.append(unlock(notional_usd=3.0, supersedes=second))
        current = store.current()
        assert len(current) == 1
        assert current[0].notional_usd == 3.0

    def test_superseding_a_nonexistent_record_is_rejected(self, tmp_path: Path) -> None:
        store = self.store(tmp_path)
        with pytest.raises(ValueError, match="does not exist"):
            store.append(unlock(supersedes="deadbeefdeadbeef"))

    def test_superseding_an_already_superseded_record_is_rejected(self, tmp_path: Path) -> None:
        """A fork has no single latest record, and the file cannot be edited afterwards.

        The original id is the one a human wrote down, so filing a second correction against it is
        the natural mistake. It must fail at ``append`` — once both lines are on disk, an
        append-only calendar has no legal way to remove either.
        """
        store = self.store(tmp_path)
        original = store.append(unlock(notional_usd=1.0))
        store.append(unlock(notional_usd=2.0, supersedes=original))

        with pytest.raises(ValueError, match="already superseded"):
            store.append(unlock(notional_usd=3.0, supersedes=original))

        current = store.current()
        assert len(current) == 1
        assert current[0].notional_usd == 2.0
        assert len(store.all_records()) == 2, "the rejected fork never reached the file"

    def test_current_terminates_on_a_forked_chain(self, tmp_path: Path) -> None:
        """A hand-edited calendar must not be able to hang the reader.

        ``append`` refuses to write a fork, but the file is plain text that a human can edit, and
        ``append`` itself reads before it writes — a reader that loops would brick every later
        write as well.
        """
        path = tmp_path / "calendar.jsonl"
        store = EventStore(path)
        original = store.append(unlock(notional_usd=1.0))
        store.append(unlock(notional_usd=2.0, supersedes=original))
        forked = unlock(notional_usd=3.0, supersedes=original)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(forked.as_dict(), sort_keys=True) + "\n")

        current = store.current()  # must return, not spin
        assert {event.notional_usd for event in current} == {2.0, 3.0}

    def test_an_event_is_invisible_until_it_is_filed(self, tmp_path: Path) -> None:
        """The look-ahead guard is the later of announcement and filing, not the announcement.

        Backfilling a calendar is the normal case: we learn about last month's unlock today. A
        backtest dated last month could not have conditioned on a record that did not exist yet,
        however early the announcement it describes.
        """
        store = self.store(tmp_path)
        store.append(
            unlock(
                announced_time_utc="2026-01-01T00:00:00Z",
                recorded_time_utc="2026-06-01T00:00:00Z",
            )
        )

        after_announcement = datetime(2026, 3, 1, tzinfo=UTC)
        after_filing = datetime(2026, 7, 1, tzinfo=UTC)
        assert store.visible_at(after_announcement) == [], "a record we had not filed yet"
        assert len(store.visible_at(after_filing)) == 1

    def test_visible_at_enforces_the_lookahead_guard(self, tmp_path: Path) -> None:
        store = self.store(tmp_path)
        store.append(unlock(announced_time_utc="2026-06-01T00:00:00Z"))

        before = datetime(2026, 5, 1, tzinfo=UTC)
        after = datetime(2026, 7, 1, tzinfo=UTC)
        assert store.visible_at(before) == []
        assert len(store.visible_at(after)) == 1
        with pytest.raises(ValueError, match="timezone-aware"):
            store.visible_at(datetime(2026, 7, 1))  # noqa: DTZ001 - the point of the test

    def test_upcoming_windows_on_event_time(self, tmp_path: Path) -> None:
        store = self.store(tmp_path)
        store.append(unlock(announced_time_utc="2023-03-16T00:00:00Z"))
        as_of = datetime(2026, 9, 1, tzinfo=UTC)
        assert len(store.upcoming(as_of, horizon_days=30.0)) == 1
        assert store.upcoming(as_of, horizon_days=5.0) == []
        after_the_event = datetime(2026, 10, 1, tzinfo=UTC)
        assert store.upcoming(after_the_event, horizon_days=30.0) == []

    def test_a_corrupt_line_fails_loudly_with_its_location(self, tmp_path: Path) -> None:
        path = tmp_path / "calendar.jsonl"
        store = EventStore(path)
        store.append(unlock())
        path.write_text(path.read_text() + "{not json}\n")
        with pytest.raises(ValueError, match="calendar.jsonl:2"):
            store.all_records()

    def test_missing_file_reads_as_empty(self, tmp_path: Path) -> None:
        assert self.store(tmp_path).current() == []
