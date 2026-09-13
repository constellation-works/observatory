"""Render the static study page for one reproduction run.

The page is a single self-contained HTML file: inline CSS, base64 images, no CDN
and no JavaScript requirement. It reports, never recomputes: every number comes
from the run's own run.json/metrics.json/energies.csv and the frozen protocol.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import html
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

from .compare import load_reference

# The digitized calibration rectangle inside reference/la-1940-fig1.png, derived from
# reference/README.md: the 150 dpi page rectangle (306, 333)-(1111, 1219) inside the
# crop that extract_figure.sh takes from (210, 300). Reconstruction axes are placed on
# these fractions so the two panels share one pixel geometry as well as one data range.
CROP = {
    "file": "la-1940-fig1.png",
    "width": 950,
    "height": 1000,
    "left": 306 - 210,
    "right": 1111 - 210,
    "top": 333 - 300,
    "bottom": 1219 - 300,
    "x_range": (0.0, 30000.0),
    "y_range": (0.0, 300.0),
}

MODE_COLOURS = {1: "#1f77b4", 2: "#d62728", 3: "#2ca02c", 4: "#9467bd", 5: "#ff7f0e"}

RESIDUAL_FEATURES = [
    ("M1/M2", "mode-1 first recurrence", "mode1_recurrence"),
    ("M3", "mode-2 first maximum", "mode2_first_maximum"),
    ("M3", "mode-3 first maximum", "mode3_first_maximum"),
    ("M3", "mode-4 first maximum", "mode4_first_maximum"),
    ("reported", "mode-5 first maximum", "mode5_first_maximum"),
    ("reported", "mode-3 second maximum", "mode3_second_maximum"),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_energies(path: Path) -> tuple[np.ndarray, np.ndarray]:
    cycles: list[int] = []
    rows: list[list[float]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            cycles.append(int(row["cycle"]))
            rows.append([float(row[f"energy_mode_{mode}_units"]) for mode in range(1, 6)])
    return np.asarray(cycles, dtype=np.int64), np.asarray(rows, dtype=np.float64)


def _pyplot():
    from .compare import plt  # configured for Agg with caches outside the worktree

    return plt


def measured_features(metrics: dict[str, Any]) -> dict[str, dict[str, float] | None]:
    """Measured (t_cycles, energy_units) for every digitized feature the metrics cover."""
    features: dict[str, dict[str, float] | None] = {}
    m1, m2 = metrics["M1"], metrics["M2"]
    features["mode1_recurrence"] = (
        None
        if m1["value"] is None or m2["value"] is None
        else {"t_cycles": float(m1["value"]), "energy_units": float(m2["value"]) * 300.0}
    )
    for mode in (2, 3, 4):
        measured = metrics["M3"]["value"].get(f"mode_{mode}")
        features[f"mode{mode}_first_maximum"] = (
            None
            if measured is None
            else {
                "t_cycles": float(measured["t_cycles"]),
                "energy_units": float(measured["fraction_e1"]) * 300.0,
            }
        )
    reported = metrics["M3"].get("additional_reporting", {})
    for key, name in (
        ("mode5_first_major_peak", "mode5_first_maximum"),
        ("mode3_second_maximum", "mode3_second_maximum"),
    ):
        measured = (reported.get(key) or {}).get("value")
        features[name] = (
            None
            if measured is None
            else {
                "t_cycles": float(measured["t_cycles"]),
                "energy_units": float(measured["fraction_e1"]) * 300.0,
            }
        )
    return features


def residual_rows(metrics: dict[str, Any], reference: dict[str, Any]) -> list[dict[str, Any]]:
    """Reconstructed minus digitized at every digitized feature point."""
    measured = measured_features(metrics)
    rows: list[dict[str, Any]] = []
    for metric_id, label, key in RESIDUAL_FEATURES:
        digitized = reference["features"].get(key)
        if digitized is None:
            continue
        value = measured.get(key)
        rows.append(
            {
                "metric": metric_id,
                "label": label,
                "reference_t": digitized["t_cycles"],
                "reference_energy": digitized["energy_units"],
                "measured_t": None if value is None else value["t_cycles"],
                "measured_energy": None if value is None else value["energy_units"],
                "residual_t": None if value is None else value["t_cycles"] - digitized["t_cycles"],
                "residual_energy": (
                    None if value is None else value["energy_units"] - digitized["energy_units"]
                ),
            }
        )
    return rows


def draw_matched_reconstruction(
    output: Path, cycles: np.ndarray, energy_units: np.ndarray, protocol_version: str
) -> None:
    """Plot the reconstruction on the digitized figure's own axes geometry."""
    plt = _pyplot()
    width, height = CROP["width"], CROP["height"]
    figure = plt.figure(figsize=(width / 100.0, height / 100.0), dpi=100)
    axis = figure.add_axes(
        [
            CROP["left"] / width,
            1.0 - CROP["bottom"] / height,
            (CROP["right"] - CROP["left"]) / width,
            (CROP["bottom"] - CROP["top"]) / height,
        ]
    )
    for mode in range(1, 6):
        axis.plot(
            cycles / 1000.0,
            energy_units[:, mode - 1],
            color=MODE_COLOURS[mode],
            linewidth=1.6,
            label=f"mode {mode}",
        )
    # The original's own axis labels and units: t in thousands of cycles, energy in the
    # report's 300-unit normalization.
    axis.set(
        xlim=(CROP["x_range"][0] / 1000.0, CROP["x_range"][1] / 1000.0),
        ylim=CROP["y_range"],
        xlabel="t in thousands of cycles",
        ylabel="energy (report units, $E_k/E_1(0)\\times300$)",
    )
    axis.set_xticks(range(0, 31, 10))
    axis.set_xticks(range(0, 31, 5), minor=True)
    axis.set_yticks(range(0, 301, 100))
    axis.set_yticks(range(0, 301, 50), minor=True)
    axis.grid(alpha=0.22)
    axis.grid(alpha=0.12, which="minor")
    axis.legend(ncol=5, fontsize=11, loc="upper center", framealpha=0.9)
    axis.set_title(f"Independent reconstruction (protocol {protocol_version})", fontsize=11)
    figure.savefig(output, dpi=100)
    plt.close(figure)


