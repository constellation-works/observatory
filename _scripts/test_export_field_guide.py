"""Allowlist and exclusion invariants for ``_scripts/export-field-guide.sh``."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "_scripts" / "export-field-guide.sh"
FPUT_SITE = REPO / "research" / "R005-fput-recurrence-reproduction" / "output" / "site"
CHAPTER_REL = Path("docs") / "field-guide" / "orbits-numerical-error"
FORBIDDEN_PATH = re.compile(
    r"_archive/|lineage|_data/|\.orbit|\.env|\.git|tests/|reference\.py"
)
ATTR_RE = re.compile(r"""\b(?:href|src)\s*=\s*(['"])(.*?)\1""", re.I)
IMPORT_RE = re.compile(
    r"""(?:import|export)\s+(?:type\s+)?(?:\{[\s\S]*?\}|\*\s+as\s+\w+|\w+)\s*from\s*['"]([^'"]+)['"]"""
    r"""|import\s*\(\s*['"]([^'"]+)['"]\s*\)"""
    r"""|import\s+['"]([^'"]+)['"]"""
)
WEB_FILES = (
    "chapter.js",
    "chapter.css",
    "plot.js",
    "panel.js",
    "loop.js",
    "canvas2d.js",
    "integrators.js",
    "vec.js",
    "style.css",
)


def run_export(
    output: Path, *, cwd: Path | None = None, check: bool = True
) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        [str(SCRIPT), "--output", str(output)],
        cwd=cwd or REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and proc.returncode != 0:
        raise AssertionError(
            f"export failed ({proc.returncode})\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc


def local_targets(text: str) -> list[str]:
    found = [url for _, url in ATTR_RE.findall(text)]
    for match in IMPORT_RE.finditer(text):
        found.append(next(g for g in match.groups() if g))
    out = []
    for url in found:
        raw = url.strip().split("#", 1)[0].split("?", 1)[0]
        if not raw or raw.startswith(("http://", "https://", "mailto:", "data:", "javascript:")):
            continue
        out.append(raw)
    return out


def assert_inside(export_root: Path, source: Path, url: str) -> Path:
    assert not url.startswith("/"), f"non-relative url {url!r} in {source}"
    target = (source.parent / url).resolve()
    root = export_root.resolve()
    assert root == target or root in target.parents, f"{url!r} from {source} left the export"
    assert target.exists(), f"{url!r} from {source} is missing ({target})"
    return target


@pytest.fixture
def export_dir(tmp_path: Path) -> Path:
    out = tmp_path / "field-guide-export"
    run_export(out, cwd=tmp_path)
    return out


def test_script_rebuilds_allowlist_and_prints_chapter_count(export_dir: Path) -> None:
    chapter = export_dir / CHAPTER_REL
    assert (chapter / "index.html").is_file()
    assert (chapter / "orbits.js").is_file()
    assert (chapter / "chapter.json").is_file()
    assert (chapter / "sim.json").is_file()
    assert (chapter / "validation.json").is_file()
    assert (chapter / "README.md").is_file()
    assert not (chapter / "tests").exists()
    assert not (chapter / "reference.py").exists()
    assert not list(export_dir.rglob("reference.py"))
    assert not list(export_dir.rglob("tests"))

    for name in WEB_FILES:
        assert (export_dir / "_lib" / "web" / name).is_file()
    assert not (export_dir / "_lib" / "vendor").exists()

    assert (export_dir / "docs" / "field-guide" / "README.md").is_file()
    assert (export_dir / "index.html").is_file()
    assert (export_dir / "LICENSES.md").is_file()
    assert (export_dir / "reference" / "la-1940-fig1.png").is_file()
    assert (export_dir / "reference" / "README.md").is_file()

    licenses = (export_dir / "LICENSES.md").read_text()
    assert "LA-1940" in licenses
    assert "public domain" in licenses.lower()
    assert "osti.gov" in licenses.lower()
    assert "as in the observatory repository" in licenses
    assert "three.js" not in licenses.lower()


def test_orbits_index_imports_resolve_inside_export(export_dir: Path) -> None:
    html_path = export_dir / CHAPTER_REL / "index.html"
    html = html_path.read_text()
    urls = local_targets(html)
    assert any(url.endswith("_lib/web/chapter.js") for url in urls)
    assert any(url.endswith("./orbits.js") or url.endswith("orbits.js") for url in urls)
    for url in urls:
        assert_inside(export_dir, html_path, url)
    # The shared harness is copied verbatim: the chapter keeps its in-repository
    # ../../../_lib/web prefix, which the mirrored export layout resolves.
    assert "../../../_lib/web/" in html

    js_path = export_dir / CHAPTER_REL / "orbits.js"
    for url in local_targets(js_path.read_text()):
        assert_inside(export_dir, js_path, url)


def test_root_index_uses_relative_links(export_dir: Path) -> None:
    index = export_dir / "index.html"
    html = index.read_text()
    hrefs = local_targets(html)
    assert f"{CHAPTER_REL.as_posix()}/index.html" in hrefs
    for url in hrefs:
        assert not url.startswith("/"), url
        assert_inside(export_dir, index, url)


def test_forbidden_path_fragments_and_home_strings_absent(export_dir: Path) -> None:
    for path in export_dir.rglob("*"):
        rel = path.relative_to(export_dir).as_posix()
        assert FORBIDDEN_PATH.search(rel) is None, rel
    hits = subprocess.run(
        ["grep", "-rIl", "/home/", str(export_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert hits.returncode == 1, hits.stdout
    secrets = subprocess.run(
        ["grep", "-rIlE", r"(BEGIN (RSA|OPENSSH|EC) PRIVATE|api[_-]?key|token=)", str(export_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert secrets.returncode == 1, secrets.stdout


def test_rebuilds_from_scratch(tmp_path: Path) -> None:
    out = tmp_path / "field-guide-export"
    out.mkdir()
    junk = out / "stale.txt"
    junk.write_text("should vanish")
    run_export(out)
    assert not junk.exists()
    assert (out / CHAPTER_REL / "index.html").is_file()


def test_runnable_from_any_cwd(tmp_path: Path) -> None:
    cwd = tmp_path / "elsewhere"
    cwd.mkdir()
    out = tmp_path / "export"
    proc = run_export(out, cwd=cwd)
    assert "3 chapter" in proc.stdout
    assert "orbits-numerical-error" in proc.stdout
    assert (out / CHAPTER_REL / "index.html").is_file()


def test_skips_missing_fput_site(tmp_path: Path) -> None:
    if FPUT_SITE.is_dir():
        pytest.skip("FPUT study site is already generated")
    out = tmp_path / "export"
    proc = run_export(out)
    assert "skipping" in proc.stderr
    assert not (out / "study").exists()


@pytest.fixture
def scratch_fput_site():
    if FPUT_SITE.exists():
        pytest.skip("real FPUT study site present; not mutating it")
    FPUT_SITE.mkdir(parents=True)
    try:
        yield FPUT_SITE
    finally:
        shutil.rmtree(FPUT_SITE, ignore_errors=True)


def test_copies_fput_site_when_present(tmp_path: Path, scratch_fput_site: Path) -> None:
    (scratch_fput_site / "index.html").write_text("<!DOCTYPE html><title>FPUT</title><p>ok</p>\n")
    (scratch_fput_site / "notes.txt").write_text("relative only\n")
    out = tmp_path / "export"
    run_export(out)
    assert (out / "study" / "fput-recurrence-reproduction" / "index.html").is_file()
    assert (out / "study" / "fput-recurrence-reproduction" / "notes.txt").is_file()
    html = (out / "index.html").read_text()
    assert "study/fput-recurrence-reproduction/index.html" in html


def test_self_check_rejects_forbidden_tests_path(tmp_path: Path, scratch_fput_site: Path) -> None:
    nested = scratch_fput_site / "tests"
    nested.mkdir()
    (nested / "secret.txt").write_text("nope\n")
    proc = run_export(tmp_path / "export", check=False)
    assert proc.returncode != 0
    assert "tests/" in proc.stderr


def test_self_check_rejects_absolute_home_path(tmp_path: Path, scratch_fput_site: Path) -> None:
    (scratch_fput_site / "leak.txt").write_text("see /home/someone/secret\n")
    proc = run_export(tmp_path / "export", check=False)
    assert proc.returncode != 0
    assert "/home/" in proc.stderr


def test_self_check_rejects_href_outside_export(tmp_path: Path, scratch_fput_site: Path) -> None:
    (scratch_fput_site / "index.html").write_text(
        '<!DOCTYPE html><a href="../../../../etc/passwd">nope</a>\n'
    )
    proc = run_export(tmp_path / "export", check=False)
    assert proc.returncode != 0
    assert "outside" in proc.stderr.lower() or "leaves the export" in proc.stderr
