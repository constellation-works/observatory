"""Append-only preregistration and outcome journal for any numbered research domain."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True)
class ResearchIntent:
    """The claim and evaluation contract frozen before an experiment runs."""

    venture: str
    question: str
    hypothesis: str
    baseline: str
    method: str
    primary_metric: str
    invalidation: str
    data_cutoff: str


@dataclass(frozen=True)
class ResearchOutcome:
    """The observed result appended without changing the original intent."""

    summary: str
    decision: str
    artifacts: str
    limitations: str


class ResearchJournal:
    """SQLite journal with immutable intents and append-only outcomes."""

    _decisions = frozenset({"reject", "revise", "advance"})

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def preregister(self, intent: ResearchIntent) -> str:
        for field_name in (
            "venture",
            "question",
            "hypothesis",
            "baseline",
            "method",
            "primary_metric",
            "invalidation",
            "data_cutoff",
        ):
            _require_text(getattr(intent, field_name), field_name)

        experiment_id = uuid4().hex
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO research_intents (
                    id, created_at, venture, question, hypothesis, baseline, method,
                    primary_metric, invalidation, data_cutoff
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    experiment_id,
                    _now(),
                    intent.venture,
                    intent.question,
                    intent.hypothesis,
                    intent.baseline,
                    intent.method,
                    intent.primary_metric,
                    intent.invalidation,
                    intent.data_cutoff,
                ),
            )
        return experiment_id

    def record_outcome(self, experiment_id: str, outcome: ResearchOutcome) -> None:
        for field_name in ("summary", "decision", "artifacts", "limitations"):
            _require_text(getattr(outcome, field_name), field_name)
        if outcome.decision not in self._decisions:
            choices = ", ".join(sorted(self._decisions))
            raise ValueError(f"decision must be one of: {choices}")

        with self._connect() as connection:
            exists = connection.execute(
                "SELECT 1 FROM research_intents WHERE id = ?", (experiment_id,)
            ).fetchone()
            if exists is None:
                raise KeyError(f"unknown experiment id: {experiment_id}")
            connection.execute(
                """
                INSERT INTO research_outcomes (
                    experiment_id, recorded_at, summary, decision, artifacts, limitations
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    experiment_id,
                    _now(),
                    outcome.summary,
                    outcome.decision,
                    outcome.artifacts,
                    outcome.limitations,
                ),
            )

    def get(self, experiment_id: str) -> dict[str, object]:
        with self._connect() as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute(
                """
                SELECT i.*, o.recorded_at, o.summary, o.decision, o.artifacts, o.limitations
                FROM research_intents AS i
                LEFT JOIN research_outcomes AS o ON o.experiment_id = i.id
                WHERE i.id = ?
                """,
                (experiment_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"unknown experiment id: {experiment_id}")
        return dict(row)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS research_intents (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    venture TEXT NOT NULL,
                    question TEXT NOT NULL,
                    hypothesis TEXT NOT NULL,
                    baseline TEXT NOT NULL,
                    method TEXT NOT NULL,
                    primary_metric TEXT NOT NULL,
                    invalidation TEXT NOT NULL,
                    data_cutoff TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS research_outcomes (
                    experiment_id TEXT PRIMARY KEY REFERENCES research_intents(id),
                    recorded_at TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    decision TEXT NOT NULL CHECK (decision IN ('reject', 'revise', 'advance')),
                    artifacts TEXT NOT NULL,
                    limitations TEXT NOT NULL
                );

                CREATE TRIGGER IF NOT EXISTS research_intents_no_update
                BEFORE UPDATE ON research_intents
                BEGIN
                    SELECT RAISE(ABORT, 'research preregistrations are immutable');
                END;

                CREATE TRIGGER IF NOT EXISTS research_intents_no_delete
                BEFORE DELETE ON research_intents
                BEGIN
                    SELECT RAISE(ABORT, 'research preregistrations are immutable');
                END;

                CREATE TRIGGER IF NOT EXISTS research_outcomes_no_update
                BEFORE UPDATE ON research_outcomes
                BEGIN
                    SELECT RAISE(ABORT, 'research outcomes are append-only');
                END;

                CREATE TRIGGER IF NOT EXISTS research_outcomes_no_delete
                BEFORE DELETE ON research_outcomes
                BEGIN
                    SELECT RAISE(ABORT, 'research outcomes are append-only');
                END;
                """
            )


def _now() -> str:
    return datetime.now(tz=UTC).isoformat()


def _require_text(value: str, name: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must not be empty")