def draw_residual_panel(output: Path, rows: list[dict[str, Any]], reference: dict[str, Any]) -> None:
    """Residuals with the digitization uncertainty drawn as bands, not as error-free points."""
    plt = _pyplot()
    tight = reference["uncertainty"]
    figure, (time_axis, energy_axis) = plt.subplots(
        2, 1, figsize=(9.0, 6.4), constrained_layout=True, sharex=True
    )
    labels = [row["label"] for row in rows]
    positions = np.arange(len(rows), dtype=np.float64)
    for axis, key, band, wide, unit in (
        (time_axis, "residual_t", tight["t_cycles"], 1000.0, "cycles"),
        (energy_axis, "residual_energy", tight["energy_units"], 10.0, "report units"),
    ):
        values = [0.0 if row[key] is None else row[key] for row in rows]
        axis.axhspan(-wide, wide, color="#c7d7e8", alpha=0.5, label=f"±{wide:g} {unit} calibration")
        axis.axhspan(-band, band, color="#7aa6d2", alpha=0.6, label=f"±{band:g} {unit} stated")
        axis.axhline(0.0, color="0.3", linewidth=1.0)
        axis.bar(positions, values, width=0.45, color="#1f3d63")
        axis.set_ylabel(f"reconstructed − digitized\n({unit})")
        axis.legend(fontsize=8, loc="upper right", ncol=2)
        limit = max([wide * 1.35, *[abs(value) * 1.35 for value in values]])
        axis.set_ylim(-limit, limit)
    energy_axis.set_xticks(positions)
    energy_axis.set_xticklabels(labels, rotation=20, ha="right", fontsize=9)
    time_axis.set_title("Residuals at the digitized feature points, with digitization uncertainty")
    figure.savefig(output, dpi=150)
    plt.close(figure)


def data_uri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def _text(value: Any) -> str:
    return html.escape(str(value), quote=True)


