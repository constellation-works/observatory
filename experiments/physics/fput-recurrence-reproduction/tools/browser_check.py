#!/usr/bin/env python3
"""Headless-Chromium check for a rendered study page.

Loads the page at a desktop and a 375 px viewport and reports, for each:
document-level horizontal scrolling, page errors, failed requests, and any
remotely-loaded resource (a self-contained page must load none).

    LD_LIBRARY_PATH=$HOME/.local/chromium-deps/root/usr/lib/x86_64-linux-gnu \
      uv run --with playwright python tools/browser_check.py <index.html> [--screenshots DIR]

Exits 0 when every viewport is clean, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

MEASURE = """() => ({
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
  remoteResources: [...document.querySelectorAll('img[src], script[src], link[href], iframe[src]')]
    .map(e => e.getAttribute('src') || e.getAttribute('href'))
    .filter(u => /^(https?:)?\\/\\//.test(u)),
  sectionsRendered: document.querySelectorAll('h2').length,
})"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", type=Path)
    parser.add_argument("--screenshots", type=Path)
    parser.add_argument("--width", type=int, action="append", default=[])
    arguments = parser.parse_args()
    widths = arguments.width or [1280, 375]

    from playwright.sync_api import sync_playwright

    target = arguments.page.resolve()
    if arguments.screenshots:
        arguments.screenshots.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for width in widths:
            page = browser.new_page(viewport={"width": width, "height": 900})
            problems: list[str] = []
            page.on("pageerror", lambda error: problems.append(f"pageerror: {error}"))
            page.on("requestfailed", lambda request: problems.append(f"requestfailed: {request.url[:120]}"))
            page.goto(target.as_uri(), wait_until="load")
            measured = page.evaluate(MEASURE)
            if arguments.screenshots:
                page.screenshot(path=str(arguments.screenshots / f"page-{width}.png"), full_page=True)
            results.append({
                "width": width,
                "horizontal_scroll": measured["scrollWidth"] > measured["clientWidth"],
                "sections": measured["sectionsRendered"],
                "remote_resources": measured["remoteResources"],
                "problems": problems,
                **{k: measured[k] for k in ("scrollWidth", "clientWidth")},
            })
            page.close()
        browser.close()
    print(json.dumps({"page": target.name, "viewports": results}, indent=2))
    failed = any(r["horizontal_scroll"] or r["remote_resources"] or r["problems"] for r in results)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
