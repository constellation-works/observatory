"""The chapter's kill condition, as a test.

``reference.py`` (Python, float64, numpy) and ``waves.js`` (the exact code path
the page runs) integrate the same predefined validation points on the linear
N-mass chain. This test runs the JavaScript under Node, headlessly and without
rendering, and requires the two implementations to agree at the tolerance
declared in ``chapter.json``.

It also checks the physics itself: every standing-wave period agrees with the
analytic dispersion relation to within 1%, the two-pulse superposition maximum
matches the linear sum of the two pulses run separately, the reflection sign
matches the fixed/free prediction, and the convergence entry recovers
Stormer-Verlet's second order. Finally it checks that ``chapter.json`` carries
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
LIB = CHAPTER.parents[2] / "_lib" / "web"
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
import {{ runCase }} from '{(CHAPTER / "waves.js").as_uri()}';
import {{ validateChapter }} from '{(LIB / "chapter.js").as_uri()}';

const validation = JSON.parse(readFileSync({json.dumps(str(CHAPTER / "validation.json"))}, 'utf8'));
const fields = ['period_measured', 'measured_max', 'measured_sign', 'extremum'];
const compute = (c) => runCase(c);
const result = validateChapter(validation, compute, {{ fields }});
// Control: the same comparison must fail when a value is perturbed just above
// the tolerance, so a passing run cannot be a vacuous one.
const perturbed = validateChapter(validation, (c) => {{
  const out = compute(c);
  if (typeof out.period_measured === 'number') out.period_measured *= 1 + 1e-6;
  if (typeof out.measured_max === 'number') out.measured_max += 1e-6 + Math.abs(out.measured_max) * 1e-6;
  return out;
}}, {{ fields }});
console.log(JSON.stringify({{
  node: process.version,
  tolerance: result.tolerance,
  pass: result.pass,
  worst: result.worst_relative_difference,
  rows: result.rows.map((r) => ({{
    kind: r.case.kind, pass: r.pass, worst: r.worst_relative_difference,
    worst_field: r.worst_field, actual: compute(r.case),
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
    assert len(browser_numerics["rows"]) == len(validation["cases"]) == 12
    assert browser_numerics["worst"] <= browser_numerics["tolerance"]


def test_comparison_is_not_vacuous(browser_numerics):
    """A 1e-6 relative perturbation must be caught at the declared tolerance."""
    assert browser_numerics["control_pass"] is False


def test_dispersion_periods_within_one_percent_of_analytic(validation):
    """omega_k = 2 sin(pi k / 2N): every measured standing-wave period agrees with
    the closed-form dispersion relation to within the chapter's declared 1%."""
    dispersion = [c for c in validation["cases"] if c["kind"] == "dispersion"]
    assert {c["mode"] for c in dispersion} == set(range(1, 9))
    for c in dispersion:
        assert c["period_within_tolerance"] is True
        assert c["period_relative_error"] <= c["period_tolerance_relative"]
        assert c["period_relative_error"] <= 0.01


def test_two_pulse_superposition(validation):
    """In phase must double the single-pulse amplitude; antiphase must cancel it,
    and in both cases the combined run must equal the linear sum of the two runs."""
    superposition = [c for c in validation["cases"] if c["kind"] == "superposition"]
    in_phase = next(c for c in superposition if c["phase"] == pytest.approx(0.0))
    antiphase_case = next(c for c in superposition if c["phase"] == pytest.approx(3.141592653589793))
    assert antiphase_case["measured_max"] == pytest.approx(0.0, abs=1e-6)
    assert in_phase["measured_max"] == pytest.approx(2 * in_phase["amplitude"], rel=0.01)
    for c in superposition:
        assert c["measured_max"] == pytest.approx(c["predicted_max"], rel=1e-6, abs=1e-9)


def test_reflection_sign_fixed_vs_free(validation):
    """A fixed end inverts the reflected pulse; a free end does not."""
    cases = {c["boundary"]: c for c in validation["cases"] if c["kind"] == "reflection"}
    assert cases["fixed"]["measured_sign"] == -1.0
    assert cases["free"]["measured_sign"] == 1.0
    for c in cases.values():
        assert c["sign_matches_expected"] is True


def test_convergence_recovers_second_order(validation):
    """The dt^2 convergence entry must show Stormer-Verlet's second order."""
    conv = validation["dt_convergence"]
    assert conv["expected_order"] == 2
    assert conv["observed_order"] == pytest.approx(2, abs=CONVERGENCE_ORDER_TOLERANCE)
    assert len(conv["dts"]) == len(conv["period_errors"]) >= 3
    # Monotonically shrinking dt must shrink the error (dt^2 scaling, not noise).
    for a, b in zip(conv["period_errors"], conv["period_errors"][1:], strict=False):
        assert b < a


def test_chapter_json_satisfies_the_presentation_contract(chapter):
    missing = [f for f in REQUIRED_CHAPTER_FIELDS if f not in chapter]
    assert not missing, f"chapter.json is missing {missing}"
    assert len(chapter["prediction_options"]) == 3
    assert 2 <= len(chapter["controls"]) <= 4
    for control in chapter["controls"]:
        assert {"key", "type", "label", "default", "unit"} <= set(control)
    assert {c["key"] for c in chapter["controls"]} == {"mode", "phase", "boundary", "pulseWidth"}
    assert chapter["presets"], "a chapter needs reproducible named parameter sets"
    for preset in chapter["presets"]:
        keys = set(preset["values"])
        assert keys <= {c["key"] for c in chapter["controls"]}
    preset_ids = {p["id"] for p in chapter["presets"]}
    for expected in (
        "standing-wave-k1", "standing-wave-k2", "standing-wave-k3",
        "two-pulses-in-phase", "two-pulses-antiphase",
        "single-pulse-fixed-end", "single-pulse-free-end",
    ):
        assert expected in preset_ids
    assert chapter["validation_cases"]["tolerance"]["relative"] > 0
    assert chapter["references"], "a chapter cites its sources"


def test_limits_link_the_fput_study(chapter):
    assert any("fput-recurrence-reproduction" in item for item in chapter["limits"])


def test_chapter_files_exist():
    for name in ("index.html", "sim.json", "chapter.json", "reference.py", "validation.json",
                 "waves.js"):
        assert (CHAPTER / name).is_file(), name
    for name in ("plot.js", "chapter.js", "chapter.css"):
        assert (LIB / name).is_file(), f"_lib/web/{name}"


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
try {{ checkParameters(chapter, {{ kind: "dispersion", mode: 99, N: 32, dt: 0.1, periods: 1.0 }}); }}
catch (e) {{ message = e.message; }}
console.log(JSON.stringify({{ message }}));
"""
    out = run_node(script)
    assert out["message"], "an out-of-range value must be refused"
    assert "mode" in out["message"]
    assert "outside the allowed range" in out["message"] or "is not one of" in out["message"]


def test_the_js_handle_guards_run_case():
    page = (CHAPTER / "index.html").read_text()
    assert "checkParameters" in page, "index.html imports the parameter guard"
    assert "runCase: (c) => runCase(checkParameters(" in page, (
        "window.__chapter.runCase must validate its arguments before integrating"
    )