def format_value(value: Any) -> str:
    if value is None:
        return "not evaluable"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.6g}"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, dict):
        return "; ".join(f"{key}: {format_value(item)}" for key, item in value.items())
    if isinstance(value, list):
        return ", ".join(format_value(item) for item in value)
    return str(value)


def verdict_cell(passed: bool | None) -> str:
    if passed is None:
        return '<td class="verdict none">not evaluable</td>'
    return (
        '<td class="verdict pass">pass</td>' if passed else '<td class="verdict fail">fail</td>'
    )


def metric_rows(metrics: dict[str, Any], protocol: dict[str, Any]) -> str:
    names = {key: entry.get("name", key) for key, entry in protocol["metrics"].items()}
    names.update({key: entry.get("name", key) for key, entry in protocol["controls"].items()})
    roles = {key: protocol["controls"][key].get("role", "gating") for key in protocol["controls"]}
    lines: list[str] = []
    for metric_id in ("M1", "M2", "M3", "M4", "C1", "C2", "C3"):
        metric = metrics[metric_id]
        role = roles.get(metric_id)
        label = _text(names.get(metric_id, metric_id))
        if role:
            label += f' <span class="role">{_text(role)}</span>'
        lines.append(
            "<tr>"
            f'<th scope="row">{_text(metric_id)}</th>'
            f"<td>{label}</td>"
            f"<td>{_text(format_value(metric['value']))}</td>"
            f"<td>{_text(format_value(metric['reference']))}</td>"
            f"<td>{_text(format_value(metric['tolerance']))}</td>"
            f"{verdict_cell(metric['pass'])}"
            "</tr>"
        )
        if metric_id == "M3":
            for mode in (2, 3, 4):
                component = metric["value"].get(f"mode_{mode}")
                target = metric["reference"][f"mode_{mode}"]
                lines.append(
                    '<tr class="sub">'
                    f'<th scope="row">M3·{mode}</th>'
                    f"<td>mode {mode} global maximum, cycles 0–20,000</td>"
                    f"<td>{_text(format_value(component))}</td>"
                    f"<td>{_text(format_value(target))}</td>"
                    f"<td>time ±5%, height ±0.10 E₁(0)</td>"
                    f"{verdict_cell(metric.get('component_pass', {}).get(f'mode_{mode}'))}"
                    "</tr>"
                )
    return "\n".join(lines)


def definition_list(pairs: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f"<div class=\"pair\"><dt>{_text(key)}</dt><dd>{value}</dd></div>" for key, value in pairs
    )
    return f'<dl class="pairs">{items}</dl>'


def code(value: Any) -> str:
    return f"<code>{_text(format_value(value))}</code>"


def exploratory_cards(runs: list[dict[str, Any]]) -> str:
    if not runs:
        return (
            '<p class="note">No exploratory run directories were found next to this run. '
            "Create one with <code>run.py explore --set alpha=1.0</code>.</p>"
        )
    cards: list[str] = []
    for entry in runs:
        record, metrics = entry["run"], entry["metrics"]
        delta = record.get("parameter_delta", {})
        delta_html = "".join(
            f"<li><code>{_text(key)}</code>: baseline {_text(format_value(item['baseline']))} → "
            f"<strong>{_text(format_value(item['value']))}</strong></li>"
            for key, item in sorted(delta.items())
        )
        recurrence = metrics.get("M1", {}) if metrics else {}
        fraction = metrics.get("M2", {}) if metrics else {}
        parameters = record.get("effective_parameters", {})
        spanned = float(parameters.get("steps", 0)) * float(parameters.get("dt", 0.0))
        cards.append(
            '<article class="explore-card">'
            '<p class="tag">EXPLORATORY</p>'
            f"<h3>{_text(entry['directory'])}</h3>"
            f"<ul class=\"delta\">{delta_html}</ul>"
            "<dl class=\"pairs\">"
            f'<div class="pair"><dt>execution status</dt><dd>{_text(record.get("status"))}</dd></div>'
            f'<div class="pair"><dt>mode-1 argmax over 20k–30k cycles</dt>'
            f'<dd>{_text(format_value(recurrence.get("value")))}</dd></div>'
            f'<div class="pair"><dt>E₁ at that cycle / E₁(0)</dt>'
            f'<dd>{_text(format_value(fraction.get("value")))}</dd></div>'
            f'<div class="pair"><dt>model time spanned</dt>'
            f'<dd>{_text(format_value(spanned))} (steps × dt)</dd></div>'
            f'<div class="pair"><dt>baseline directory touched</dt><dd>no</dd></div>'
            "</dl>"
            '<p class="note">Exploratory runs are never the registered baseline. Their status '
            "is produced by the same decision rules against the digitized Fig. 1 reference, "
            "which describes the baseline parameters only, so a non-completed status here is a "
            "statement about the comparison, not a defect in the run.</p>"
            "</article>"
        )
    return f'<div class="explore-grid">{"".join(cards)}</div>'


