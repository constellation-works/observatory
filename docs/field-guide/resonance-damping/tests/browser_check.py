#!/usr/bin/env python3
"""Headless-browser check for the "Resonance and damping" chapter.

Serves the observatory root over HTTP (the chapter imports ../../../_lib/web/*.js,
so file:// will not do), opens the chapter in headless Chromium at 1280 px and
375 px and checks:

  * no console errors and no uncaught page errors,
  * every control (including the pendulum toggle) is reachable by Tab and
    operable from the keyboard, with the plotted numbers changing as a result,
  * no horizontal scrolling at 375 px,
  * the prefers-reduced-motion path renders the finished static figure without
    animating, with the same numbers,
  * the static-figure download produces an SVG.

Screenshots, the downloaded SVG and a JSON report are written under
docs/field-guide/resonance-damping/output/ (git-ignored).

Run (dk-server-1; no sudo, so Chromium's libraries come from a user directory):

    LD_LIBRARY_PATH=$HOME/.local/chromium-deps/root/usr/lib/x86_64-linux-gnu \
      uv run --with playwright python \
      docs/field-guide/resonance-damping/tests/browser_check.py

Exits non-zero if any check fails.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import socketserver
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parent
ROOT = CHAPTER.parents[2]  # docs/field-guide/<chapter> -> repository root
PAGE = "/".join(CHAPTER.relative_to(ROOT).parts) + "/index.html"
OUTDIR = CHAPTER / "output"

VIEWPORTS = {"desktop": (1280, 900), "mobile": (375, 780)}


class Server:
    """A quiet static server over the repository root."""

    def __init__(self, root: Path):
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
        handler.log_message = lambda *a, **k: None  # type: ignore[assignment]
        self.httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
        self.httpd.daemon_threads = True
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.httpd.shutdown()
        self.httpd.server_close()

    def url(self, path: str) -> str:
        return f"http://127.0.0.1:{self.port}/{path}"


class Report:
    def __init__(self):
        self.checks: list[dict] = []

    def record(self, name: str, ok: bool, detail: str = ""):
        self.checks.append({"check": name, "ok": bool(ok), "detail": detail})
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
        return ok

    @property
    def ok(self) -> bool:
        return all(c["ok"] for c in self.checks)


def reset_focus(page) -> None:
    """Send the focus back to the top of the document before a Tab walk.

    blur() alone is not enough: Chromium keeps the sequential focus navigation
    starting point at the last focused element, so the next Tab would continue
    from the middle of the page. Focusing the heading resets that point.
    """
    page.evaluate(
        """() => {
            const h = document.querySelector('.fg-chapter h1');
            h.tabIndex = -1;
            h.focus();
            window.scrollTo(0, 0);
        }"""
    )


def describe_focus(page) -> dict:
    return page.evaluate(
        """() => {
            const el = document.activeElement;
            if (!el || el === document.body) return { tag: 'body' };
            const label = el.id ? document.querySelector(`label[for="${el.id}"]`) : null;
            return {
                tag: el.tagName.toLowerCase(),
                type: el.type || '',
                id: el.id || '',
                text: (el.textContent || '').trim().slice(0, 48),
                label: label ? label.textContent.trim() : (el.getAttribute('aria-label') || ''),
                value: el.value ?? '',
            };
        }"""
    )


def state(page) -> dict:
    return page.evaluate("() => window.__chapter.state()")


def open_chapter(context, server, report: Report, tag: str):
    page = context.new_page()
    errors: list[str] = []
    page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}")
            if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    page.goto(server.url(PAGE), wait_until="load")
    page.wait_for_function("() => window.__chapter !== undefined", timeout=15000)
    page.wait_for_timeout(400)
    report.record(f"{tag}: no console or page errors", not errors, "; ".join(errors[:4]))
    return page, errors


def keyboard_walk(page, report: Report):
    """Tab through the chapter and operate every control from the keyboard."""
    reset_focus(page)
    page.keyboard.press("Tab")
    stops: list[dict] = []
    seen_download = False
    for _ in range(50):
        d = describe_focus(page)
        if d.get("tag") == "body":
            break
        stops.append(d)
        if d.get("text", "").startswith("Download static figure"):
            seen_download = True
            break
        page.keyboard.press("Tab")

    kinds = {s["tag"] for s in stops}
    report.record(
        "keyboard: every control type is in the tab order",
        {"input", "select", "button"} <= kinds,
        f"{len(stops)} tab stops: {sorted(kinds)}",
    )
    report.record("keyboard: the download control is reachable by Tab", seen_download)

    def focus_by(pred, what):
        reset_focus(page)
        for _ in range(50):
            page.keyboard.press("Tab")
            d = describe_focus(page)
            if d.get("tag") == "body":
                break
            if pred(d):
                return d
        report.record(f"keyboard: could not focus {what}", False)
        return None

    # 1. Prediction radios, then the button that starts the run.
    d = focus_by(lambda x: x.get("type") == "radio", "a prediction radio")
    if d:
        page.keyboard.press("Space")
        picked = page.evaluate("() => !!document.querySelector('input[type=radio]:checked')")
        report.record("keyboard: a prediction can be selected with Space", picked)
    d = focus_by(lambda x: x.get("text", "").startswith("Record prediction"), "the start button")
    if d:
        before = state(page)
        page.keyboard.press("Enter")
        page.wait_for_timeout(700)
        after = state(page)
        report.record("keyboard: Enter on the start button runs the simulation",
                      after["steps"] > before["steps"],
                      f"steps {before['steps']} -> {after['steps']}")

    # 2. Every model control: the plotted numbers must change.
    checks = [
        (lambda x: x.get("label", "").startswith("drive frequency"), "ArrowRight", "omega",
         "drive-frequency slider"),
        (lambda x: x.get("label", "").startswith("damping ratio"), "ArrowLeft", "zeta",
         "damping-ratio slider"),
        (lambda x: x.get("label", "").startswith("drive amplitude"), "ArrowRight", "F",
         "drive-amplitude slider"),
        (lambda x: x.get("label", "") == "restoring force", "ArrowDown", "model",
         "restoring-force (pendulum toggle) select"),
    ]
    for pred, key, field, what in checks:
        d = focus_by(pred, what)
        if not d:
            continue
        before = state(page)
        page.keyboard.press(key)
        page.wait_for_timeout(700)
        after = state(page)
        report.record(
            f"keyboard: {what} changes the model ({field}) and the plotted numbers",
            after[field] != before[field] and after["status"] != before["status"],
            f"{field} {before[field]} -> {after[field]}",
        )

    # 3. Presets, transport and reset.
    d = focus_by(lambda x: x.get("text", "") == "Critically damped", "the critically-damped preset")
    if d:
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
        s = state(page)
        report.record("keyboard: a preset applies from the keyboard",
                      abs(s["zeta"] - 1.0) < 1e-6 and abs(s["omega"] - 1.0) < 1e-6,
                      f"omega={s['omega']}, zeta={s['zeta']}")

    # zeta is a log-range slider whose step grid does not contain log10(0.02), so this
    # preset is the one that catches a preset silently landing on the nearest notch.
    d = focus_by(lambda x: x.get("text", "") == "Light damping at resonance",
                 "the light-damping preset")
    if d:
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
        s = state(page)
        report.record("a preset applies its declared value exactly, not the nearest slider step",
                      abs(s["zeta"] - 0.02) < 1e-9 and abs(s["omega"] - 1.0) < 1e-9,
                      f"omega={s['omega']}, zeta={s['zeta']} (declared omega=1.0, zeta=0.02)")

    d = focus_by(lambda x: x.get("text", "") in ("Pause", "Play"), "the play/pause button")
    if d:
        was = state(page)["playing"]
        page.keyboard.press("Space")
        page.wait_for_timeout(250)
        now = state(page)["playing"]
        report.record("keyboard: play/pause toggles", was != now, f"playing {was} -> {now}")
        if now:  # leave it paused for the single-step check
            page.keyboard.press("Space")
            page.wait_for_timeout(250)

    d = focus_by(lambda x: x.get("text", "") == "Single step", "the single-step button")
    if d:
        before = state(page)
        page.keyboard.press("Enter")
        page.wait_for_timeout(250)
        after = state(page)
        report.record("keyboard: single step advances the run by exactly one step",
                      after["steps"] == before["steps"] + 1,
                      f"steps {before['steps']} -> {after['steps']}")

    d = focus_by(lambda x: x.get("text", "") == "Reset", "the reset button")
    if d:
        page.keyboard.press("Enter")
        page.wait_for_timeout(250)
        report.record("keyboard: reset returns the run to the start",
                      state(page)["steps"] == 0)

    d = focus_by(lambda x: x.get("text", "").startswith("Animation"), "the motion toggle")
    if d:
        before = state(page)["animating"]
        page.keyboard.press("Enter")
        page.wait_for_timeout(600)
        s = state(page)
        report.record("keyboard: the reduced-motion toggle switches to the static path",
                      s["animating"] != before and (s["done"] or s["animating"]),
                      f"animating {before} -> {s['animating']}, run complete {s['done']}")
        page.keyboard.press("Enter")  # restore
        page.wait_for_timeout(400)


def check_no_horizontal_scroll(page, report: Report, width: int, tag: str):
    metrics = page.evaluate(
        """() => ({ scrollWidth: document.documentElement.scrollWidth,
                    clientWidth: document.documentElement.clientWidth,
                    widest: [...document.querySelectorAll('.fg-chapter *')]
                      .reduce((m, el) => Math.max(m, el.getBoundingClientRect().right), 0) })"""
    )
    report.record(
        f"{tag}: no horizontal scrolling at {width} px",
        metrics["scrollWidth"] <= metrics["clientWidth"] + 1,
        json.dumps(metrics),
    )


def check_validation_table(page, report: Report, tag: str):
    rows = page.locator("#validation table").first.locator("tbody tr")
    status = page.locator("#validation .fg-status").first.inner_text()
    report.record(f"{tag}: the validation table is rendered and agrees",
                  rows.count() == 6 and "all" in status and "agree" in status,
                  f"{rows.count()} rows; {status[:120]}")
    conv = page.locator("#validation table").nth(1).locator("tbody tr")
    report.record(f"{tag}: the convergence table is rendered", conv.count() == 4,
                  f"{conv.count()} rows")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", default=str(OUTDIR))
    args = parser.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    report = Report()
    with Server(ROOT) as server, sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            # --- desktop: full keyboard pass ---------------------------------
            w, h = VIEWPORTS["desktop"]
            ctx = browser.new_context(viewport={"width": w, "height": h}, accept_downloads=True)
            print(f"\n[1280 px] {server.url(PAGE)}")
            page, _ = open_chapter(ctx, server, report, "desktop")
            check_validation_table(page, report, "desktop")
            keyboard_walk(page, report)
            check_no_horizontal_scroll(page, report, w, "desktop")

            # Screenshot a finished animated run rather than a freshly reset one.
            page.get_by_role("button", name="Light damping at resonance").click()
            page.get_by_role("button", name="Play").click()
            page.wait_for_function("() => window.__chapter.state().done", timeout=60000)
            page.wait_for_timeout(300)
            done = state(page)
            report.record("desktop: an animated run reaches its step horizon",
                          done["done"] and done["steps"] == done["totalSteps"],
                          f"{done['steps']}/{done['totalSteps']} steps")
            page.screenshot(path=str(outdir / "chapter-1280.png"), full_page=True)

            # The static figure download, from the keyboard.
            with page.expect_download() as dl:
                page.get_by_role("button", name="Download static figure (SVG)").press("Enter")
            path = outdir / "figure-1280.svg"
            dl.value.save_as(str(path))
            svg = path.read_text()
            report.record("desktop: the static figure downloads as SVG",
                          svg.startswith("<svg") and "<path" in svg, f"{len(svg)} bytes")
            ctx.close()

            # --- mobile ------------------------------------------------------
            w, h = VIEWPORTS["mobile"]
            ctx = browser.new_context(viewport={"width": w, "height": h},
                                      device_scale_factor=2, is_mobile=True, has_touch=True)
            print("\n[375 px]")
            page, _ = open_chapter(ctx, server, report, "mobile")
            check_no_horizontal_scroll(page, report, w, "mobile")
            cols = page.evaluate(
                "() => getComputedStyle(document.querySelector('.fg-grid')).gridTemplateColumns")
            report.record("mobile: the sim/plot grid reflows to a single column",
                          len(cols.split()) == 1, cols)
            check_validation_table(page, report, "mobile")
            page.get_by_role("button", name="Critically damped").click()
            page.wait_for_timeout(200)
            page.get_by_role("button", name="Play").click()
            page.wait_for_function("() => window.__chapter.state().done", timeout=60000)
            page.wait_for_timeout(300)
            page.screenshot(path=str(outdir / "chapter-375.png"), full_page=True)
            ctx.close()

            # --- prefers-reduced-motion --------------------------------------
            ctx = browser.new_context(viewport={"width": 1280, "height": 900},
                                      reduced_motion="reduce")
            print("\n[prefers-reduced-motion: reduce]")
            page, _ = open_chapter(ctx, server, report, "reduced-motion")
            s = state(page)
            report.record("reduced motion: the static figure is complete without animating",
                          (not s["animating"]) and s["done"] and s["steps"] == s["totalSteps"],
                          f"animating={s['animating']}, done={s['done']}, "
                          f"steps={s['steps']}/{s['totalSteps']}")
            disabled = page.evaluate(
                """() => [...document.querySelectorAll('.fg-transport button')]
                       .filter(b => b.disabled).map(b => b.textContent)"""
            )
            report.record("reduced motion: play and single-step are disabled",
                          sorted(disabled) == ["Play", "Single step"], json.dumps(disabled))
            numbers = page.locator(".fg-status").first.inner_text()
            report.record("reduced motion: the same numbers are reported",
                          "run complete" in numbers, numbers[:140])
            page.screenshot(path=str(outdir / "chapter-reduced-motion.png"), full_page=True)
            ctx.close()
        finally:
            browser.close()

    (outdir / "browser-check.json").write_text(
        json.dumps({"page": PAGE, "checks": report.checks, "ok": report.ok}, indent=2) + "\n")
    print(f"\n{sum(c['ok'] for c in report.checks)}/{len(report.checks)} checks passed; "
          f"artifacts in {outdir}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
