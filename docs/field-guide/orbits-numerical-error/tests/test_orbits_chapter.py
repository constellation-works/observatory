"""The chapter's kill condition, as a test.

``reference.py`` (Python, float64, numpy) and ``orbits.js`` (the exact code path
the page runs) integrate the same predefined validation points. This test runs
the JavaScript under Node, headlessly and without rendering, and requires the
two implementations to agree at the tolerance declared in ``chapter.json``.

It also checks that ``validation.json`` is current, that the convergence-order
table the page renders really comes from ``reference.py`` and recovers the order
of each method, and that ``chapter.json`` carries every field the chapter
presentation contract requires of it
(``docs/design/paper-reproduction-workbench.md``).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

CHAPTER = Path(__file__).resolve().parent.parent
LIB = CHAPTER.parents[2] / "_lib" / "web"
NODE = shutil.which("node")

# The contract every field-guide chapter.json must satisfy.
REQUIRED_CHAPTER_FIELDS = (
    "question", "prediction_prompt", "model", "controls", "presets",
    "validation_cases", "references", "source_revision", "limits",
)
EXPECTED_ORDERS = {
    "euler": 1,
    "semi-implicit-euler": 1,
    "leapfrog-kdk": 2,
    "rk4": 4,
}
ORDER_TOLERANCE = 0.15


def load(name: str) -> dict:
    return json.loads((CHAPTER / name).read_text())


@pytest.fixture(scope="module")
def chapter() -> dict:
    return load("chapter.json")


@pytest.fixture(scope="module")
def validation() -> dict:
    return load("validation.json")


def run_node(script: str) -> dict:
    """Run an ES module under Node and return the JSON it prints."""
    proc = subprocess.run(
        [NODE, "--input-type=module"],
        input=script, capture_output=True, text=True, cwd=CHAPTER, timeout=300,
    )
    if proc.returncode != 0:
        raise AssertionError(f"node failed ({proc.returncode}):\n{proc.stderr}")
    return json.loads(proc.stdout)


@pytest.fixture(scope="module")
def browser_numerics() -> dict:
    """The browser's own numerics for every validation case, plus a control."""
    if NODE is None:
        pytest.skip("node is not on PATH; the browser numerics cannot be run headlessly")
    script = f"""
import {{ readFileSync }} from 'node:fs';
import {{ runCase }} from '{(CHAPTER / "orbits.js").as_uri()}';
import {{ validateChapter }} from '{(LIB / "chapter.js").as_uri()}';

const validation = JSON.parse(readFileSync({json.dumps(str(CHAPTER / "validation.json"))}, 'utf8'));
const compute = (c) => runCase({{ v0: c.v0, dt: c.dt, integrator: c.integrator,
                                 periods: c.periods }});
const result = validateChapter(validation, compute);
// Control: the same comparison must fail when a value is perturbed just above
// the tolerance, so a passing run cannot be a vacuous one.
const perturbed = validateChapter(validation, (c) => {{
  const out = compute(c);
  out.max_rel_energy_error *= 1 + 1e-6;
  return out;
}});
console.log(JSON.stringify({{
  node: process.version,
  tolerance: result.tolerance,
  pass: result.pass,
  worst: result.worst_relative_difference,
  rows: result.rows.map((r) => ({{
    v0: r.case.v0, dt: r.case.dt, integrator: r.case.integrator,
    pass: r.pass, worst: r.worst_relative_difference, worst_field: r.worst_field,
    actual: compute(r.case),
  }})),
  control_pass: perturbed.pass,
}}));
"""
    return run_node(script)


def test_validation_file_is_current():
    """validation.json must be what reference.py produces right now."""
    proc = subprocess.run(
        [sys.executable, str(CHAPTER / "reference.py"), "--check"],
        capture_output=True, text=True, timeout=600,
    )
    assert proc.returncode == 0, f"{proc.stdout}\n{proc.stderr}"


def test_every_validation_case_agrees(browser_numerics, validation):
    """The kill condition: browser numerics vs the independent Python reference."""
    failures = [r for r in browser_numerics["rows"] if not r["pass"]]
    assert not failures, json.dumps(failures, indent=2)
    assert len(browser_numerics["rows"]) == len(validation["cases"]) == 16
    assert browser_numerics["worst"] <= browser_numerics["tolerance"]