STYLE = """
:root {
  color-scheme: light;
  --ink: #16202c; --muted: #56657a; --line: #d5dde7; --panel: #f6f8fb;
  --pass: #1a7f4b; --fail: #b3261e; --explore: #8a4b00;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; max-width: 100%; overflow-x: hidden; }
body {
  font: 16px/1.55 -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: var(--ink); background: #fff;
}
main { width: 100%; max-width: 1120px; margin: 0 auto; padding: 1.25rem; }
h1 { font-size: 1.7rem; line-height: 1.2; margin: 0 0 .35rem; }
h2 { font-size: 1.2rem; margin: 2rem 0 .6rem; padding-bottom: .3rem; border-bottom: 2px solid var(--line); }
h3 { font-size: 1rem; margin: .2rem 0 .5rem; word-break: break-word; }
p, li { overflow-wrap: break-word; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .86em; overflow-wrap: anywhere; }
.subtitle { color: var(--muted); margin: 0 0 .75rem; }
.pills { display: flex; flex-wrap: wrap; gap: .4rem; padding: 0; margin: .5rem 0 0; list-style: none; }
.pill { border: 1px solid var(--line); border-radius: 999px; padding: .2rem .7rem; font-size: .82rem; background: var(--panel); }
.pill.pass { border-color: var(--pass); color: var(--pass); }
.pill.fail { border-color: var(--fail); color: var(--fail); }
.pill.explore { border-color: var(--explore); color: var(--explore); }
.panel { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: .9rem 1rem; }
.pairs { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: .6rem 1.2rem; margin: 0; }
.pair { min-width: 0; }
.pair dt { font-size: .78rem; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); }
.pair dd { margin: .15rem 0 0; min-width: 0; overflow-wrap: anywhere; }
.figure-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1rem; }
figure { margin: 0; }
figure img { display: block; width: 100%; height: auto; border: 1px solid var(--line); border-radius: 6px; background: #fff; }
figcaption { color: var(--muted); font-size: .85rem; margin-top: .4rem; }
.scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
table { border-collapse: collapse; width: 100%; min-width: 520px; font-size: .92rem; }
th, td { text-align: left; padding: .42rem .5rem; border-bottom: 1px solid var(--line); vertical-align: top; }
thead th { font-size: .78rem; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); }
tr.sub th, tr.sub td { color: var(--muted); font-size: .86rem; }
.verdict.pass { color: var(--pass); font-weight: 600; }
.verdict.fail { color: var(--fail); font-weight: 600; }
.verdict.none { color: var(--muted); }
.role { color: var(--muted); font-size: .78rem; }
.note { color: var(--muted); font-size: .88rem; }
.explore-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }
.explore-card { border: 2px dashed var(--explore); border-radius: 10px; padding: .9rem 1rem; background: #fffaf3; min-width: 0; }
.explore-card .tag { margin: 0 0 .3rem; font-size: .75rem; letter-spacing: .12em; font-weight: 700; color: var(--explore); }
.explore-card .delta { margin: 0 0 .6rem; padding-left: 1.1rem; }
footer { margin-top: 2.5rem; border-top: 1px solid var(--line); padding-top: .8rem; color: var(--muted); font-size: .85rem; }
a { color: #14507d; }
@media (max-width: 480px) {
  main { padding: .9rem; }
  h1 { font-size: 1.35rem; }
  table { min-width: 420px; }
}
"""


