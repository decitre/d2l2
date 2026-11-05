"""Browser smoke test: every notebook in content/ runs in each kernel and app, with no error output
and nothing fetched from other hosts.

Run after build.sh, from the repository root (needs Google Chrome):

    uv run --group browser pytest tests/smoke_test.py -v

Adapted from jl-forge's examples/demo/smoke_test.py.
"""

import re
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import pytest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
PUBLIC = ROOT / "workspace" / "public"
NOTEBOOKS = sorted(p.relative_to(ROOT / "content").as_posix() for p in (ROOT / "content").rglob("*.ipynb"))
KERNEL_START_MS = 240_000  # first load downloads the kernel and its packages
RUN_MS = 120_000
# runtime-check.ipynb prints which kernel runs it.
REPORT = re.compile(r"(xeus-python|pyodide) on emscripten, Python 3\.\d+\.\d+, NumPy \d+\.\d+")
CASES = [(site, app, nb) for site in ("xeus", "pyodide") for app in ("lab", "notebooks") for nb in NOTEBOOKS]


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="module")
def base_url():
    if not (PUBLIC / "index.html").is_file():
        pytest.skip(f"{PUBLIC} not built; run ./build.sh first")
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(_QuietHandler, directory=PUBLIC))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        yield browser
        browser.close()


@pytest.mark.parametrize(("site", "app", "notebook"), CASES, ids=[f"{s}-{a}-{Path(n).stem}" for s, a, n in CASES])
def test_notebook(browser, base_url, site, app, notebook):
    page = browser.new_page()
    responses = []
    page.on("response", lambda r: responses.append((r.url, r.status)))
    page.goto(f"{base_url}/{site}/{app}/index.html?path={notebook}")
    page.wait_for_selector(".jp-CodeCell", timeout=KERNEL_START_MS)
    page.click("li.lm-MenuBar-item:has-text('Run')")
    page.click("li.lm-Menu-item:has-text('Run All Cells')")  # queued until the kernel is ready

    # Run All stops at the first error, so the last code cell showing "[n]:" (not "[ ]:" or "[*]:")
    # means every cell ran. Off-screen prompts can render empty, so don't check them all.
    # Stop waiting at the first error output instead of timing out.
    errors = page.locator(".jp-OutputArea-output[data-mime-type='application/vnd.jupyter.stderr']")
    last_ran = page.locator(".jp-CodeCell .jp-InputPrompt").last.filter(has_text=re.compile(r"\[\d+\]"))
    last_ran.or_(errors.first).wait_for(timeout=KERNEL_START_MS + RUN_MS)
    assert errors.count() == 0, errors.all_inner_texts()
    if notebook == "runtime-check.ipynb":
        assert REPORT.search(page.inner_text("body")).group(1) == site.replace("xeus", "xeus-python")

    # Self-hosted: no other host, and no file missing from the site (how a pruned Pyodide package shows up).
    assert {urlparse(u).netloc for u, _ in responses if not u.startswith(base_url)} == set()
    assert not [(u, s) for u, s in responses if u.startswith(base_url) and s >= 400]
    page.close()
