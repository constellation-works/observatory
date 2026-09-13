"""The chapter's kill condition, as a test.

``reference.py`` (Python, float64, numpy) and ``resonance.js`` (the exact code
path the page runs) integrate the same predefined validation points on the
driven damped linear oscillator. This test runs the JavaScript under Node,
headlessly and without rendering, and requires the two implementations to
agree at the tolerance declared in ``chapter.json``.

It also checks the physics itself: the RK4-measured steady-state amplitude and
phase agree with the analytic response within the declared steady-state
tolerance, the RK4 trajectory agrees with the closed-form underdamped
transient within the declared absolute tolerance, and the convergence entry
recovers RK4's fourth order. Finally it checks that ``chapter.json`` carries
every field the chapter presentation contract requires
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
LIB = CHAPTER.parents[1] / "_lib" / "web"
NODE = shutil.which("node")

REQUIRED_CHAPTER_FIELDS = (
    "question", "prediction_prompt", "model", "controls", "presets",
    "validation_cases", "references", "source_revision", "limits",
)
CONVERGENCE_ORDER_TOLERANCE = 0.15


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
import {{ runCase }} from '{(CHAPTER / "resonance.js").as_uri()}';
import {{ validateChapter }} from '{(LIB / "chapter.js").as_uri()}';

const validation = JSON.parse(readFileSync({json.dumps(str(CHAPTER / "validation.json"))}, 'utf8'));
const fields = ['rk4_amplitude', 'rk4_phase', 'amplitude_relative_error',
                'phase_absolute_error', 'transient_max_abs_error'];
const compute = (c) => runCase({{ omega: c.omega, zeta: c.zeta, F: c.F, dt: c.dt }});
const result = validateChapter(validation, compute, {{ fields }});
// Control: the same comparison must fail when a value is perturbed just above
// the tolerance, so a passing run cannot be a vacuous one.
const perturbed = validateChapter(validation, (c) => {{
  const out = compute(c);
  out.rk4_amplitude *= 1 + 1e-6;
  return out;
}}, {{ fields }});
console.log(JSON.stringify({{
  node: process.version,
  tolerance: result.tolerance,
  pass: result.pass,
  worst: result.worst_relative_difference,
  rows: result.rows.map((r) => ({{
    omega: r.case.omega, zeta: r.case.zeta, F: r.case.F,
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
    assert len(browser_numerics["rows"]) == len(validation["cases"]) == 6
    assert browser_numerics["worst"] <= browser_numerics["tolerance"]


def test_comparison_is_not_vacuous(browser_numerics):
    """A 1e-6 relative perturbation must be caught at the declared tolerance."""
    assert browser_numerics["control_pass"] is False


@pytest.mark.parametrize("field", ["steps", "total_time", "final_state"])
def test_browser_matches_reference_bookkeeping(browser_numerics, validation, field):
    for row, expected in zip(browser_numerics["rows"], validation["cases"], strict=True):
        assert row["actual"][field] == pytest.approx(expected[field], rel=1e-9), (
            f"{field} differs for omega={row['omega']}, zeta={row['zeta']}, F={row['F']}"
        )


def test_steady_state_within_declared_tolerance(validation, chapter):
    tol = chapter["validation_cases"]["steady_state_tolerance"]
    for c in validation["cases"]:
        assert c["steady_state_within_tolerance"] is True
        assert c["amplitude_relative_error"] <= tol["amplitude_relative"]
        assert c["phase_absolute_error"] <= tol["phase_absolute"]


def test_transient_within_declared_tolerance(validation, chapter):
    tol = chapter["validation_cases"]["transient_tolerance_absolute"]
    for c in validation["cases"]:
        assert c["transient_within_tolerance"] is True
        assert c["transient_max_abs_error"] <= tol


def test_resonance_frequency_and_quality_factor(validation):
    """omega_r = omega_0 sqrt(1 - 2 zeta^2) and Q = 1/(2 zeta), for every case's zeta."""
    for c in validation["cases"]:
        zeta = c["zeta"]
        expected_q = 1.0 / (2.0 * zeta)
        assert c["analytic"]["Q"] == pytest.approx(expected_q, rel=1e-12)
        disc = 1.0 - 2.0 * zeta * zeta
        if disc > 0:
            assert c["analytic"]["omega_r"] == pytest.approx(disc**0.5, rel=1e-12)
        else:
            assert c["analytic"]["omega_r"] is None