def render(
    *,
    run_dir: Path,
    experiment_root: Path,
    repo_root: Path,
    site_dir: Path,
    exploratory_runs: list[Path],
) -> Path:
    """Render the study page for `run_dir` into `site_dir` and return index.html."""
    record = read_json(run_dir / "run.json")
    metrics = read_json(run_dir / "metrics.json")
    protocol_version = record["protocol_version"]
    protocol = read_json(experiment_root / "protocol" / f"{protocol_version}.json")
    reference = load_reference(experiment_root / "reference" / "fig1-digitized.csv")
    data_manifest = read_json(
        repo_root / "_data" / "physics" / experiment_root.name / "manifest.json"
    )
    cycles, energy_units = read_energies(run_dir / "energies.csv")

    site_dir.mkdir(parents=True, exist_ok=True)
    (site_dir / "data").mkdir(exist_ok=True)
    shutil.copyfile(run_dir / "metrics.json", site_dir / "data" / "metrics.json")
    shutil.copyfile(run_dir / "run.json", site_dir / "data" / "run.json")
    crop_source = experiment_root / "reference" / CROP["file"]
    shutil.copyfile(crop_source, site_dir / CROP["file"])
    shutil.copyfile(run_dir / "figure.png", site_dir / "reconstruction-overlay.png")
    matched = site_dir / "reconstruction-matched.png"
    draw_matched_reconstruction(matched, cycles, energy_units, protocol_version)
    residuals = residual_rows(metrics, reference)
    residual_image = site_dir / "residuals.png"
    draw_residual_panel(residual_image, residuals, reference)

    artifacts = {
        name: sha256_file(run_dir / name)
        for name in ("energies.csv", "metrics.json", "figure.png")
        if (run_dir / name).is_file()
    }
    recorded = record.get("artifact_sha256", {})
    artifact_rows = "\n".join(
        "<tr>"
        f'<th scope="row">{_text(name)}</th>'
        f"<td><code>{_text(digest)}</code></td>"
        f"<td>{'matches run.json' if recorded.get(name) == digest else 'not recorded in run.json' if name not in recorded else 'DIFFERS from run.json'}</td>"
        "</tr>"
        for name, digest in sorted(artifacts.items())
    )

    explorations: list[dict[str, Any]] = []
    for directory in sorted(exploratory_runs):
        run_json = directory / "run.json"
        if not run_json.is_file():
            continue
        metrics_path = directory / "metrics.json"
        explorations.append(
            {
                "directory": directory.name,
                "run": read_json(run_json),
                "metrics": read_json(metrics_path) if metrics_path.is_file() else {},
            }
        )

    target = protocol["target"]
    controls = protocol["controls"]
    status = record.get("status", "unknown")
    assessment = record.get("scientific_assessment", "not_evaluated")
    control_results = record.get("control_results", {})
    gating = protocol.get("decision_rules", {}).get("gating_controls", ["C1", "C2", "C3"])
    evidence_index = site_dir / "evidence" / "index.html"

    residual_table_rows = "\n".join(
        "<tr>"
        f'<th scope="row">{_text(row["label"])}</th>'
        f"<td>{_text(row['metric'])}</td>"
        f"<td>{_text(format_value(row['measured_t']))} / {_text(format_value(row['measured_energy']))}</td>"
        f"<td>{_text(format_value(row['reference_t']))} / {_text(format_value(row['reference_energy']))}</td>"
        f"<td>{_text(format_value(row['residual_t']))} / {_text(format_value(row['residual_energy']))}</td>"
        "</tr>"
        for row in residuals
    )

    control_rows = "\n".join(
        "<tr>"
        f'<th scope="row">{_text(key)}</th>'
        f"<td>{_text(controls[key]['name'])}</td>"
        f"<td>{_text('gating' if key in gating else controls[key].get('role', 'reported'))}</td>"
        f"<td>{_text(format_value(metrics[key]['value']))}</td>"
        f"<td>{_text(format_value(metrics[key]['tolerance']))}</td>"
        f"{verdict_cell(control_results.get(key, metrics[key]['pass']))}"
        "</tr>"
        for key in ("C1", "C2", "C3")
    )

    generated = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%SZ")
    parameters = record.get("effective_parameters", {})
    solver = protocol["numerics"]["solver_settings"]
    inputs = record.get("input_hashes", {})

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LA-1940 Fig. 1 reproduction — {_text(protocol_version)} — {_text(run_dir.name)}</title>
<style>{STYLE}</style>
</head>
<body>
<main>
<header>
  <h1>LA-1940 Fig. 1 — independent reconstruction</h1>
  <p class="subtitle">Run <code>{_text(run_dir.name)}</code> · protocol
    <code>{_text(protocol_version)}</code> ({_text(protocol.get("status", "unknown"))}) ·
    page generated {_text(generated)}</p>
  <ul class="pills">
    <li class="pill {'pass' if status == 'completed' else 'fail' if status == 'failed' else ''}">execution: {_text(status)}</li>
    <li class="pill {'pass' if all(value for value in control_results.values()) else 'fail'}">controls: {_text(', '.join(f'{k}={"pass" if v else "fail" if v is False else "n/a"}' for k, v in sorted(control_results.items())))}</li>
    <li class="pill {'pass' if assessment == 'supports' else ''}">assessment: {_text(assessment)}</li>
    <li class="pill">kind: {_text(record.get("kind", "unknown"))}</li>
  </ul>
