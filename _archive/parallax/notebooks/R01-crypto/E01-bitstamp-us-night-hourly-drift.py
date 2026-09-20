"""E01 methodology: Bitstamp US night hourly drift (H08).

Exploratory (`preregistered: false`). Frozen after the tape was already opened.
Run from the Parallax repo:

    uv run python notebooks/R01-crypto/E01-bitstamp-us-night-hourly-drift.py
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from math import erfc
from pathlib import Path

import numpy as np
import pandas as pd

# --- frozen identity ---
RESEARCH_ID = "R01"
HYPOTHESIS_ID = "H08"
EXPERIMENT_ID = "E01"
PREREGISTERED = False
KAGGLE_HANDLE = "mczielinski/bitcoin-historical-data"
KAGGLE_VERSION = "685"
SOURCE_FILE = "btcusd_1-min_data.csv"
EXPECTED_SHA256 = "7cc5764ca4307d0ed90400f0c1331fa1154c04f8a40187796e8ef6625a6dfece"
WINDOW_START_UTC = datetime(2026, 4, 1, tzinfo=timezone.utc)
PRIOR_HOUR_UTC = datetime(2026, 3, 31, 23, 0, tzinfo=timezone.utc)
NIGHT_HOURS = (21, 22, 23)
CASH_CLOSE_HOUR_ET = 16
BOOTSTRAP_DRAWS = 8_000
BOOTSTRAP_SEED = 7
ANNUALIZATION_HOURS = 365.25 * 24


def repo_root() -> Path:
    here = Path.cwd().resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "docs/research/R01-crypto"
        ).is_dir():
            return candidate
    raise SystemExit("run from the Parallax repository")


def resolve_source_csv() -> tuple[Path, dict]:
    binary = shutil.which("datasets") or str(Path.home() / ".local/bin/datasets")
    meta = json.loads(subprocess.check_output([binary, "json", KAGGLE_HANDLE], text=True))
    version = str(meta["version"])
    if version != KAGGLE_VERSION:
        raise SystemExit(f"expected Kaggle version {KAGGLE_VERSION}, found {version}")
    csv_path = Path(meta["local"]["resolved_path"]) / SOURCE_FILE
    if not csv_path.is_file():
        raise SystemExit(f"missing source file: {csv_path}")
    return csv_path, meta


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_minutes(csv_path: Path) -> pd.DataFrame:
    start_ts = int(PRIOR_HOUR_UTC.timestamp())
    chunks = []
    for chunk in pd.read_csv(
        csv_path,
        usecols=["Timestamp", "Open", "High", "Low", "Close", "Volume"],
        dtype={
            "Timestamp": "int64",
            "Open": "float64",
            "High": "float64",
            "Low": "float64",
            "Close": "float64",
            "Volume": "float64",
        },
        chunksize=400_000,
    ):
        sub = chunk.loc[chunk["Timestamp"] >= start_ts]
        if not sub.empty:
            chunks.append(sub)
    if not chunks:
        raise SystemExit("no 1-minute rows in the observation window")
    minutes = (
        pd.concat(chunks, ignore_index=True)
        .sort_values("Timestamp")
        .drop_duplicates("Timestamp", keep="last")
        .reset_index(drop=True)
    )
    minutes["dt"] = pd.to_datetime(minutes["Timestamp"], unit="s", utc=True)
    return minutes


def validate_minutes(minutes: pd.DataFrame) -> dict[str, int | float]:
    in_window = minutes.loc[minutes["dt"] >= WINDOW_START_UTC]
    expected = pd.date_range(in_window["dt"].iloc[0], in_window["dt"].iloc[-1], freq="min", tz="UTC")
    ohlc_bad = (
        (in_window["High"] < in_window[["Open", "Close"]].max(axis=1))
        | (in_window["Low"] > in_window[["Open", "Close"]].min(axis=1))
    )
    return {
        "rows": int(len(in_window)),
        "nulls": int(in_window.isna().sum().sum()),
        "missing_minutes": int(len(expected) - len(in_window)),
        "high_lt_low": int((in_window["High"] < in_window["Low"]).sum()),
        "nonpositive_close": int((in_window["Close"] <= 0).sum()),
        "ohlc_inconsistent": int(ohlc_bad.sum()),
        "zero_volume": int((in_window["Volume"] == 0).sum()),
    }


def hourly_bars(minutes: pd.DataFrame) -> pd.DataFrame:
    minutes = minutes.copy()
    minutes["hour"] = minutes["dt"].dt.floor("h")
    hourly = minutes.groupby("hour", sort=True).agg(
        open=("Open", "first"),
        high=("High", "max"),
        low=("Low", "min"),
        close=("Close", "last"),
        volume=("Volume", "sum"),
        n_minutes=("Close", "size"),
    )
    hourly = hourly.loc[hourly.index >= WINDOW_START_UTC].copy()
    hourly["ret"] = hourly["close"].pct_change()
    hourly["log_ret"] = np.log(hourly["close"] / hourly["close"].shift(1))
    hourly["pt"] = hourly.index.tz_convert("America/Los_Angeles")
    hourly["et"] = hourly.index.tz_convert("America/New_York")
    hourly["hour_pt"] = hourly["pt"].dt.hour
    hourly["hour_et"] = hourly["et"].dt.hour
    hourly["is_weekend_et"] = hourly["et"].dt.dayofweek >= 5
    return hourly


def welch_t_less(a: pd.Series, b: pd.Series) -> tuple[float, float]:
    a_v = np.asarray(a.dropna(), float)
    b_v = np.asarray(b.dropna(), float)
    se = np.sqrt(a_v.var(ddof=1) / len(a_v) + b_v.var(ddof=1) / len(b_v))
    t_stat = (a_v.mean() - b_v.mean()) / se
    p_less = 0.5 * erfc(-t_stat / np.sqrt(2.0))
    return float(t_stat), float(p_less)


def bootstrap_mean_ci(values: pd.Series, draws: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = np.asarray(values.dropna(), float)
    means = rng.choice(x, size=(draws, len(x)), replace=True).mean(axis=1)
    return np.percentile(means, [2.5, 50.0, 97.5])


def window_report(hourly: pd.DataFrame, hour_col: str, label: str) -> dict[str, float | int | str]:
    night = hourly[hour_col].isin(NIGHT_HOURS)
    inside = hourly.loc[night, "ret"].dropna()
    outside = hourly.loc[~night, "ret"].dropna()
    t_stat, p_less = welch_t_less(inside, outside)
    ci = bootstrap_mean_ci(inside, BOOTSTRAP_DRAWS, BOOTSTRAP_SEED)
    weekday = hourly.loc[night & ~hourly["is_weekend_et"], "ret"].dropna()
    weekend = hourly.loc[night & hourly["is_weekend_et"], "ret"].dropna()
    return {
        "window": label,
        "n": int(len(inside)),
        "n_out": int(len(outside)),
        "mean_bps": float(inside.mean() * 1e4),
        "mean_out_bps": float(outside.mean() * 1e4),
        "diff_bps": float((inside.mean() - outside.mean()) * 1e4),
        "ci95_lo_bps": float(ci[0] * 1e4),
        "ci95_hi_bps": float(ci[2] * 1e4),
        "welch_t": t_stat,
        "p_mean_in_lt_out": p_less,
        "compound_in": float((1 + inside).prod() - 1),
        "compound_out": float((1 + outside).prod() - 1),
        "share_neg": float((inside < 0).mean()),
        "share_neg_out": float((outside < 0).mean()),
        "weekday_mean_bps": float(weekday.mean() * 1e4),
        "weekend_mean_bps": float(weekend.mean() * 1e4),
        "weekday_n": int(len(weekday)),
        "weekend_n": int(len(weekend)),
    }


def hour_of_day(hourly: pd.DataFrame, hour_col: str) -> pd.DataFrame:
    grouped = hourly.groupby(hour_col)["ret"]
    table = grouped.agg(["count", "mean", "median", "std"])
    table["mean_bps"] = table["mean"] * 1e4
    table["median_bps"] = table["median"] * 1e4
    table["compound"] = grouped.apply(lambda s: (1 + s).prod() - 1)
    table["ann_vol"] = table["std"] * np.sqrt(ANNUALIZATION_HOURS)
    table["share_neg"] = grouped.apply(lambda s: (s < 0).mean())
    return table[["count", "mean_bps", "median_bps", "compound", "ann_vol", "share_neg"]]


def three_hour_blocks(hourly: pd.DataFrame, hour_col: str) -> pd.DataFrame:
    rows = []
    for start in range(24):
        hours = [(start + offset) % 24 for offset in range(3)]
        returns = hourly.loc[hourly[hour_col].isin(hours), "ret"].dropna()
        rows.append(
            {
                "block": f"{start:02d}:00-{(start + 3) % 24:02d}:00",
                "mean_bps": float(returns.mean() * 1e4),
                "compound": float((1 + returns).prod() - 1),
                "share_neg": float((returns < 0).mean()),
                "n": int(len(returns)),
            }
        )
    return pd.DataFrame(rows).sort_values("mean_bps")


def fmt_row(row: dict[str, float | int | str]) -> str:
    lines = [f"{row['window']}"]
    for key, value in row.items():
        if key == "window":
            continue
        if isinstance(value, float):
            lines.append(f"  {key}={value:.6f}")
        else:
            lines.append(f"  {key}={value}")
    return "\n".join(lines)


def main() -> pd.DataFrame:
    print(f"research={RESEARCH_ID} hypothesis={HYPOTHESIS_ID} experiment={EXPERIMENT_ID}")
    print(f"preregistered={PREREGISTERED}")
    csv_path, meta = resolve_source_csv()
    digest = sha256_file(csv_path)
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"SHA-256 mismatch: {digest}")
    print(f"kaggle_handle={KAGGLE_HANDLE}")
    print(f"kaggle_version={meta['version']}")
    print(f"source_csv={csv_path}")
    print(f"sha256={digest}")
    print(f"retrieved_at={meta['local']['retrieved_at']}")
    print(f"license={[item.get('name') for item in meta.get('kaggle', {}).get('info', {}).get('licenses', [])]}")

    minutes = load_minutes(csv_path)
    checks = validate_minutes(minutes)
    print("minute_checks", checks)
    if checks["missing_minutes"] or checks["nulls"] or checks["high_lt_low"] or checks["nonpositive_close"]:
        raise SystemExit("1-minute tape failed coverage checks")

    hourly = hourly_bars(minutes)
    first = hourly.iloc[0]
    last = hourly.iloc[-1]
    buyhold = float(last["close"] / first["close"] - 1)
    print(f"hours={len(hourly)} returns={int(hourly['ret'].notna().sum())}")
    print(f"first_hour={hourly.index[0]} close={first['close']:.2f} minutes={int(first['n_minutes'])}")
    print(f"last_hour={hourly.index[-1]} close={last['close']:.2f} minutes={int(last['n_minutes'])}")
    print(f"buy_and_hold={buyhold:.8f}")
    print(f"pt_offsets={sorted({str(ts.utcoffset()) for ts in hourly['pt']})}")
    print(f"et_offsets={sorted({str(ts.utcoffset()) for ts in hourly['et']})}")

    observed = hourly["ret"].dropna()
    print(
        "unconditional",
        {
            "mean_bps": float(observed.mean() * 1e4),
            "std_bps": float(observed.std(ddof=1) * 1e4),
            "ann_vol": float(observed.std(ddof=1) * np.sqrt(ANNUALIZATION_HOURS)),
            "excess_kurtosis": float(observed.kurtosis()),
        },
    )

    month_end = hourly.groupby(hourly.index.tz_convert("UTC").strftime("%Y-%m")).tail(1)
    print("month_end_closes")
    print(month_end[["close", "n_minutes"]].to_string())

    primary = window_report(hourly, "hour_pt", "PT 21:00-00:00")
    secondary = window_report(hourly, "hour_et", "ET 21:00-00:00")
    print("PRIMARY")
    print(fmt_row(primary))
    print("SECONDARY")
    print(fmt_row(secondary))

    print("hour_of_day_pt")
    print(hour_of_day(hourly, "hour_pt").to_string(float_format=lambda x: f"{x: .6f}"))
    print("hour_of_day_et")
    print(hour_of_day(hourly, "hour_et").to_string(float_format=lambda x: f"{x: .6f}"))

    cash = hourly.loc[hourly["hour_et"].eq(CASH_CLOSE_HOUR_ET), "ret"].dropna()
    cash_wd = hourly.loc[
        hourly["hour_et"].eq(CASH_CLOSE_HOUR_ET) & ~hourly["is_weekend_et"], "ret"
    ].dropna()
    print(
        "cash_close_et16",
        {
            "n": int(len(cash)),
            "mean_bps": float(cash.mean() * 1e4),
            "compound": float((1 + cash).prod() - 1),
            "weekday_mean_bps": float(cash_wd.mean() * 1e4),
        },
    )

    crashes = hourly.loc[hourly["ret"] < -0.02, ["ret", "hour_pt", "hour_et", "volume", "n_minutes"]]
    print("hours_ret_lt_minus_2pct")
    print(crashes.to_string(float_format=lambda x: f"{x: .4f}"))

    print("three_hour_blocks_pt_ranked")
    print(three_hour_blocks(hourly, "hour_pt").to_string(index=False, float_format=lambda x: f"{x: .4f}"))
    print("three_hour_blocks_et_ranked")
    print(three_hour_blocks(hourly, "hour_et").to_string(index=False, float_format=lambda x: f"{x: .4f}"))

    evening = hourly["hour_et"].isin([20, 21, 22])
    evening_wd = hourly.loc[evening & ~hourly["is_weekend_et"], "ret"].dropna()
    evening_we = hourly.loc[evening & hourly["is_weekend_et"], "ret"].dropna()
    print(
        "discovery_et_20_23",
        {
            "weekday_mean_bps": float(evening_wd.mean() * 1e4),
            "weekend_mean_bps": float(evening_we.mean() * 1e4),
            "compound": float((1 + hourly.loc[evening, "ret"].dropna()).prod() - 1),
        },
    )
    return hourly


if __name__ == "__main__":
    pd.set_option("display.width", 160)
    pd.set_option("display.max_rows", 32)
    main()