def test_comparison_is_not_vacuous(browser_numerics):
    """A 1e-6 relative perturbation must be caught at the declared tolerance."""
    assert browser_numerics["control_pass"] is False


@pytest.mark.parametrize("field", ["steps", "t_final", "final_state"])
def test_browser_matches_reference_bookkeeping(browser_numerics, validation, field):
    for row, expected in zip(browser_numerics["rows"], validation["cases"], strict=True):
        assert row["actual"][field] == pytest.approx(expected[field], rel=1e-9), (
            f"{field} differs for v0={row['v0']}, dt={row['dt']}, {row['integrator']}"
        )


def test_convergence_table_recovers_the_method_orders(validation):
    """The visible convergence table must show Δt¹, Δt², Δt⁴ where theory says so."""
    rows = validation["convergence"]["rows"]
    assert {r["integrator"] for r in rows} == set(EXPECTED_ORDERS)
    for row in rows:
        expected = EXPECTED_ORDERS[row["integrator"]]
        assert row["expected_order"] == expected
        assert row["observed_order_position"] == pytest.approx(expected, abs=ORDER_TOLERANCE)
        assert row["observed_order_energy"] == pytest.approx(expected, abs=ORDER_TOLERANCE)
        assert len(row["dts"]) == len(row["position_errors"]) == len(row["energy_errors"])


def test_chapter_json_satisfies_the_presentation_contract(chapter):
    missing = [f for f in REQUIRED_CHAPTER_FIELDS if f not in chapter]
    assert not missing, f"chapter.json is missing {missing}"
    assert len(chapter["prediction_options"]) == 3
    assert 2 <= len(chapter["controls"]) <= 4
    for control in chapter["controls"]:
        assert {"key", "type", "label", "default", "unit"} <= set(control)
    assert chapter["presets"], "a chapter needs reproducible named parameter sets"
    for preset in chapter["presets"]:
        keys = set(preset["values"])
        assert keys <= {c["key"] for c in chapter["controls"]}
    assert chapter["validation_cases"]["tolerance"]["relative"] > 0
    assert chapter["references"], "a chapter cites its sources"


def test_chapter_files_exist():
    for name in ("index.html", "sim.json", "chapter.json", "reference.py", "validation.json",
                 "orbits.js"):
        assert (CHAPTER / name).is_file(), name
    for name in ("plot.js", "chapter.js", "chapter.css"):
        assert (LIB / name).is_file(), f"_lib/web/{name}"
    assert (LIB.parent / "README.md").is_file(), "_lib/README.md documents the contract"


def test_sim_manifest_is_a_gallery_entry():
    sim = load("sim.json")
    assert sim["kind"] == "web"
    assert sim["entry"] == "index.html"
    assert sim["slug"] == CHAPTER.name
    assert sim["provenance"]["sources"], "the gallery entry records its reference sources"


def test_out_of_range_parameters_are_refused_with_a_message():
    """The page's JS handle guards runCase, so a bad value is a message, not NaNs."""
    if NODE is None:
        pytest.skip("node is not on PATH; the browser guard cannot be exercised")
    script = f"""
import {{ readFileSync }} from 'node:fs';
import {{ checkParameters }} from '{(LIB / "chapter.js").as_uri()}';

const chapter = JSON.parse(readFileSync({json.dumps(str(CHAPTER / "chapter.json"))}, 'utf8'));
let message = null;
try {{ checkParameters(chapter, {{ v0: 9.0, dt: 0.01, integrator: "rk4", periods: 1 }}); }}
catch (e) {{ message = e.message; }}
console.log(JSON.stringify({{ message }}));
"""
    out = run_node(script)
    assert out["message"], "an out-of-range value must be refused"
    assert "v0" in out["message"]
    assert "outside the allowed range" in out["message"] or "is not one of" in out["message"]


def test_the_js_handle_guards_run_case():
    page = (CHAPTER / "index.html").read_text()
    assert "checkParameters" in page, "index.html imports the parameter guard"
    assert "runCase: (c) => runCase(checkParameters(" in page, (
        "window.__chapter.runCase must validate its arguments before integrating"
    )