</header>

<h2 id="target">1. Target</h2>
<div class="panel">
{definition_list([
    ("work", _text(target["work"])),
    ("report", _text(target["report"]) + f", report p. {_text(target.get('report_page', '?'))}"),
    ("figure", _text(target["figure"])),
    ("doi", f'<a href="https://doi.org/{_text(target["doi"])}">{_text(target["doi"])}</a>'),
    ("source", f'<a href="{_text(target["source_url"])}">{_text(target["source_url"])}</a>'),
    ("licence", _text(data_manifest["licence"])),
    ("reproduction type", _text(protocol["reproduction_type"])),
    ("caption parameters", code(target["caption_parameters"])),
])}
</div>
<p class="note">The source PDF is never tracked in this repository: it is fetched to a
temporary path and verified against
<code>_data/physics/{_text(experiment_root.name)}/manifest.json</code>
(sha256 <code>{_text(data_manifest["sha256"])}</code>, {_text(format_value(data_manifest["size_bytes"]))} bytes).
The Fig. 1 crop is a credited public-domain excerpt, and
<code>reference/fig1-digitized.csv</code> is digitization evidence with stated
uncertainty — not the original MANIAC dataset.</p>

<h2 id="provenance-assumptions">2. Provenance and assumptions</h2>
<div class="panel">
{definition_list([
    ("model", _text(protocol["model"]["name"]) + " — " + code(protocol["model"]["equation"])),
    ("boundary conditions", _text(protocol["model"]["boundary_conditions"])),
    ("initial state", code(protocol["model"]["initial_state"]["displacement"]) + " with " + _text(protocol["model"]["initial_state"]["velocity"])),
    ("integrator", _text(protocol["integrator"]["name"])),
    ("integrator assumption", _text(protocol["integrator"]["implementation_assumption"])),
    ("time step", code(f'dt = {protocol["model"]["parameters"]["dt"]} = {protocol["model"]["parameters"]["dt_expression"]}, dt^2 = {protocol["model"]["parameters"]["dt_squared"]}')),
    ("normalization", code(protocol["mode_analysis"]["comparison_normalization"])),
    ("nonlinear energy", _text(protocol["mode_analysis"]["nonlinear_energy_note"])),
    ("seeds", _text(protocol["numerics"]["seeds"])),
    ("digitization uncertainty", f'±{_text(format_value(reference["uncertainty"]["t_cycles"]))} cycles and ±{_text(format_value(reference["uncertainty"]["energy_units"]))} report units as plotted; reference/README.md states a wider ±1,000 cycle / ±10 unit calibration bound for re-measured peaks.'),
])}
</div>

