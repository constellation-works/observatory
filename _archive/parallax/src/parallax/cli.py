"""Command-line entry point for Parallax."""

from __future__ import annotations

import argparse
import re
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from parallax import __version__

CRYPTO_DATA_ROOT = Path("data/R01-crypto")
CONSUMER_GOODS_DATA_ROOT = Path("data/R03-consumer-goods")
RESEARCH_SLUG = re.compile(r"R\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="parallax",
        description="Run falsifiable, reproducible research across numbered domains.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("doctor", help="show the scaffold's operating safety posture")

    data = subparsers.add_parser("data", help="manage public market data")
    data_commands = data.add_subparsers(dest="data_command", required=True)
    fetch = data_commands.add_parser("fetch", help="backfill public one-minute candles")
    fetch.add_argument("--venue", choices=("binance", "coinbase"), required=True)
    fetch.add_argument("--symbol", required=True, help="BTCUSDT on Binance; BTC-USD on Coinbase")
    fetch.add_argument("--start", required=True, help="inclusive UTC date, YYYY-MM-DD")
    fetch.add_argument("--end", required=True, help="exclusive UTC date, YYYY-MM-DD")
    fetch.add_argument("--output", type=Path, default=CRYPTO_DATA_ROOT / "raw/candles")
    fetch.add_argument("--pause-seconds", type=float, default=0.1)

    book = subparsers.add_parser("book", help="capture and study level-2 order book data")
    book_commands = book.add_subparsers(dest="book_command", required=True)

    record = book_commands.add_parser("record", help="capture live depth diffs and trades")
    record.add_argument("--symbol", default="BTCUSDT")
    record.add_argument(
        "--market",
        choices=("spot", "futures"),
        default="spot",
        help="futures adds forceOrder (liquidations) and markPrice@1s (funding) streams",
    )
    record.add_argument("--output", type=Path, default=CRYPTO_DATA_ROOT / "raw/book")
    record.add_argument("--snapshot-seconds", type=float, default=300.0)
    record.add_argument("--depth-limit", type=int, default=None)
    record.add_argument(
        "--streams",
        default=None,
        help=(
            "comma-separated stream suffixes overriding the market default, e.g. "
            "'aggTrade,bookTicker,forceOrder,markPrice@1s' for a disk-light futures "
            "capture without the depth feed"
        ),
    )

    build = book_commands.add_parser("build", help="reconstruct the book into a feature table")
    build.add_argument("--symbol", default="BTCUSDT")
    build.add_argument("--market", choices=("spot", "futures"), default="spot")
    build.add_argument("--input", type=Path, default=CRYPTO_DATA_ROOT / "raw/book")
    build.add_argument(
        "--output", type=Path, default=CRYPTO_DATA_ROOT / "processed/book_features.parquet"
    )
    build.add_argument("--sample-seconds", type=float, default=1.0)

    sweep = book_commands.add_parser("sweep", help="measure predictability decay against cost")
    sweep.add_argument(
        "--input", type=Path, default=CRYPTO_DATA_ROOT / "processed/book_features.parquet"
    )
    sweep.add_argument(
        "--round-trip-cost-bps",
        type=float,
        required=True,
        help="measured round-trip cost; use parallax.crypto.costs.MeasuredCostModel, not a guess",
    )
    sweep.add_argument("--train-fraction", type=float, default=0.7)
    sweep.add_argument("--sample-seconds", type=float, default=1.0)
    sweep.add_argument(
        "--execution-lag-s",
        type=float,
        default=None,
        help="delay between the last observation used and the traded price "
        "(default: one sample); 0 measures an untradeable signal and is a sensitivity check only",
    )
    sweep.add_argument("--json", action="store_true", help="emit machine-readable results")

    impact = book_commands.add_parser(
        "impact", help="fit the scaling exponents of price response to flow and depth"
    )
    impact.add_argument(
        "--input", type=Path, default=CRYPTO_DATA_ROOT / "processed/book_features.parquet"
    )
    impact.add_argument("--sample-seconds", type=float, default=1.0)
    impact.add_argument("--depth-band", default="25", help="depth band in bps, e.g. 10, 25, 50")
    impact.add_argument("--json", action="store_true", help="emit machine-readable results")

    revelation = book_commands.add_parser(
        "revelation", help="test whether impact is mechanical flow or maker withdrawal"
    )
    revelation.add_argument(
        "--input", type=Path, default=CRYPTO_DATA_ROOT / "processed/book_features.parquet"
    )
    revelation.add_argument("--window-seconds", type=float, default=5.0)
    revelation.add_argument("--max-lag-seconds", type=float, default=30.0)
    revelation.add_argument("--sample-seconds", type=float, default=1.0)
    revelation.add_argument("--json", action="store_true", help="emit machine-readable results")

    journal = subparsers.add_parser("journal", help="use the append-only trade journal")
    journal.add_argument("--db", type=Path, default=CRYPTO_DATA_ROOT / "journal.sqlite3")
    journal_commands = journal.add_subparsers(dest="journal_command", required=True)
    preregister = journal_commands.add_parser("preregister", help="freeze a trade thesis")
    preregister.add_argument("--hypothesis", required=True)
    preregister.add_argument("--entry-rule", required=True)
    preregister.add_argument("--exit-rule", required=True)
    preregister.add_argument("--invalidation", required=True)
    preregister.add_argument("--size", required=True)
    preregister.add_argument("--expected-edge-bps", type=float, required=True)
    close = journal_commands.add_parser("close", help="append the observed outcome")
    close.add_argument("trade_id")
    close.add_argument("--fill", required=True)
    close.add_argument("--fees", required=True)
    close.add_argument("--slippage-bps", type=float, required=True)
    close.add_argument("--result", required=True)
    show = journal_commands.add_parser("show", help="show one preregistration and its outcome")
    show.add_argument("trade_id")

    research = subparsers.add_parser("research", help="use the domain-neutral research journal")
    research.add_argument(
        "--db",
        type=Path,
        default=None,
        help="override the default data/<research-slug>/research.sqlite3 journal",
    )
    research_commands = research.add_subparsers(dest="research_command", required=True)
    research_preregister = research_commands.add_parser(
        "preregister", help="freeze a research question and evaluation contract"
    )
    research_preregister.add_argument(
        "--domain",
        "--venture",
        dest="venture",
        required=True,
        help="numbered research domain, e.g. R02-language-models (--venture is a legacy alias)",
    )
    research_preregister.add_argument("--question", required=True)
    research_preregister.add_argument("--hypothesis", required=True)
    research_preregister.add_argument("--baseline", required=True)
    research_preregister.add_argument("--method", required=True)
    research_preregister.add_argument("--metric", required=True)
    research_preregister.add_argument("--invalidation", required=True)
    research_preregister.add_argument("--data-cutoff", required=True)
    research_close = research_commands.add_parser("close", help="append the observed outcome")
    research_close.add_argument(
        "--domain",
        "--venture",
        dest="venture",
        help="numbered research domain; required when --db is omitted",
    )
    research_close.add_argument("experiment_id")
    research_close.add_argument("--summary", required=True)
    research_close.add_argument(
        "--decision", choices=("reject", "revise", "advance"), required=True
    )
    research_close.add_argument("--artifacts", required=True)
    research_close.add_argument("--limitations", required=True)
    research_show = research_commands.add_parser(
        "show", help="show one research preregistration and its outcome"
    )
    research_show.add_argument(
        "--domain",
        "--venture",
        dest="venture",
        help="numbered research domain; required when --db is omitted",
    )
    research_show.add_argument("experiment_id")

    consumer_goods = subparsers.add_parser(
        "consumer-goods", help="collect and study consumer search-attention proxies"
    )
    consumer_goods_commands = consumer_goods.add_subparsers(
        dest="consumer_goods_command", required=True
    )
    import_history = consumer_goods_commands.add_parser(
        "import-history", help="preserve one immutable historical Google Trends dataset"
    )
    import_history.add_argument(
        "--output", type=Path, default=CONSUMER_GOODS_DATA_ROOT / "raw/history"
    )
    import_history.add_argument(
        "--date", dest="snapshot_date", type=_iso_date, default=None, help="import date, YYYY-MM-DD"
    )
    import_history.add_argument(
        "--google-trends-file",
        type=Path,
        required=True,
        help="official pilot Google Trends CSV export",
    )
    pilot = consumer_goods_commands.add_parser(
        "pilot", help="run the preregistered E01 wearable log-ratio experiment"
    )
    pilot.add_argument(
        "--history-root",
        type=Path,
        default=CONSUMER_GOODS_DATA_ROOT / "raw/history",
        help="immutable import history; the latest snapshot is used unless --snapshot is given",
    )
    pilot.add_argument("--snapshot", default=None, help="snapshot date, YYYY-MM-DD")
    pilot.add_argument(
        "--input",
        type=Path,
        default=None,
        help="bypass the manifest and read a loose CSV; the result is then unpinned",
    )
    pilot.add_argument("--as-of", type=_iso_date, default=None)
    pilot.add_argument("--bootstrap-samples", type=int, default=2_000)
    pilot.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/R03-consumer-goods/E01-pilot.json"),
    )

    reset_panel = consumer_goods_commands.add_parser(
        "reset-panel",
        help="align staple attention on the post-Thanksgiving reset and calibrate it",
    )
    reset_panel.add_argument(
        "--input", type=Path, default=CONSUMER_GOODS_DATA_ROOT / "raw/multiTimeline_staple.csv"
    )
    reset_panel.add_argument("--low-week", type=int, default=-4)
    reset_panel.add_argument("--high-week", type=int, default=8)
    reset_panel.add_argument("--first-year", type=int, default=2021)
    reset_panel.add_argument("--last-year", type=int, default=2025)
    reset_panel.add_argument("--json", action="store_true", help="emit machine-readable results")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        print("mode: research")
        print("research_domains: extensible")
        print("crypto_benchmark: bitcoin buy-and-hold")
        print("crypto_signal_execution: next observation")
        print("live_actions: disabled")
        print("live_trading: disabled")
        return 0
    if args.command == "data" and args.data_command == "fetch":
        from parallax.crypto.data.candles import write_candle_stream
        from parallax.crypto.data.sources import BinanceKlines, CoinbaseCandles

        source_class = BinanceKlines if args.venue == "binance" else CoinbaseCandles
        source = source_class(pause_seconds=args.pause_seconds)
        start_ms = _date_ms(args.start)
        end_ms = _date_ms(args.end)
        summary = write_candle_stream(
            args.output,
            source.pages(args.symbol, start_ms, end_ms),
            expected_start_ms=start_ms,
            expected_end_ms=end_ms,
        )
        print(f"rows: {summary.rows}")
        print(f"files: {len(summary.files)}")
        print(f"missing_minutes: {summary.missing_minutes}")
        return 0
    if args.command == "book":
        return _run_book(args)
    if args.command == "journal":
        from parallax.crypto.journal import TradeIntent, TradeJournal, TradeOutcome

        journal = TradeJournal(args.db)
        if args.journal_command == "preregister":
            trade_id = journal.preregister(
                TradeIntent(
                    hypothesis=args.hypothesis,
                    entry_rule=args.entry_rule,
                    exit_rule=args.exit_rule,
                    invalidation=args.invalidation,
                    size=args.size,
                    expected_edge_bps=args.expected_edge_bps,
                )
            )
            print(trade_id)
            return 0
        if args.journal_command == "close":
            journal.record_outcome(
                args.trade_id,
                TradeOutcome(
                    fill=args.fill,
                    fees=args.fees,
                    slippage_bps=args.slippage_bps,
                    result=args.result,
                ),
            )
            print(args.trade_id)
            return 0
        if args.journal_command == "show":
            import json

            print(json.dumps(journal.get(args.trade_id), indent=2, sort_keys=True))
            return 0
    if args.command == "research":
        import json

        from parallax.research import ResearchIntent, ResearchJournal, ResearchOutcome

        journal = ResearchJournal(_research_database_path(args))
        if args.research_command == "preregister":
            experiment_id = journal.preregister(
                ResearchIntent(
                    venture=args.venture,
                    question=args.question,
                    hypothesis=args.hypothesis,
                    baseline=args.baseline,
                    method=args.method,
                    primary_metric=args.metric,
                    invalidation=args.invalidation,
                    data_cutoff=args.data_cutoff,
                )
            )
            print(experiment_id)
            return 0
        if args.research_command == "close":
            journal.record_outcome(
                args.experiment_id,
                ResearchOutcome(
                    summary=args.summary,
                    decision=args.decision,
                    artifacts=args.artifacts,
                    limitations=args.limitations,
                ),
            )
            print(args.experiment_id)
            return 0
        if args.research_command == "show":
            print(json.dumps(journal.get(args.experiment_id), indent=2, sort_keys=True))
            return 0
    if args.command == "consumer-goods" and args.consumer_goods_command == "import-history":
        from parallax.consumer_goods.data import import_historical_snapshot

        summary = import_historical_snapshot(
            args.output,
            snapshot_date=args.snapshot_date,
            google_trends_file=args.google_trends_file,
        )
        print(f"snapshot: {summary.snapshot}")
        print(f"files: {len(summary.files)}")
        print(f"created: {str(summary.created).lower()}")
        return 0
    if args.command == "consumer-goods" and args.consumer_goods_command == "pilot":
        import json

        from parallax.consumer_goods.data.history import resolve_pilot_source
        from parallax.consumer_goods.pilot import run_pilot

        if args.input is not None:
            source = args.input
            print(f"warning: reading {source} directly; this result is not pinned to a snapshot")
        else:
            try:
                source = resolve_pilot_source(args.history_root, args.snapshot)
            except (FileNotFoundError, ValueError) as error:
                print(f"error: {error}")
                return 1

        result = run_pilot(
            source,
            as_of=args.as_of,
            bootstrap_samples=args.bootstrap_samples,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n")
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        print(f"artifact: {args.output}")
        return 0
    if args.command == "consumer-goods" and args.consumer_goods_command == "reset-panel":
        import json

        from parallax.consumer_goods.reset_panel import (
            build_panel,
            calibrate_against_placebo_calendars,
            format_calibrations,
            load_staple_history,
            panel_extrema,
            reset_anchor,
            week_over_week_log_change,
        )

        history = load_staple_history(args.input)
        change_dates, change = week_over_week_log_change(history)
        anchors = [reset_anchor(year) for year in range(args.first_year, args.last_year + 1)]
        panel = build_panel(change_dates, change, anchors, args.low_week, args.high_week)
        extrema = panel_extrema(panel, history.terms, args.low_week)
        try:
            calibrations = calibrate_against_placebo_calendars(
                change_dates, change, history.terms, anchors, args.low_week, args.high_week
            )
        except ValueError as error:
            print(f"error: {error}")
            return 1

        if args.json:
            print(
                json.dumps(
                    {
                        "extrema": [vars(item) for item in extrema],
                        "calibration": [
                            {**vars(item), "p_value": item.p_value} for item in calibrations
                        ],
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            for item in extrema:
                print(
                    f"{item.term:>8} week {item.relative_week:>+3d} "
                    f"{item.mean_change:>+8.3f}  {item.years_agreeing}/{item.years_observed} agree"
                )
            print()
            print(format_calibrations(calibrations))
            print()
            print(
                "p is the share of shifted calendars reaching the same statistic; it says the "
                "week is unlike other weeks, not that the cause is a reset rather than a holiday."
            )
        return 0
    raise AssertionError(f"unhandled command: {args.command}")


def _iso_date(value: str):
    from datetime import date

    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("expected YYYY-MM-DD") from error


def _run_book(args: argparse.Namespace) -> int:
    if args.book_command == "record":
        import asyncio

        from parallax.crypto.microstructure.record import CaptureConfig, run_capture

        suffixes = None
        if args.streams:
            suffixes = tuple(part.strip() for part in args.streams.split(",") if part.strip())
        config = CaptureConfig(
            symbol=args.symbol,
            root=args.output,
            market=args.market,
            stream_suffixes=suffixes,
            depth_limit=args.depth_limit,
            snapshot_seconds=args.snapshot_seconds,
        )
        print(f"capturing {config.capture_label} to {config.root / config.capture_label}")
        print("stop with ctrl-c; every gap is written into the capture")
        lines = asyncio.run(run_capture(config))
        print(f"lines: {lines}")
        return 0

    if args.book_command == "build":
        from parallax.crypto.microstructure.pipeline import build_features
        from parallax.crypto.microstructure.record import capture_paths

        paths = capture_paths(args.input, args.symbol, args.market)
        if not paths:
            print(f"no capture files for {args.symbol.upper()} ({args.market}) under {args.input}")
            return 1
        summary = build_features(paths, args.output, sample_seconds=args.sample_seconds)
        for key, value in summary.as_dict().items():
            print(f"{key}: {value}")
        return 0

    if args.book_command == "sweep":
        import json

        from parallax.crypto.microstructure.horizon import (
            DEFAULT_EXECUTION_LAG_S,
            format_results,
            load_feature_table,
            sweep,
        )

        columns = load_feature_table(args.input)
        results = sweep(
            columns,
            round_trip_cost_bps=args.round_trip_cost_bps,
            train_fraction=args.train_fraction,
            sample_seconds=args.sample_seconds,
            execution_lag_s=(
                DEFAULT_EXECUTION_LAG_S if args.execution_lag_s is None else args.execution_lag_s
            ),
        )
        if not results:
            print("not enough rows to evaluate any horizon")
            return 1
        if args.json:
            print(json.dumps([result.as_dict() for result in results], indent=2))
        else:
            print(format_results(results))
        return 0

    if args.book_command == "impact":
        import json

        from parallax.crypto.microstructure.horizon import load_feature_table
        from parallax.crypto.microstructure.impact import format_fits, sweep_windows

        columns = load_feature_table(args.input)
        fits = sweep_windows(
            columns, sample_seconds=args.sample_seconds, depth_band=args.depth_band
        )
        if not fits:
            print("not enough windows to fit any scaling law")
            return 1
        if args.json:
            print(json.dumps([fit.as_dict() for fit in fits], indent=2))
        else:
            print(format_fits(fits))
            print()
            print("delta 1.0 = naive flow/depth and Kyle; delta 0.5 = the square-root law.")
            print("gamma spanning 0 means resting depth does no work and resistance is not")
            print("separately identified. This is contemporaneous impact, not a forecast.")
        return 0

    if args.book_command == "revelation":
        import json

        from parallax.crypto.microstructure.horizon import load_feature_table
        from parallax.crypto.microstructure.revelation import (
            decompose_trade_coincidence,
            detection_profile,
            format_revelation,
            withdrawal_amplification,
        )

        columns = load_feature_table(args.input)
        coincidence = decompose_trade_coincidence(columns)
        amplification = withdrawal_amplification(
            columns, window_s=args.window_seconds, sample_seconds=args.sample_seconds
        )
        detection = detection_profile(
            columns, sample_seconds=args.sample_seconds, max_lag_s=args.max_lag_seconds
        )
        if args.json:
            print(
                json.dumps(
                    {
                        "trade_coincidence": coincidence.as_dict(),
                        "withdrawal_amplification": (
                            amplification.as_dict() if amplification else None
                        ),
                        "detection": detection.as_dict() if detection else None,
                    },
                    indent=2,
                )
            )
        else:
            print(format_revelation(coincidence, amplification, detection))
        return 0

    raise AssertionError(f"unhandled book command: {args.book_command}")


def _date_ms(value: str) -> int:
    parsed = datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=UTC)
    return int(parsed.timestamp() * 1_000)


def _research_database_path(args: argparse.Namespace) -> Path:
    if args.db is not None:
        return args.db
    domain = getattr(args, "venture", None)
    if not domain:
        raise SystemExit("research close/show requires --domain when --db is omitted")
    if not RESEARCH_SLUG.fullmatch(domain):
        raise SystemExit("research domain must match R<NN>-<lowercase-kebab-title>")
    return Path("data") / domain / "research.sqlite3"


if __name__ == "__main__":
    raise SystemExit(main())