def test_phase_crosses_quarter_turn_at_resonance(validation):
    """phi(omega_0) = pi/2 exactly, for every damping ratio in the grid."""
    import math
    for c in validation["cases"]:
        if c["omega"] == pytest.approx(1.0):
            assert c["analytic"]["phase"] == pytest.approx(math.pi / 2, rel=1e-9)


def test_convergence_recovers_fourth_order(validation):
    """The dt^4 convergence entry must show RK4's fourth order."""
    conv = validation["dt_convergence"]
    assert conv["expected_order"] == 4
    assert conv["observed_order"] == pytest.approx(4, abs=CONVERGENCE_ORDER_TOLERANCE)
    assert len(conv["dts"]) == len(conv["position_errors"]) >= 3
    for a, b in zip(conv["position_errors"], conv["position_errors"][1:], strict=False):
        assert b < a


def test_chapter_json_satisfies_the_presentation_contract(chapter):
    missing = [f for f in REQUIRED_CHAPTER_FIELDS if f not in chapter]
    assert not missing, f"chapter.json is missing {missing}"
    assert len(chapter["prediction_options"]) == 3
    assert 2 <= len(chapter["controls"]) <= 4
    for control in chapter["controls"]:
        assert {"key", "type", "label", "default", "unit"} <= set(control)
    assert {c["key"] for c in chapter["controls"]} == {"omega", "zeta", "F", "model"}
    assert chapter["presets"], "a chapter needs reproducible named parameter sets"
    for preset in chapter["presets"]:
        keys = set(preset["values"])
        assert keys <= {c["key"] for c in chapter["controls"]}
    preset_ids = {p["id"] for p in chapter["presets"]}
    for expected in (
        "light-damping-resonance", "heavy-damping", "off-resonance-beats",
        "critically-damped", "pendulum-foldover",
    ):
        assert expected in preset_ids
    assert chapter["validation_cases"]["tolerance"]["relative"] > 0
    assert chapter["references"], "a chapter cites its sources"


def test_pendulum_toggle_extends_the_starter(chapter):
    model_control = next(c for c in chapter["controls"] if c["key"] == "model")
    assert {o["value"] for o in model_control["options"]} == {"linear", "pendulum"}


def test_chapter_files_exist():
    for name in ("index.html", "sim.json", "chapter.json", "reference.py", "validation.json",
                 "resonance.js"):
        assert (CHAPTER / name).is_file(), name
    for name in ("plot.js", "chapter.js", "chapter.css", "integrators.js"):
        assert (LIB / name).is_file(), f"_lib/web/{name}"
    starter = CHAPTER.parents[1] / "pendulum-driven" / "pendulum-driven" / "index.html"
    assert starter.is_file(), "the pendulum-driven starter this chapter extends must stay in place"


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
try {{ checkParameters(chapter, {{ omega: 0.0, zeta: 0.05, F: 0.3, dt: 0.01 }}); }}
catch (e) {{ message = e.message; }}
console.log(JSON.stringify({{ message }}));
"""
    out = run_node(script)
    assert out["message"], "an out-of-range value must be refused"
    assert "omega" in out["message"]
    assert "outside the allowed range" in out["message"] or "is not one of" in out["message"]


def test_the_js_handle_guards_run_case():
    page = (CHAPTER / "index.html").read_text()
    assert "checkParameters" in page, "index.html imports the parameter guard"
    assert "runCase: (c) => runCase(checkParameters(" in page, (
        "window.__chapter.runCase must validate its arguments before integrating"
    )
