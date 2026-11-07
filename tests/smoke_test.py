"""Browser smoke test: every notebook in content/ runs in each kernel and app, with no error output
and nothing fetched from other hosts.

Each case runs in desktop Google Chrome and in WebKit (Safari's engine, which every iPad browser uses)
emulating an iPad in portrait. The emulation covers the engine, screen size and touch, not a real
tablet's memory limits.

Run after build.sh, from the repository root (needs Google Chrome; install WebKit once with
`uv run --group browser playwright install webkit`):

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
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
PUBLIC = ROOT / "workspace" / "public"
FAILURES = ROOT / "workspace" / "smoke-failures"  # screenshots of notebooks that did not finish
NOTEBOOKS = sorted(p.relative_to(ROOT / "content").as_posix() for p in (ROOT / "content").rglob("*.ipynb"))
KERNEL_START_MS = 240_000  # first load downloads the kernel and its packages
RUN_MS = 120_000
# The kernel name each site's toolbar shows: catches a site built with the other kernel.
KERNEL_NAMES = {"xeus": "(XPython)", "pyodide": "(Pyodide)"}
IPAD = "iPad (gen 11)"
# The toolbar's execution indicator reads "idle" before any kernel exists, then "initializing" or "unknown"
# while the kernel starts, then "idle" again once it is ready: wait for that second "idle".
KERNEL_READY_JS = """() => {
  const status = document.querySelector('.jp-Notebook-ExecutionIndicator')?.dataset.status;
  if (status && status !== 'idle') window.__kernelStarting = true;
  return window.__kernelStarting === true && status === 'idle';
}"""
CASES = [(b, site, app, nb) for b in ("chrome", "ipad") for site in ("xeus", "pyodide")
         for app in ("lab", "notebooks") for nb in NOTEBOOKS]


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
def new_context():
    """new_context(name): a fresh browser context, launching each browser on first use."""
    with sync_playwright() as p:
        browsers = {}

        def new_context(name):
            if name not in browsers:
                browsers[name] = p.webkit.launch() if name == "ipad" else p.chromium.launch(channel="chrome")
            return browsers[name].new_context(**(p.devices[IPAD] if name == "ipad" else {}))

        yield new_context
        for browser in browsers.values():
            browser.close()


@pytest.mark.parametrize(("browser", "site", "app", "notebook"), CASES,
                         ids=[f"{b}-{s}-{a}-{Path(n).stem}" for b, s, a, n in CASES])
def test_notebook(new_context, base_url, browser, site, app, notebook):
    context = new_context(browser)
    page = context.new_page()
    responses, console_errors, page_errors = [], [], []
    page.on("response", lambda r: responses.append((r.url, r.status)))
    page.on("pageerror", lambda e: page_errors.append(str(e)))
    # The kernel's own fetches run in a web worker; their failures show up here, not always as responses.
    # The browser's own /favicon.ico request at the server root is outside the site.
    page.on("console", lambda m: console_errors.append(m.text)
            if m.type == "error" and not m.location.get("url", "").endswith("/favicon.ico") else None)
    page.goto(f"{base_url}/{site}/{app}/index.html?path={notebook}")
    page.wait_for_selector(".jp-CodeCell", timeout=KERNEL_START_MS)
    # Run All while the kernel is still starting can lose the session in WebKit: nothing runs, or Lab
    # shows a "Select Kernel" dialog. A tablet user who taps Run All right away sees the same.
    page.wait_for_function(KERNEL_READY_JS, timeout=KERNEL_START_MS, polling=100)
    page.click("li.lm-MenuBar-item:has-text('Run')")
    page.click("li.lm-Menu-item:has-text('Run All Cells')")

    # Run All stops at the first error, so the last code cell showing "[n]:" (not "[ ]:" or "[*]:")
    # means every cell ran. Off-screen prompts can render empty, so don't check them all.
    # Stop waiting at the first error output instead of timing out.
    errors = page.locator(".jp-OutputArea-output[data-mime-type='application/vnd.jupyter.stderr']")
    last_ran = page.locator(".jp-CodeCell .jp-InputPrompt").last.filter(has_text=re.compile(r"\[\d+\]"))
    try:
        last_ran.or_(errors.first).wait_for(timeout=RUN_MS)
    except PlaywrightTimeoutError:
        FAILURES.mkdir(parents=True, exist_ok=True)
        shot = FAILURES / f"{browser}-{site}-{app}-{Path(notebook).stem}.png"
        page.screenshot(path=shot)
        prompts = page.locator(".jp-CodeCell .jp-InputPrompt").all_inner_texts()
        status = page.locator(".jp-Notebook-ExecutionIndicator").first.get_attribute("data-status")
        pytest.fail(f"cells did not finish: prompts {prompts}, kernel {status}, page errors {page_errors}, "
                    f"console errors {console_errors}, screenshot {shot}")
    assert errors.count() == 0, errors.all_inner_texts()
    assert KERNEL_NAMES[site] in page.locator(".jp-Toolbar-kernelName").first.inner_text()

    # Self-hosted: no other host, and no file missing from the site (how a pruned Pyodide package shows up).
    assert {urlparse(u).netloc for u, _ in responses if not u.startswith(base_url)} == set()
    assert not [(u, s) for u, s in responses if u.startswith(base_url) and s >= 400]
    assert not console_errors
    context.close()
