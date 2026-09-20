"""E02 methodology: BTC 5-minute early Polymarket lean (H09).

Cuts are frozen in H09. Run from the Parallax repo:

    uv run --group notebook python notebooks/R01-crypto/E02-btc-5m-early-polymarket-lean.py
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from math import erfc, sqrt
from pathlib import Path

import numpy as np
import pandas as pd

# --- frozen identity ---
RESEARCH_ID = "R01"
HYPOTHESIS_ID = "H09"
EXPERIMENT_ID = "E02"
PREREGISTERED = True
KAGGLE_HANDLE = "kachoio/polymarket-5-minute-crypto-updown-markets"
KAGGLE_VERSION = "1"
MARKETS_FILE = "btc_markets.parquet"
TICKS_FILE = "btc_ticks.parquet"
EXPECTED_SHA256 = {
    MARKETS_FILE: "8e0ed78021bd98d3dba18829266103ebd9b46a77f6ba872a1c7f98be77b506bd",
    TICKS_FILE: "173760b951ac0a2c795e1c3873a506e2fd4372db356dd3515f06582820ff975e",
}
PRIMARY_TAUS = (5, 15, 30)
OPEN_TAU = 0
EXTREME_OPEN_ABS = 0.15
NIGHT_HOURS_PT = (21, 22, 23)
BOOTSTRAP_DRAWS = 8_000
BOOTSTRAP_SEED = 7


def repo_root() -> Path:
    here = Path.cwd().resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "docs/research/R01-crypto"
        ).is_dir():
            return candidate
    raise SystemExit("run from the Parallax repository")


def resolve_source_dir() -> tuple[Path, dict]:
    binary = shutil.which("datasets") or str(Path.home() / ".local/bin/datasets")
    meta = json.loads(subprocess.check_output([binary, "json", KAGGLE_HANDLE], text=True))
    version = str(meta["version"])
    if version != KAGGLE_VERSION:
        raise SystemExit(f"expected Kaggle version {KAGGLE_VERSION}, found {version}")
    source_dir = Path(meta["local"]["resolved_path"])
    for name in (MARKETS_FILE, TICKS_FILE):
        if not (source_dir / name).is_file():
            raise SystemExit(f"missing source file: {source_dir / name}")
    return source_dir, meta


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normal_sf(z: float) -> float:
    return 0.5 * erfc(z / sqrt(2.0))


def one_sample_t_greater(values: np.ndarray, mu0: float = 0.0) -> tuple[float, float]:
    x = np.asarray(values, float)
    se = x.std(ddof=1) / sqrt(len(x))
    t_stat = (x.mean() - mu0) / se
    return float(t_stat), float(normal_sf(t_stat))


def two_sample_t_greater(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    se = sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    t_stat = (a.mean() - b.mean()) / se
    return float(t_stat), float(normal_sf(t_stat))


def bootstrap_mean_ci(values: np.ndarray, draws: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = np.asarray(values, float)
    means = rng.choice(x, size=(draws, len(x)), replace=True).mean(axis=1)
    return np.percentile(means, [2.5, 50.0, 97.5])


def snapshot_at_or_before(joined: pd.DataFrame, tau: int) -> pd.DataFrame:
    eligible = joined.loc[joined["elapsed_s"] <= tau]
    if eligible.empty:
        return eligible.iloc[0:0].copy()
    return (
        eligible.sort_values(["condition_id", "elapsed_s"])
        .groupby("condition_id", as_index=False, sort=False)
        .tail(1)
        .copy()
    )


def attach_labels(snap: pd.DataFrame) -> pd.DataFrame:
    out = snap.copy()
    out["mid_up"] = (out["bu"] + out["au"]) / 2.0
    out["depth"] = out["du"] + out["dd"]
    out["spread_up"] = out["au"] - out["bu"]
    valid_outcome = out["outcome"].isin(["Up", "Down"])
    valid_mid = out["mid_up"].notna()
    out = out.loc[valid_outcome & valid_mid].copy()
    out["s"] = np.where(out["outcome"].eq("Up"), 1.0, -1.0)
    out["signed_mid"] = out["s"] * (out["mid_up"] - 0.5)
    out["agree"] = (
        ((out["mid_up"] > 0.5) & out["outcome"].eq("Up"))
        | ((out["mid_up"] < 0.5) & out["outcome"].eq("Down"))
    ).astype(float)
    out["tie"] = np.isclose(out["mid_up"], 0.5)
    out["is_night_pt"] = out["hour_pt"].isin(NIGHT_HOURS_PT)
    out["is_weekend_et"] = out["dow_et"] >= 5
    return out


def metric_block(frame: pd.DataFrame, label: str) -> dict[str, float | int | str]:
    signed = frame["signed_mid"].to_numpy(float)
    agree = frame.loc[~frame["tie"], "agree"].to_numpy(float)
    t_signed, p_signed = one_sample_t_greater(signed, 0.0)
    t_agree, p_agree = one_sample_t_greater(agree, 0.5)
    ci_signed = bootstrap_mean_ci(signed, BOOTSTRAP_DRAWS, BOOTSTRAP_SEED)
    ci_agree = bootstrap_mean_ci(agree, BOOTSTRAP_DRAWS, BOOTSTRAP_SEED)
    return {
        "slice": label,
        "n": int(len(frame)),
        "n_ties": int(frame["tie"].sum()),
        "n_agree_denom": int(len(agree)),
        "mean_signed_mid": float(signed.mean()),
        "median_signed_mid": float(np.median(signed)),
        "ci95_lo_signed": float(ci_signed[0]),
        "ci95_hi_signed": float(ci_signed[2]),
        "t_signed_gt_0": t_signed,
        "p_signed_gt_0": p_signed,
        "agreement": float(agree.mean()) if len(agree) else float("nan"),
        "ci95_lo_agree": float(ci_agree[0]) if len(agree) else float("nan"),
        "ci95_hi_agree": float(ci_agree[2]) if len(agree) else float("nan"),
        "t_agree_gt_50": t_agree if len(agree) else float("nan"),
        "p_agree_gt_50": p_agree if len(agree) else float("nan"),
        "mean_mid_up": float(frame["mid_up"].mean()),
        "share_up_outcome": float(frame["outcome"].eq("Up").mean()),
    }


def compare_slices(
    inside: pd.DataFrame, outside: pd.DataFrame, label: str
) -> dict[str, float | int | str]:
    a = inside["signed_mid"].to_numpy(float)
    b = outside["signed_mid"].to_numpy(float)
    t_stat, p_greater = two_sample_t_greater(a, b)
    return {
        "contrast": label,
        "n_in": int(len(inside)),
        "n_out": int(len(outside)),
        "mean_in": float(a.mean()),
        "mean_out": float(b.mean()),
        "diff": float(a.mean() - b.mean()),
        "t_in_gt_out": t_stat,
        "p_in_gt_out": p_greater,
    }


def fmt_row(row: dict[str, float | int | str]) -> str:
    title_key = "slice" if "slice" in row else "contrast"
    lines = [str(row[title_key])]
    for key, value in row.items():
        if key == title_key:
            continue
        if isinstance(value, float):
            lines.append(f"  {key}={value:.6f}")
        else:
            lines.append(f"  {key}={value}")
    return "\n".join(lines)


def main() -> dict[int, pd.DataFrame]:
    print(f"research={RESEARCH_ID} hypothesis={HYPOTHESIS_ID} experiment={EXPERIMENT_ID}")
    print(f"preregistered={PREREGISTERED}")
    source_dir, meta = resolve_source_dir()
    print(f"kaggle_handle={KAGGLE_HANDLE}")
    print(f"kaggle_version={meta['version']}")
    print(f"source_dir={source_dir}")
    print(f"retrieved_at={meta['local']['retrieved_at']}")
    licenses = [item.get("name") for item in meta.get("kaggle", {}).get("info", {}).get("licenses", [])]
    print(f"license={licenses}")

    for name, expected in EXPECTED_SHA256.items():
        digest = sha256_file(source_dir / name)
        if digest != expected:
            raise SystemExit(f"SHA-256 mismatch for {name}: {digest}")
        print(f"sha256_{name}={digest}")

    markets = pd.read_parquet(source_dir / MARKETS_FILE)
    ticks = pd.read_parquet(source_dir / TICKS_FILE)
    print(
        "coverage",
        {
            "n_markets": int(len(markets)),
            "n_ticks": int(len(ticks)),
            "market_start_min": str(markets["market_start"].min()),
            "market_start_max": str(markets["market_start"].max()),
            "outcome_null": int(markets["outcome"].isna().sum()),
            "outcome_up": int(markets["outcome"].eq("Up").sum()),
            "outcome_down": int(markets["outcome"].eq("Down").sum()),
            "n_ticks_lt_300": int((markets["n_ticks"] < 300).sum()),
            "unique_tick_markets": int(ticks["condition_id"].nunique()),
        },
    )

    market_cols = [
        "condition_id",
        "market_start",
        "market_end",
        "outcome",
        "n_ticks",
        "volume",
        "liquidity",
    ]
    joined = ticks.merge(markets[market_cols], on="condition_id", how="inner", validate="m:1")
    joined["elapsed_s"] = (joined["ts_utc"] - joined["market_start"]).dt.total_seconds()
    start_pt = joined["market_start"].dt.tz_convert("America/Los_Angeles")
    start_et = joined["market_start"].dt.tz_convert("America/New_York")
    joined["hour_pt"] = start_pt.dt.hour
    joined["dow_et"] = start_et.dt.dayofweek
    print(
        "join_checks",
        {
            "tick_rows": int(len(joined)),
            "elapsed_lt_0": int((joined["elapsed_s"] < -1e-9).sum()),
            "elapsed_gt_300": int((joined["elapsed_s"] > 300 + 1e-9).sum()),
            "pt_offsets": sorted(start_pt.dt.strftime("%z").unique().tolist()),
            "et_offsets": sorted(start_et.dt.strftime("%z").unique().tolist()),
        },
    )

    open_snap = attach_labels(snapshot_at_or_before(joined, OPEN_TAU))
    open_extreme = set(
        open_snap.loc[(open_snap["mid_up"] - 0.5).abs() > EXTREME_OPEN_ABS, "condition_id"]
    )
    print(
        "open_snapshot",
        {
            "n": int(len(open_snap)),
            "n_extreme_abs_gt_0_15": int(len(open_extreme)),
            "mean_abs_mid_minus_half": float((open_snap["mid_up"] - 0.5).abs().mean()),
        },
    )

    last_snap = attach_labels(
        joined.sort_values(["condition_id", "elapsed_s"])
        .groupby("condition_id", as_index=False, sort=False)
        .tail(1)
    )
    print("QC_LAST_TICK")
    print(fmt_row(metric_block(last_snap, "last tick in window")))

    snapshots: dict[int, pd.DataFrame] = {}
    for tau in PRIMARY_TAUS:
        snap = attach_labels(snapshot_at_or_before(joined, tau))
        snapshots[tau] = snap
        print("PRIMARY")
        print(fmt_row(metric_block(snap, f"tau={tau}s all BTC 5m")))

        dropped = snap.loc[~snap["condition_id"].isin(open_extreme)]
        print("SECONDARY")
        print(fmt_row(metric_block(dropped, f"tau={tau}s drop extreme open")))

        night = snap.loc[snap["is_night_pt"]]
        day = snap.loc[~snap["is_night_pt"]]
        weekend = snap.loc[snap["is_weekend_et"]]
        weekday = snap.loc[~snap["is_weekend_et"]]
        print("SECONDARY")
        print(fmt_row(compare_slices(night, day, f"tau={tau}s night PT 21-23 vs rest")))
        print("SECONDARY")
        print(fmt_row(compare_slices(weekend, weekday, f"tau={tau}s weekend ET vs weekday")))

        depth_ok = snap.loc[snap["depth"].notna()].copy()
        tercile = pd.qcut(
            depth_ok["depth"], 3, labels=["low", "mid", "high"], duplicates="drop"
        )
        depth_ok = depth_ok.assign(depth_tercile=tercile)
        snapshots[tau] = snap
        low = depth_ok.loc[depth_ok["depth_tercile"].eq("low")]
        high = depth_ok.loc[depth_ok["depth_tercile"].eq("high")]
        print("SECONDARY")
        print(
            fmt_row(
                compare_slices(
                    low, high, f"tau={tau}s lowest vs highest PM bid-depth tercile"
                )
            )
        )
        print("SECONDARY")
        print(fmt_row(metric_block(low, f"tau={tau}s lowest PM bid-depth tercile")))

        short = snap.loc[snap["n_ticks"] < 300]
        full = snap.loc[snap["n_ticks"] >= 300]
        print("SECONDARY")
        print(
            fmt_row(
                metric_block(full, f"tau={tau}s n_ticks>=300")
                if len(full)
                else {"slice": f"tau={tau}s n_ticks>=300", "n": 0}
            )
        )
        print(
            "short_markets",
            {"tau": tau, "n_short": int(len(short)), "n_full": int(len(full))},
        )

    return snapshots


if __name__ == "__main__":
    pd.set_option("display.width", 160)
    pd.set_option("display.max_rows", 32)
    main()