<h2 id="figures">3. Original figure beside the reconstruction</h2>
<div class="figure-grid">
  <figure>
    <img src="{data_uri(site_dir / CROP["file"])}" alt="Digitized crop of Fig. 1 from LA-1940">
    <figcaption>Original LA-1940 Fig. 1 (public-domain OSTI/LANL scan, credited crop).
    Abscissa 0–30,000 cycles, ordinate 0–300 report units inside the calibrated plot
    rectangle.</figcaption>
  </figure>
  <figure>
    <img src="{data_uri(matched)}" alt="Reconstructed mode energies on the original figure's axes">
    <figcaption>Reconstruction from this run, drawn on the same axes geometry: the plotted
    rectangle occupies the identical fraction of the panel
    ({_text(CROP["left"])}–{_text(CROP["right"])} px of {_text(CROP["width"])},
    {_text(CROP["top"])}–{_text(CROP["bottom"])} px of {_text(CROP["height"])}), the same
    0–30,000 cycle abscissa and the same 0–300 report-unit ordinate.</figcaption>
  </figure>
</div>
<figure>
  <img src="{data_uri(site_dir / "reconstruction-overlay.png")}" alt="Reconstruction with digitized feature overlay">
  <figcaption>The run's own overlay figure: reconstruction curves with the digitized
  feature points and their uncertainty bars, plus the caption's 20-unit higher-mode
  ceiling.</figcaption>
</figure>

<h2 id="residuals">4. Residuals at the digitized feature points</h2>
<figure>
  <img src="{data_uri(residual_image)}" alt="Residual panel: reconstruction minus digitized values">
  <figcaption>Reconstructed minus digitized, in cycles (top) and report units (bottom).
  The inner band is the digitization uncertainty stated by
  <code>fput/compare.py</code>; the outer band is the wider calibration bound recorded in
  <code>reference/README.md</code>.</figcaption>
</figure>
<div class="scroll">
<table>
<caption class="note">Measured and digitized feature coordinates (t_cycles / energy units).</caption>
<thead><tr><th>feature</th><th>metric</th><th>reconstructed</th><th>digitized</th><th>residual</th></tr></thead>
<tbody>
{residual_table_rows}
</tbody>
</table>
</div>

<h2 id="metrics">5. Metrics</h2>
<div class="scroll">
<table>
<thead><tr><th>id</th><th>observable</th><th>value</th><th>reference</th><th>tolerance</th><th>result</th></tr></thead>
<tbody>
{metric_rows(metrics, protocol)}
</tbody>
</table>
</div>
<p class="note">Machine-readable source: <a href="data/metrics.json"><code>data/metrics.json</code></a>
(copied verbatim from <code>{_text(run_dir.name)}/metrics.json</code>) and
<a href="data/run.json"><code>data/run.json</code></a>. M4 additionally reports the summed
modes-6–31 maximum {code(metrics["M4"].get("additional_reporting", {}).get("summed_modes_6_31_max"))}
for transparency; the gate is the per-mode ceiling.</p>

<h2 id="execution">6. Execution status</h2>
<div class="panel">
{definition_list([
    ("status", _text(status)),
    ("exit code", code(record.get("exit_code"))),
    ("kind", _text(record.get("kind", "unknown")) + (" (registered baseline)" if record.get("baseline_eligible") else " (not baseline-eligible)")),
    ("started", code(record.get("started_at"))),
    ("ended", code(record.get("ended_at"))),
    ("elapsed", code(f'{record.get("runtime", {}).get("elapsed_seconds", 0.0):.3f} s') + " of a " + code(f'{record.get("runtime", {}).get("timeout_seconds")} s') + " bounded timeout"),
    ("host / platform", _text(record.get("runtime", {}).get("host", "unknown")) + " · " + _text(record.get("runtime", {}).get("platform", "unknown"))),
    ("python / numpy / matplotlib", code(record.get("runtime", {}).get("python")) + " · " + code(record.get("runtime", {}).get("numpy")) + " · " + code(record.get("runtime", {}).get("matplotlib"))),
    ("invocation", code(" ".join(record.get("command", [])))),
])}
</div>

