#!/usr/bin/env python3
"""Verify that each browser loads the exact public WOFF2 over HTTP."""
import argparse
import hashlib
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PROOF = "qa/release-1.3.0/specimen.html"
FONT = "fonts/woff2/Kleyos-Regular.woff2"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def test(out, chromium_executable):
    out.mkdir(parents=True, exist_ok=True)
    expected_sha = hashlib.sha256((ROOT / FONT).read_bytes()).hexdigest()
    report = []
    handler = partial(QuietHandler, directory=ROOT)
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            with sync_playwright() as p:
                for engine in ("chromium", "firefox"):
                    options = {"headless": True}
                    if engine == "chromium" and chromium_executable:
                        options["executable_path"] = chromium_executable
                    browser = getattr(p, engine).launch(**options)
                    try:
                        page = browser.new_page(viewport={"width": 1120, "height": 640})
                        failures = []
                        page.on("pageerror", lambda error: failures.append(str(error)))
                        url = f"http://127.0.0.1:{server.server_port}/{PROOF}"
                        with page.expect_response(lambda resp: resp.url.endswith("/" + FONT)) as source:
                            page.goto(url, wait_until="load")
                        response = source.value
                        assert response.status == 200, response.status
                        assert "font/woff2" in response.headers["content-type"]
                        assert hashlib.sha256(response.body()).hexdigest() == expected_sha
                        data = page.evaluate('''async () => {
                          const faces = await document.fonts.load('42px "Kleyos"', 'É € + $ & — %');
                          const context = document.createElement('canvas').getContext('2d');
                          context.font = '42px "Kleyos"';
                          const samples = ['Écouter, être, Noël', 'Č Ř Š Ū Ž', 'Ä Ö Ü ç'];
                          const normalization = samples.map(text =>
                            Math.abs(context.measureText(text.normalize('NFC')).width -
                                     context.measureText(text.normalize('NFD')).width));
                          return {
                            fonts: faces.map(face => [face.family, face.status]),
                            normalization,
                            overflow: document.documentElement.scrollWidth > window.innerWidth
                          };
                        }''')
                        data["fonts"] = [
                            [family.strip(chr(34)).strip(chr(39)), status]
                            for family, status in data["fonts"]
                        ]
                        assert data["fonts"] == [["Kleyos", "loaded"]], data
                        assert max(data["normalization"]) < .02, data
                        assert not data["overflow"] and not failures, (data, failures)
                        page.screenshot(path=out / f"Specimen-{engine}.png", full_page=True)
                        report.append({
                            "engine": engine,
                            "version": browser.version,
                            "transport": "http",
                            "woff2_sha256": expected_sha,
                            "http_status": response.status,
                            "passed": True,
                            **data,
                        })
                    finally:
                        browser.close()
        finally:
            server.shutdown()
            worker.join()
    (out / "BROWSER-TESTS.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "build/browser")
    parser.add_argument("--chromium-executable")
    args = parser.parse_args()
    test(args.out, args.chromium_executable)
