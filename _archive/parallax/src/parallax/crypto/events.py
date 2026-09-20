"""The event calendar: scheduled mechanical-flow events with announced-time discipline.

Schema and rationale: ``docs/research/R01-crypto/EVENTS.md``. The load-bearing rule is that every
event records when it became publicly knowable (``announced_time_utc``), and experiments may
condition on it only from that moment (:meth:`EventStore.visible_at`). The store is append-only
JSON lines; wrong records are superseded, never edited, so the calendar preserves what was believed
and when.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

EVENT_TYPES = frozenset(
    {
        "token_unlock",
        "options_expiry",
        "futures_expiry",
        "funding_settlement",
        "index_rebalance",
        "exchange_listing",
        "exchange_delisting",
        "network_upgrade",
        "macro_release",
        "etf_flow_publication",
        "other",
    }
)

CONFIDENCE_LEVELS = frozenset({"confirmed", "estimated", "rumored"})

DEFAULT_CALENDAR = Path("events/calendar.jsonl")


@dataclass(frozen=True)
class Event:
    """One scheduled event. Validation happens at construction; invalid events cannot exist."""

    event_type: str
    asset: str
    event_time_utc: str
    announced_time_utc: str
    source_url: str
    confidence: str
    recorded_by: str
    venue: str = ""
    notional_usd: float | None = None
    pct_supply: float | None = None
    notes: str = ""
    supersedes: str = ""
    recorded_time_utc: str = ""
    event_id: str = field(default="", compare=False)

    def __post_init__(self) -> None:
        if self.event_type not in EVENT_TYPES:
            raise ValueError(
                f"unknown event_type {self.event_type!r}; see docs/research/R01-crypto/EVENTS.md"
            )
        if self.confidence not in CONFIDENCE_LEVELS:
            raise ValueError(f"confidence must be one of {sorted(CONFIDENCE_LEVELS)}")
        if not self.asset or (self.asset != "*" and not self.asset.isalnum()):
            raise ValueError("asset must be an alphanumeric ticker or '*'")
        if self.asset != self.asset.upper():
            raise ValueError("asset must be uppercase")
        if not self.source_url.startswith(("http://", "https://")):
            raise ValueError("source_url must be a verifiable http(s) link")
        if not self.recorded_by:
            raise ValueError("recorded_by is required")

        event_time = _parse_utc(self.event_time_utc, "event_time_utc")
        announced = _parse_utc(self.announced_time_utc, "announced_time_utc")
        if announced > event_time:
            raise ValueError("announced_time_utc must not be after event_time_utc")
        if self.notional_usd is not None and self.notional_usd < 0.0:
            raise ValueError("notional_usd must be non-negative")
        if self.pct_supply is not None and not 0.0 <= self.pct_supply <= 100.0:
            raise ValueError("pct_supply must be within [0, 100]")

        if not self.recorded_time_utc:
            object.__setattr__(self, "recorded_time_utc", _now_iso())
        else:
            _parse_utc(self.recorded_time_utc, "recorded_time_utc")
        if not self.event_id:
            object.__setattr__(self, "event_id", self._derive_id())

    def _derive_id(self) -> str:
        key = "|".join((self.event_type, self.asset, self.venue, self.event_time_utc))
        if self.supersedes:
            # A correction must not collide with the record it corrects, or it would appear to
            # supersede itself; salt its id with the corrected content.
            content = json.dumps(
                {
                    "supersedes": self.supersedes,
                    "announced": self.announced_time_utc,
                    "source": self.source_url,
                    "confidence": self.confidence,
                    "notional": self.notional_usd,
                    "pct": self.pct_supply,
                    "notes": self.notes,
                },
                sort_keys=True,
            )
            key = f"{key}|{content}"
        return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]

    @property
    def event_time(self) -> datetime:
        return _parse_utc(self.event_time_utc, "event_time_utc")

    @property
    def announced_time(self) -> datetime:
        return _parse_utc(self.announced_time_utc, "announced_time_utc")

    @property
    def recorded_time(self) -> datetime:
        return _parse_utc(self.recorded_time_utc, "recorded_time_utc")

    @property
    def visible_time(self) -> datetime:
        """The instant this event became usable: the later of announcement and filing.

        A record we file today about an announcement from last month was not available to a
        backtest running last month, however early the announcement itself was.
        """
        return max(self.announced_time, self.recorded_time)

    def as_dict(self) -> dict[str, object]:
        return {k: v for k, v in asdict(self).items() if v not in (None, "")}


class EventStore:
    """Append-only JSONL calendar with supersession resolution and point-in-time queries."""

    def __init__(self, path: Path = DEFAULT_CALENDAR) -> None:
        self.path = Path(path)

    def append(self, event: Event) -> str:
        """Append one validated event. Re-filing an identical live event is rejected.

        Corrections must target the *current* record of a chain. Two records correcting the same
        already-superseded id would fork the chain, and a fork has no single latest record — so it
        is rejected here, before it reaches an append-only file that cannot be edited afterwards.
        """
        records = self.all_records()
        known = {e.event_id for e in records}
        superseded = _superseded_ids(records)
        current = {e.event_id: e for e in _resolve_current(records)}

        if event.event_id in current and not event.supersedes:
            existing = current[event.event_id]
            if existing.as_dict() == event.as_dict():
                return event.event_id  # idempotent re-file
            raise ValueError(
                f"event {event.event_id} already exists; append a correction with "
                f"supersedes={event.event_id!r} instead of re-filing"
            )
        if event.supersedes:
            if event.supersedes == event.event_id:
                raise ValueError(f"event {event.event_id} cannot supersede itself")
            if event.supersedes not in known:
                raise ValueError(f"supersedes target {event.supersedes!r} does not exist")
            if event.supersedes in superseded:
                replacement = next(
                    (r.event_id for r in records if r.supersedes == event.supersedes), ""
                )
                raise ValueError(
                    f"supersedes target {event.supersedes!r} was already superseded by "
                    f"{replacement!r}; correct the current record instead"
                )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.as_dict(), sort_keys=True) + "\n")
        return event.event_id

    def all_records(self) -> list[Event]:
        """Every record ever written, including superseded ones, in file order."""
        if not self.path.exists():
            return []
        records: list[Event] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(Event(**json.loads(line)))
                except (json.JSONDecodeError, TypeError, ValueError) as error:
                    raise ValueError(
                        f"{self.path}:{line_number}: invalid record: {error}"
                    ) from error
        return records

    def current(self) -> list[Event]:
        """Latest record of each supersession chain, in event-time order."""
        return sorted(_resolve_current(self.all_records()), key=lambda r: r.event_time_utc)

    def visible_at(self, as_of: datetime) -> list[Event]:
        """Events an experiment may condition on at ``as_of`` — the look-ahead guard.

        Both the announcement and the *filing* must precede ``as_of``: an event we recorded
        yesterday about last month is still invisible to a backtest running before we filed it,
        unless its announcement time is trusted and earlier. The conservative rule used here is
        the later of the two.
        """
        if as_of.tzinfo is None:
            raise ValueError("as_of must be timezone-aware")
        return [event for event in self.current() if event.visible_time <= as_of]

    def upcoming(self, as_of: datetime, horizon_days: float = 30.0) -> list[Event]:
        """Announced-and-pending events within the horizon, for the monitoring loop."""
        visible = self.visible_at(as_of)
        return [
            event
            for event in visible
            if 0.0 <= (event.event_time - as_of).total_seconds() <= horizon_days * 86_400.0
        ]


def _superseded_ids(records: list[Event]) -> set[str]:
    """Ids that some later record corrects, and which are therefore no longer current."""
    return {record.supersedes for record in records if record.supersedes}


def _resolve_current(records: list[Event]) -> list[Event]:
    """The records nothing has corrected, in file order.

    Supersession chains are kept linear by :meth:`EventStore.append`, so a chain's live record is
    simply the one no other record names. This is a single pass over the file with no chain walk:
    a malformed or hand-edited calendar can never make it loop.
    """
    superseded = _superseded_ids(records)
    by_id: dict[str, Event] = {}
    for record in records:
        by_id[record.event_id] = record  # an identical re-file collapses onto itself
    return [record for record in by_id.values() if record.event_id not in superseded]


def _parse_utc(value: str, name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{name} must be ISO-8601, got {value!r}") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{name} must carry an explicit timezone (use Z)")
    return parsed.astimezone(UTC)


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