<h2 id="controls">7. Control results</h2>
<div class="scroll">
<table>
<thead><tr><th>id</th><th>control</th><th>role</th><th>measured</th><th>threshold</th><th>result</th></tr></thead>
<tbody>
{control_rows}
</tbody>
</table>
</div>
<p class="note">{_text(protocol["decision_rules"]["failed_control"])}</p>

<h2 id="assessment">8. Scientific assessment</h2>
<div class="panel">
{definition_list([
    ("verdict", _text(assessment)),
    ("primary metrics", "M1 " + ("pass" if metrics["M1"]["pass"] else "fail" if metrics["M1"]["pass"] is False else "not evaluable") + ", M2 " + ("pass" if metrics["M2"]["pass"] else "fail" if metrics["M2"]["pass"] is False else "not evaluable")),
    ("discrepancy rule", _text(protocol["decision_rules"]["discrepancy"])),
    ("inconclusive rule", _text(protocol["decision_rules"]["inconclusive"])),
    ("amendment rule", _text(protocol["decision_rules"]["amendment"])),
])}
</div>
<p class="note">Execution status, control results and this scientific assessment are
separate statements: a completed execution with all gating controls passing does not by
itself make the reproduction claim, and C3's reported sensitivity is retained in full
rather than tuned away.</p>

<h2 id="reproducibility">9. Provenance panel</h2>
<div class="panel">
{definition_list([
    ("protocol version", code(protocol_version) + f' ({_text(protocol.get("status", "unknown"))}, frozen {_text(protocol.get("frozen_on", "unknown"))})'),
    ("code revision", code(record.get("git_revision"))),
    ("worktree clean at run", code(record.get("git_worktree_clean"))),
    ("uv.lock sha256", code(record.get("uv_lock_sha256"))),
    ("effective parameters", code(parameters)),
    ("solver settings", code({key: solver[key] for key in ("steps", "sample_every", "overflow_policy")})),
    ("floating point", code(protocol["numerics"]["floating_point"])),
    ("sampling", code(f'every {parameters.get("sample_every_cycles")} cycles')),
])}
</div>
<div class="scroll">
<table>
<caption class="note">Input hashes recorded by the run.</caption>
<thead><tr><th>input</th><th>sha256</th></tr></thead>
<tbody>
{chr(10).join(f'<tr><th scope="row">{_text(key)}</th><td><code>{_text(value)}</code></td></tr>' for key, value in sorted(inputs.items()))}
</tbody>
</table>
</div>
<div class="scroll">
<table>
<caption class="note">Artifact digests, recomputed from the run directory at page-render time.</caption>
<thead><tr><th>artifact</th><th>sha256</th><th>agreement</th></tr></thead>
<tbody>
{artifact_rows}
</tbody>
</table>
</div>

<h2 id="exploratory">10. Exploratory runs</h2>
{exploratory_cards(explorations)}

<h2 id="evidence">11. Scientific records and evidence</h2>
<p>{
  '<a href="evidence/index.html">Evidence browser</a> — the immutable orbit-research record chain '
  '(program, claim, registered protocol, run start, run result, assessment) exported as a '
  'validated static bundle.'
  if evidence_index.is_file() else
  'The evidence browser has not been generated for this site yet. Build it with '
  '<code>run.py evidence</code> (over the canonical records) or '
  '<code>run.py evidence --bundle &lt;orbit-research export.json&gt;</code> '
  '(over a validated export).'
}</p>
<p class="note">Study note, in the observatory checkout rather than in this package:
<code>knowledgebase/studies/physics/{_text(experiment_root.name)}.md</code>. Protocol
documents: <code>protocol/{_text(protocol_version)}.md</code> and
<code>protocol/{_text(protocol_version)}.json</code>. Evidence package:
<code>run.py export</code>.</p>

<footer>
Static study page rendered by <code>run.py report</code>; it reports the run and never
recomputes it. No external network resource is referenced: styles are inline and images
are embedded.
</footer>
</main>
</body>
</html>
"""
    index = site_dir / "index.html"
    index.write_text(document, encoding="utf-8")
    return index
