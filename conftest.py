import os
from datetime import datetime

import pytest
from playwright.sync_api import sync_playwright

from utils.config import HEADLESS, BROWSER, SLOW_MO


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser_type = getattr(p, BROWSER)
        browser = browser_type.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    context = browser.new_context(
        record_video_dir="artifacts/videos",
        viewport={"width": 1366, "height": 768},
    )

    # Start tracing for each test; we'll save it only if the test fails
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # If the test passed, tracing should be stopped (without saving) before close
    # We'll handle stop() in the report hook. Here we just close.
    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    yield page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # only on the actual test call outcome
    if report.when != "call":
        return

    context = item.funcargs.get("context")
    page = item.funcargs.get("page")

    # If we don't have context, we can't save traces
    if not context:
        return

    if report.passed:
        # Stop tracing without saving (keeps things clean)
        context.tracing.stop()
        return

    # On failure: save screenshot + trace zip
    os.makedirs("artifacts", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if page:
        screenshot_path = f"artifacts/{item.name}_{timestamp}.png"
        page.screenshot(path=screenshot_path, full_page=True)

    trace_path = f"artifacts/{item.name}_{timestamp}.zip"
    context.tracing.stop(path=trace_path)